from selenium import webdriver
import time
from datetime import datetime,timedelta
import json
import os
import sys
from urllib.parse import urlparse
import requests
import glob
import hashlib
import shutil



'''
设置停留时间
'''
def sleep_time():
    time.sleep(10)

'''
加载浏览器驱动

'''
def load_driver(url,browser,path):
    
    # Chrome驱动加载
    if browser == 'chrome':
        driver = webdriver.Chrome(executable_path=path)
    # Edge驱动加载
    elif browser == 'edge':
        driver = webdriver.Edge(executable_path=path)
    driver.maximize_window()  # 最小化界面
    # 发起请求
    #print(browser)
    driver.get(url)
    return driver

'''
模拟登录
'''
def login(driver,username_xpath,password_xpath,button_xpath,username,password):
    username_field = driver.find_element_by_xpath(username_xpath)
    password_field = driver.find_element_by_xpath(password_xpath)
    # 输入用户名和密码
    username_field.send_keys(username)
    password_field.send_keys(password)
    # 提交form
    button = driver.find_element_by_xpath(button_xpath)
    button.click()
   
    while (1):
        try:
            check = driver.find_element_by_css_selector('p[class="mdMN06Number"]')
            print("验证码为：",format(check.text))
            break
        except Exception:
            continue
    #time.sleep(15)
    return driver


'''
根据xpath跳转到对应界面
'''
def find_element(driver,xpath):
    #time.sleep(5)
    while (1):
        try:
            element = driver.find_element_by_xpath(xpath)
            #print(element)
            break
        except Exception:
            continue
    element.click()
      
    return driver


def getmd5(string):
    md5 = hashlib.md5()
    md5.update(string.encode())
    md5res = md5.hexdigest()
    return md5res

'''
更新driver
'''
def switch(driver):
    handlers = driver.window_handles
    driver.switch_to.window(handlers[-1])
    return driver


'''
关闭页面
'''
def quit(driver):
    driver.quit()


'''
模拟用户到达群聊界面
'''
def driver_chat(url,username,password,browser,driver_path):
    driver = load_driver(url,browser,driver_path)
    #link = '/html/body/div/div[1]/main/div/div/div[1]/div/div/div/div[2]/div[2]/div/a[1]'   #这是之前的xpath，但是后面官方修改了界面，变成了下面这个链接
    link = '/html/body/div[1]/div[1]/div[1]/div[3]/div/div[2]/a'
    driver = find_element(driver,link)
    #sleep_time()
    
    login1 = '/html/body/div[2]/div/div[3]/div/form/div/input'
    driver = find_element(driver,login1)
    #sleep_time()
    username_xpath = '/html/body/div/div/div/div/div/div[2]/div/form/fieldset/div[1]/input'
    password_xpath = '/html/body/div/div/div/div/div/div[2]/div/form/fieldset/div[2]/input'
    button_xpath = '/html/body/div/div/div/div/div/div[2]/div/form/fieldset/div[3]/button'
    driver = login(driver,username_xpath,password_xpath,button_xpath,username,password)
    driver = switch(driver)
    message = '/html/body/div[1]/div/div/section/div/ul/li[2]/a/div'
    #message = '/html/body/div/div/div/aside/div/div/div/section/div[2]/div/ul/li/a'
    #sleep_time()
    driver = find_element(driver,message)
    #sleep_time()
    user = '/html/body/div/div/div/section/div/div/section/div/div[2]/a/a/article/section'
    driver = find_element(driver,user)
    #sleep_time()
    account = '/html/body/div/div/div/section/div/div/section/div/div/section[1]/p/p/a'
    driver = find_element(driver,account)
    
    driver = switch(driver)
    #sleep_time()
    
    chats = '/html/body/div/div[1]/nav/div/ul[1]/li[7]/a'
    driver = find_element(driver,chats)
    #sleep_time()
    driver = switch(driver)
    
    assigning = '/html/body/div[2]/div/div[2]/div/div/div/div[3]/button'
    driver = find_element(driver,assigning)
    '''/html/body/div[2]/div/div[1]/div/div[2]/nav/div[1]/a
    basic = '/html/body/div[2]/div/div[1]/div[1]/div[2]/nav/div[3]/div[2]/div[2]/a'
    driver = find_element(driver,basic)'''
    return driver

'''
获取每个群聊的url地址
'''
def get_group_url(driver,group):
    
    driver = find_element(driver,group)
    driver = switch(driver)
    url = driver.current_url
    #sleep_time()
    return driver,url


'''
下载群聊文件
'''
def download(driver):
    download = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[2]/section[4]/div[3]/div/button'
    driver = find_element(driver,download)
    #sleep_time()

'''
从html中获取群聊对应的div
'''
def get_div(driver,url):
    #driver.get(url)
    #html_content = driver.page_source
    scroll = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[2]/div[2]/div'
    element = driver.find_element_by_xpath(scroll)
    # 使用JavaScript代码来滚动元素到顶部
    driver.execute_script("arguments[0].scrollTop = 0", element)
    #sleep_time()
    sleep_time()
    while(1):
        try:
            div_list = driver.find_elements_by_css_selector('div[class="position-relative"]')
            break
        except Exception:
            continue
    return div_list

'''
创建群聊消息保存文件
'''
def create_file(path):
    file = open(path,'a',encoding='utf-8')
    return file


'''
用户类型判断
'''
def user_type(user_name):
    # 这里用户分为用户发送和机器人发送或自动回复
    if user_name == None or user_name.text.strip() == 'Auto-response':
        user_name = 'Auto-response'
        sender_type = 'Account'
    else:
        user_name = user_name.text.strip()
        sender_type = 'User'
    return user_name,sender_type


'''
日前转换
在页面上如果是今天或昨天发送的内容则转换为具体的时间，方便存储
'''
def date_switch(date):
    if str(date) == 'Today':
        date = datetime.now().replace(microsecond=0)
        date = date.strftime("%a, %b %d")
    if str(date) == 'Yesterday':
        date = datetime.now().replace(microsecond=0)-timedelta(days=1)
        date = date.strftime("%a, %b %d")
    return date

def get_text_img_voice(content_text_div,content_img,voices,filename1,file_size,timestamp1,save_path):
    content_list = []
    image_info = []
    voice_info = []

    filename111 = save_path+'image'
    # 获取具体的聊天记录
    if content_text_div != []:
        
        if(len(content_text_div)==1):
            content_list.append(content_text_div[0].get_attribute('textContent').strip())
        else:
            str1111 = content_text_div[0].get_attribute('textContent').strip()
            for content in content_text_div[1:]:
                
                str1111 = str1111 +'/'+ content.get_attribute('textContent').strip()
            content_list.append(str1111)
           
    if content_img != []:
        for content in content_img:
            class_img = content.get_attribute('class')
            if class_img == 'chat-item-sticker' or class_img == 'sticon emojione':
                #content_list.append({'image url':content.get_attribute('src')})
                url = content.get_attribute('src')
                if(url[-3:] in ['png','jpg']):
                    image_info.append('type: '+ url[-3:])
                    image_info.append('url: '+url)
                    
                    parsed_url = urlparse(url)
                    path = parsed_url.path
                    filename = os.path.basename(path)
                    base = os.path.splitext(filename)[0]
                    image_info.append('name: '+base)
                    timestamp = str(int(time.time()))
                    filename1 = save_path+'image/'+timestamp+'.'+ url[-3:]
                    try:
                        image_size = dowenload_image(url,filename1)
                    except Exception as e:
                        image_size=0
                        filename1 = ''
                        print(e)
                    image_info.append('path: '+filename1)
                    image_info.append('length: '+str(int(image_size)))
                    image_info.append('download_datetime: '+str(datetime.now().replace(microsecond=0)))
                else:
                    image_info.append('type: ' +'mp4')
                    image_info.append('url: '+url)
                    
                    parsed_url = urlparse(url)
                    path = parsed_url.path
                    filename = os.path.basename(path)
                    base = os.path.splitext(filename)[0]
                    image_info.append('name: '+ base)
                    #print(base)
                    '''timestamp = str(int(time.time()))
                    filename1 = 'line/image/'+timestamp+'.mp4'

                    image_size = dowenload_image(url,filename1)'''
                    target_file_path = os.path.join(filename111, os.path.basename(filename1))

                    # 如果目标文件已经存在，删除它
                    if os.path.exists(target_file_path)==False:
                        filename1 = shutil.move(filename1,filename111)
                    image_info.append('path: '+ filename1)
                    image_info.append('length: '+str(file_size))
                    image_info.append('download_datetime: '+ str(datetime.now().replace(microsecond=0)))
    
            else:
                url = content.get_attribute('src')
                if(url[-3:] in ['png','jpg']):
                    
                    url = content.get_attribute('src')
                    image_info.append('type: '+ url[-3:])
                    image_info.append('url: '+ url)
                    parsed_url = urlparse(url)
                    path = parsed_url.path
                    filename1 = os.path.basename(path)
                    base = os.path.splitext(filename1)[0]
                    image_info.append('name: '+ base)
                    timestamp = str(int(time.time()))
                    filename1 = save_path+'image/'+timestamp+'.'+ url[-3:]
                    try:
                        image_size = dowenload_image(url,filename1)
                    except Exception as e:
                        image_size=0
                        filename1 = ''
                        print(e)
                    image_info.append('path: '+ filename1)
                    image_info.append('length: '+str(int(image_size)))
                    image_info.append('download_datetime: '+ str(datetime.now().replace(microsecond=0)))
                else:
                    image_info.append('type: '+ 'mp4')
                    image_info.append('url: '+ url)
                    
                    parsed_url = urlparse(url)
                    path = parsed_url.path
                    filename = os.path.basename(path)
                    base = os.path.splitext(filename)[0]
                    #print(base)
                    image_info.append('name: '+ base)
                    '''timestamp = str(int(time.time()))
                    filename1 = 'line/image/'+timestamp+'.mp4'

                    image_size = dowenload_image(url,filename1)'''
                    target_file_path = os.path.join(filename111, os.path.basename(filename1))

                    # 如果目标文件已经存在，删除它
                    if os.path.exists(target_file_path)==False:
                        filename1 = shutil.move(filename1,filename111)
                    image_info.append('path: '+ filename1)
                    image_info.append('length: '+ str(file_size))
                    image_info.append('download_datetime: '+ str(datetime.now().replace(microsecond=0)))
    
    
    if voices != []:
        for voice in voices:
            #content_list.append([{'voice path':filename1},{'voice time':voice.text.strip()},{'length':file_size}])
            voice_info.append('type: '+ 'm4a')
            target_file_path = os.path.join(filename111, os.path.basename(filename1))

            # 如果目标文件已经存在，删除它
            if os.path.exists(target_file_path)==False:
                filename1 = shutil.move(filename1,filename111)
            voice_info.append('path: '+ filename1)
            voice_info.append('time: '+ voice.text.strip())
            voice_info.append('length: '+ str(file_size))
            voice_info.append('download_datetime: '+ str(datetime.now().replace(microsecond=0)))
             

    return content_list, image_info, voice_info

def user_detail(user_detail_file,member_list,user_detial_id,user_all_list,user_detail_list,serviceid):
    for member in member_list:
        user_detail = {}
        user_detail['serviceid'] = serviceid
        
        user_detail['user_name'] = member
        #user_all_list.append(member) 
        user_detail['auto_id'] = user_detial_id
        
        user_detail['group_type'] = 1
        user_detail['data_source'] = 'TRS'
        user_detail['update_time'] = str(datetime.now().replace(microsecond=0))
        user_detail['crawler_time'] = str(datetime.now().replace(microsecond=0))
        user_detail['intime'] = str(datetime.now().replace(microsecond=0))
        if user_is_excist(user_all_list,member) == False:
            user_detial_id = user_detial_id+1
            user_all_list.append(member)
            user_detail_list.append(user_detail)
            #json.dump(user_detail,user_detail_file,ensure_ascii=False)
    return user_detial_id,user_all_list,user_detail_list



def group_detail(group_detial_file,i,group_number,group_name,group_user_number,url,group_detail_list,serviceid):
    group_detail = {}
    group_detail['serviceid'] =serviceid
    group_detail['auto_id'] = i
    group_detail['group_id']= group_number
    group_detail['group_name']= group_name
    group_detail['group_url']= url
    group_user_number = group_user_number.replace('(', '')  # 去掉左括号
    group_user_number = group_user_number.replace(')', '')  # 去掉右括号
    group_detail['group_user_number']= group_user_number
    group_detail['group_type'] = 1
    group_detail['data_source'] = 'TRS'
    group_detail['update_time'] = str(datetime.now().replace(microsecond=0))
    group_detail['crawler_time'] = str(datetime.now().replace(microsecond=0))
    group_detail['intime'] = str(datetime.now().replace(microsecond=0))
    group_detail_list.append(group_detail)
    #json.dump(group_detail,group_detial_file,ensure_ascii=False) 
    return group_detail_list

def group_relation(group_relation_file,user_relation_id,group_number,member_list,first_time,last_time,relation_all_list,group_relation_list,serviceid):
    
    for member in member_list:
        group_relation ={}
        group_relation['serviceid'] = serviceid
        group_relation['group_id']= group_number
        group_relation['user_name']= member
        
        
        group_relation['auto_id'] = user_relation_id
        group_relation['md5'] = getmd5(group_number)
        
        group_relation['first_time']= first_time[member]
        group_relation['last_time']= last_time[member]
        group_relation['group_type'] = 1
        group_relation['data_source'] = 'TRS'
        group_relation['update_time'] = str(datetime.now().replace(microsecond=0))
        group_relation['crawler_time'] = str(datetime.now().replace(microsecond=0))
        group_relation['intime'] = str(datetime.now().replace(microsecond=0))
        if group_relation_is_excist(relation_all_list,group_number,member) == False:
            user_relation_id =user_relation_id+1
            relation_all_list.append({'group_id':group_number,'user_name':member}) 
            group_relation_list.append(group_relation)
            #json.dump(group_relation,group_relation_file,ensure_ascii=False)
        
    return user_relation_id,relation_all_list,group_relation_list


def dowenload_image(image_url,image_file_path):
    proxies = {
    "http": "http://127.0.0.1:7890",  # WARNING: 修改代理链接
    "https": "http://127.0.0.1:7890"  # WARNING: 修改代理链接
    }
    #image_url = image_url.replace("https://", "http://")
    response = requests.get(image_url,stream=True,proxies=proxies)
    #print(response.status_code)
    if(response.status_code == 200):
        image_size = response.headers.get('content-length',None)
        with open(image_file_path,'wb') as file:
            #print(file)
            for chunk in response.iter_content(1024):
                file.write(chunk)
    return image_size
    
def group_info(group_info_file,content_list,date,Massage_id,group_number,sender_type,true_time,data_id_list,user_name,types,time2,number,start_time,information_path,message_count,information_list,image_info,voice_info,serviceid):
    if len(data_id_list) == 1:
        messages = {}
        messages['servicerid'] = serviceid
        message_count,start_time=judeg(types,time2,number,start_time,Massage_id,information_path,message_count)
        Massage_id = Massage_id+1
        messages['message_id'] = data_id_list[0]
        messages['user_name'] = user_name
        
        messages['auto_id'] = Massage_id
        messages['md5'] = getmd5(group_number+str(data_id_list[0]))
        messages['group_id'] = group_number
        
        messages['group_type'] = 1
        messages['sender_type'] = sender_type
        if(bool(content_list)):
            
            messages['content'] = content_list
        if (bool(image_info)):
            if(image_info[0]=='type: mp4'):
                messages['video_info'] = list(image_info)
            else:
                messages['image_info'] = list(image_info)
        if (bool(voice_info)):
            messages['voice_info'] = list(voice_info)
        #messages['pubdate'] = date
        #print(date)
        date1 = datetime.strptime(date,"%a, %b %d")
        formatted_date = date1.strftime("%m-%d")
        #messages['pubdate'] = date
        messages['pubtime'] = '2023-'+str(formatted_date)+" "+true_time
        messages['data_source'] = 'TRS'
        messages['update_time'] = str(datetime.now().replace(microsecond=0))
        messages['crawler_time'] = str(datetime.now().replace(microsecond=0))
        messages['intime'] = str(datetime.now().replace(microsecond=0))
        #json.dump(messages,group_info_file,ensure_ascii=False)
        information_list.append(messages)
        message_count = message_count+1 
    else:
        for data in data_id_list:
            messages = {}
            messages['serviceid'] = serviceid
            message_count,start_time=judeg(types,time2,number,start_time,Massage_id,information_path,message_count)
            Massage_id = Massage_id+1
            messages['message_id'] = data
            messages['user_name'] = user_name
            
            messages['auto_id'] = Massage_id
            messages['md5'] = getmd5(group_number+str(data))
            messages['group_id'] = group_number
            
            messages['group_type'] = 1
            messages['sender_type'] = sender_type
            if(bool(content_list)):
                #messages['content'] = content_list[data_id_list.index(data)]
                messages['content'] = content_list
            if (bool(image_info)):
                if(image_info[0]=='type: mp4'):
                    messages['video_info'] = image_info
                else:
                    messages['image_info'] = image_info
            if (bool(voice_info)):
                messages['voice_info'] = voice_info
            date1 = datetime.strptime(date,"%a, %b %d")
            formatted_date = date1.strftime("%m-%d")
            #messages['pubdate'] = date
            messages['pubtime'] = '2023-'+formatted_date+" "+true_time
            messages['data_source'] = 'TRS'
            messages['update_time'] = str(datetime.now().replace(microsecond=0))
            messages['crawler_time'] = str(datetime.now().replace(microsecond=0))
            messages['intime'] = str(datetime.now().replace(microsecond=0))
            #json.dump(messages,group_info_file,ensure_ascii=False)
            information_list.append(messages)
            message_count = message_count+1
    return Massage_id,message_count,start_time,information_list

'''
初始化每个用户第一次发言时间
'''       
def init_first_time(member_list):

    first_time = {}
    first_time['Auto-response'] = ''
    for member in member_list:
        first_time[member] = ''
    return first_time

'''
初始化每个用户最后发言时间
'''
def init_last_time(member_list):
    last_time = {}
    last_time['Auto-response'] = ''
    for member in member_list:
        last_time[member] = ''
    return last_time


'''
记录第一次发言时间
'''   
def recode_first_time(first_time,user_name,date,true_time):
    if first_time[user_name] == '':
        date1 = datetime.strptime(date,"%a, %b %d")
        formatted_date = date1.strftime("%m-%d")
        first_time[user_name] = '2023'+'-'+str(formatted_date)+' '+str(true_time)
    else:
        return first_time
    return first_time

'''
记录最后一次发消息时间
'''
def recode_last_time(last_time,user_name,date,true_time):
    date1 = datetime.strptime(date,"%a, %b %d")
    formatted_date = date1.strftime("%m-%d")
    last_time[user_name] = '2023'+'-'+str(formatted_date)+' '+str(true_time)
    return last_time

def user_is_excist(user_all_list,user_name):
    
    user_name_flag = False
    if user_name in user_all_list:
        user_name_flag = True
    return user_name_flag


def group_relation_is_excist(relation_all_list,group_number,user_name):
    relation_flag = False
    for object in relation_all_list:
        if user_name == object['user_name'] and group_number == object['group_id']:
            relation_flag = True
            break
    return relation_flag

    



'''
依次遍历div,并从中获取需要的内容
'''
def read_div(div_list,group_number,is_group,group_name,group_user_number,i,url,Massage_id,member_list,user_detail_file,group_detial_file,group_relation_file,group_info_file,user_detial_id,user_relation_id,user_all_list,relation_all_list,group_list,flag,types,time2,number,start_time,information_path,message_count,information_list,group_relation_list,group_detail_list,user_detail_list,timestamp,div_flag,last_message_count,serviceid,save_path,div_count):
    #group_all_information = {}  # json中存入的字典
    first_time = init_first_time(member_list)
    last_time = init_last_time(member_list)
     # 判断用户是否已经存在，若不存在才存储
    user_detial_id,user_all_list,user_detail_list = user_detail(user_detail_file,member_list,user_detial_id,user_all_list,user_detail_list,serviceid)
    if group_number not in group_list:
        group_list.append(group_number)
        flag = init_flag(flag,group_number)
        group_detail_list = group_detail(group_detial_file,i,group_number,group_name,group_user_number,url,group_detail_list,serviceid)
    #sleep_time()
    #start_index = int(flag[group_number])
    #print(div_list)
    if(div_count<len(div_list)):
        div_count=len(div_list)
        last_message_count=0
    if(div_flag==False):
        for div in div_list:
            div_flag =True
            last_message_count=0
            # 这里每一天的聊天记录是一个div，class为position-relative
            #soup = BeautifulSoup(div.get_attribute('innerHTML'),'html.parser')
            # 获取消息发送的时间
            count_loop = 0;
            while(1):
                if(count_loop>=5):
                    date = 'Auto-response'
                    break
                count_loop=count_loop+1
                try:
                    date = div.find_element_by_css_selector('div[class="chatsys-content"]')
                    date = date.get_attribute('textContent').strip()
                    break
                except Exception:
                    continue
            while(1):    
                try:
                    # 获取聊天消息的主体，每一条消息为一个div，但是同一个用户连续发送的消息在一个div中
                    chat_content = div.find_elements_by_css_selector('div[class="chat-content"]')
                    #print(date,chat_content)
                    break
                except Exception:
                    continue
            '''if(start_index>0):
                start_index = start_index-1'''
            #print(Massage_id)
            # 遍历消息主体
            for content_main in chat_content:
                last_message_count = last_message_count+1
                flag[group_number] = int(flag[group_number])+1 
                count_loop = 0
                while(1):
                    if(count_loop>=5):
                        user_name = None
                        break
                    count_loop=count_loop+1
                    try:
                        # 获取用户名称
                        user_name = content_main.find_element_by_css_selector('div[class="chat-header"]')
                        #print(user_name)
                        break
                    except Exception:
                        continue
                while(1):
                    try:
                    
                        data_ids = content_main.find_elements_by_css_selector('div[class="chat-body"],div[class="chat-body more"]')
                        # 获取该用户在该时间段发送的消息
                        content_text_div = content_main.find_elements_by_css_selector('div[class="chat-item-text user-select-text"]')
                        # 获取发送的表情包及图片
                        content_img = content_main.find_elements_by_tag_name('img')
                        # 获取发送的语音
                        voices = content_main.find_elements_by_css_selector('div[class="chat-item-voice-text"]')
                        # 发送消息的具体时间
                        time = content_main.find_elements_by_css_selector('div[class="chat-sub"]')
                        break
                    except Exception:
                        continue

                # 下载音频和图片

                try:
                    download = content_main.find_element_by_xpath('.//a[text()="Download"]') 
                    download.click()
                    sleep_time()
                    filename,file_size = get_download_path()
                    '''sleep_time()
                    filename = os.listdir(download_path)[-1]'''
                except Exception:
                    filename = ''
                    file_size = 0
                user_name,sender_type = user_type(user_name)
                # 同一时间段发送的消息只有一个time，其他为空，所以遍历判断是否有值
                for time1 in time:
                    if time1.text.strip() == '':
                        continue
                    else:
                        true_time = time1.text.strip()
                # 记录第一次发消息时间和最后一次发消息时间
                date= date_switch(date)
                first_time = recode_first_time(first_time,user_name,date,true_time)
                last_time = recode_last_time(last_time,user_name,date,true_time)
                content_list,image_info,voice_info = get_text_img_voice(content_text_div,content_img,voices,filename,file_size,timestamp,save_path)
                # 记录消息ID
                data_id_list = []
                for data_id in data_ids:
                    data_id_list.append(data_id.get_attribute('data-id'))
                
                state = 'run'
                save_information(information_path,start_time,state,Massage_id,user_detial_id,user_relation_id,i)
                Massage_id,message_count,start_time,information_list = group_info(group_info_file,content_list,date,Massage_id,group_number,sender_type,true_time,data_id_list,user_name,types,time2,number,start_time,information_path,message_count,information_list,image_info,voice_info,serviceid)
                
    elif(div_flag==True):  
        for div in div_list[-1:]:
            div_flag =True
            # 这里每一天的聊天记录是一个div，class为position-relative
            #soup = BeautifulSoup(div.get_attribute('innerHTML'),'html.parser')
            # 获取消息发送的时间
            count_loop = 0;
            while(1):
                if(count_loop>=5):
                    date = 'Auto-response'
                    break
                count_loop=count_loop+1
                try:
                    date = div.find_element_by_css_selector('div[class="chatsys-content"]')
                    date = date.get_attribute('textContent').strip()
                    break
                except Exception:
                    continue
            while(1):    
                try:
                    # 获取聊天消息的主体，每一条消息为一个div，但是同一个用户连续发送的消息在一个div中
                    chat_content = div.find_elements_by_css_selector('div[class="chat-content"]')
                    #print(date,chat_content)
                    break
                except Exception:
                    continue
            '''if(start_index>0):
                start_index = start_index-1'''
            #print(Massage_id)
            # 遍历消息主体
            for content_main in chat_content[last_message_count:]:
                last_message_count = last_message_count+1
                flag[group_number] = int(flag[group_number])+1 
                  
                count_loop = 0
                while(1):
                    if(count_loop>=5):
                        user_name = None
                        break
                    count_loop=count_loop+1
                    try:
                        # 获取用户名称
                        user_name = content_main.find_element_by_css_selector('div[class="chat-header"]')
                        #print(user_name)
                        break
                    except Exception:
                        continue
                while(1):
                    try:
                    
                        data_ids = content_main.find_elements_by_css_selector('div[class="chat-body"],div[class="chat-body more"]')
                        # 获取该用户在该时间段发送的消息
                        content_text_div = content_main.find_elements_by_css_selector('div[class="chat-item-text user-select-text"]')
                        # 获取发送的表情包及图片
                        content_img = content_main.find_elements_by_tag_name('img')
                        # 获取发送的语音
                        voices = content_main.find_elements_by_css_selector('div[class="chat-item-voice-text"]')
                        # 发送消息的具体时间
                        time = content_main.find_elements_by_css_selector('div[class="chat-sub"]')
                        break
                    except Exception:
                        continue

                # 下载音频和图片

                try:
                    download = content_main.find_element_by_xpath('.//a[text()="Download"]') 
                    download.click()
                    sleep_time()
                    filename,file_size = get_download_path()
                    '''sleep_time()
                    filename = os.listdir(download_path)[-1]'''
                except Exception:
                    filename = ''
                    file_size = 0
                user_name,sender_type = user_type(user_name)
                # 同一时间段发送的消息只有一个time，其他为空，所以遍历判断是否有值
                for time1 in time:
                    if time1.text.strip() == '':
                        continue
                    else:
                        true_time = time1.text.strip()
                date= date_switch(date)
                # 记录第一次发消息时间和最后一次发消息时间
                first_time = recode_first_time(first_time,user_name,date,true_time)
                last_time = recode_last_time(last_time,user_name,date,true_time)
                content_list,image_info,voice_info = get_text_img_voice(content_text_div,content_img,voices,filename,file_size,timestamp,save_path)
                # 记录消息ID
                data_id_list = []
                for data_id in data_ids:
                    data_id_list.append(data_id.get_attribute('data-id'))
                
                state = 'run'
                save_information(information_path,start_time,state,Massage_id,user_detial_id,user_relation_id,i)
                Massage_id,message_count,start_time,information_list = group_info(group_info_file,content_list,date,Massage_id,group_number,sender_type,true_time,data_id_list,user_name,types,time2,number,start_time,information_path,message_count,information_list,image_info,voice_info,serviceid)
                        
   
    # 判断用户关系是否存在，若不存在则存储
    user_relation_id,relation_all_list,group_relation_list = group_relation(group_relation_file,user_relation_id,group_number,member_list,first_time,last_time,relation_all_list,group_relation_list,serviceid)   
    
    return Massage_id,user_detial_id,user_relation_id,user_all_list,relation_all_list,group_list,flag,message_count,start_time,information_list,group_relation_list,group_detail_list,user_detail_list,last_message_count,div_flag,div_count
           
'''
读取配置文件
'''
def open_config_file(path):
    with open(path,'r',encoding='utf-8') as file:
        config = json.load(file)
    return config


'''
判断是用户还是群聊
'''
def group_user_number_tag(driver,group_user_number_tag):
    # 判断是用户还是群
    if group_user_number_tag == []:
        is_group = 'user'
        group_name_tag = driver.find_element_by_css_selector('h4[class="mb-0 text-truncate"]')
        group_name = group_name_tag.text
        group_user_number = ''
    else:
        is_group = 'group'
        group_name_tag = driver.find_element_by_css_selector('h4[class="mb-0 text-truncate cursor-pointer"]')
        group_name = group_name_tag.text
        group_user_number = group_user_number_tag.text
    return is_group,group_name,group_user_number


def get_download_path():
    """获取系统的默认下载路径"""
    
    #download_path = os.path.expanduser("~\\Downloads")
    files = glob.glob(os.path.expanduser('~/Downloads/*'))

    # 找到最新的文件
    latest_file = max(files, key=os.path.getmtime)

    # 获取最新文件的大小，单位是字节
    file_size = os.path.getsize(latest_file)
    
    
       
    return latest_file,file_size


'''
获取群成员
'''
def get_group_member(driver,group_member):
    group_member.click()
    time.sleep(5)
    #sleep_time()
    while(1):
        try:
            members = driver.find_elements_by_css_selector('h6[class="text-truncate mb-0"]')
            break
        except Exception:
            continue
    member_list = []
    for m in members:
        member_list.append(m.text.strip())
    #sleep_time()
    while(1):
        try:
            close = driver.find_element_by_css_selector('button[class="close"]')
            break
        except Exception:
            continue
        
    close.click()
    return driver,member_list

def init_flag(flag,group_number):
    flag[group_number] = 0
    return flag


def close_file(file_name):
    file_name.close()

def save_information(information_path,start_time,state,massage_id,user_detial_id,user_relation_id,i):
    file = open(information_path,'w',encoding='utf-8')
    information = {}
    information['start time'] = str(start_time)
    information['state'] = state
    information['messages'] = massage_id
    information['users'] = user_detial_id
    information['relations'] = user_relation_id
    information['groups'] = i
    json.dump(information,file,ensure_ascii=False)
    file.close()

def judeg(types,time2,number,start_time,message_id,information_path,message_count):
    end_time = datetime.now().replace(microsecond=0)
    if types == 't':
        if (end_time-start_time).total_seconds() >= int(time2):
            state = 'sleep'
            alter_state(information_path,state)
            #print(state)
            time.sleep(int(number))
            state = 'run'
            alter_state(information_path,state)
            start_time = datetime.now().replace(microsecond=0)
    elif types == 'i':

        if message_count >= int(time2):
            message_count = 0
            state = 'sleep'
            alter_state(information_path,state)
            #print(state)
            #print(type(int(number)))
            time.sleep(int(number))
            state = 'run'
            alter_state(information_path,state)
    #print(message_count,(end_time-start_time).total_seconds())
    return message_count,start_time
    
def alter_state(information_path,state):
    # 读取 JSON 文件
    with open(information_path, 'r') as file:
        data = json.load(file)
    # 修改值
    data['state'] = state
    # 将修改后的对象转换回 JSON 格式
    updated_json = json.dumps(data, indent=4)
    # 将更新后的 JSON 数据写回文件
    with open(information_path, 'w') as file:
        file.write(updated_json)


def main1():
    start_time = datetime.now().replace(microsecond=0)
    url = 'https://developers.line.biz/en/'
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    types = sys.argv[3]
    time2 = sys.argv[4]
    number = sys.argv[5]
    #print(number)
    group_id = sys.argv[6]
    save_path = sys.argv[7]
    
    browser = sys.argv[8]
    
    driver_path = sys.argv[9]
    serviceid = sys.argv[10]

    online = sys.argv[11]
    
    
    user_detial_id = 0
    user_relation_id =0
    flag = {}
    user_all_list = []
    relation_all_list = []
    group_list = []
    
    div_count = 0
    message_count = 0
    
    driver = driver_chat(url,username,password,browser,driver_path)
    information_path = save_path+'state.json'
    
    #group_number = config['group_number']
    Massage_id = 0
    #time_record = []
    div_flag = False
    last_message_count = 0
    
    time.sleep(5)
    while(1):
        try:
            group_user_number = driver.find_elements_by_css_selector('a[class="d-flex w-100 justify-content-center"]')
            break
        except Exception:
            continue
    # 依次遍历每个群聊，并获取其内容
    while (1):
        for i in range(1,len(group_user_number)+1):
            #print(last_message_count)
            #try:
            group = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[1]/div/div[2]/div[2]/div/div['+str(i)+']/a'
            #group = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[1]/div/div[2]/div[2]/div/div['+str(i)+']/a'
            driver,url1 = get_group_url(driver,group)
            driver.get(url1)
            sleep_time()
            group_number = str(url1)[61:]
            if(group_id==group_number):
                
                timestamp = str(int(time.time()))
                if os.path.exists(save_path+'group') ==False:
                    os.makedirs(save_path+'group')
                if os.path.exists(save_path+'group_info') ==False:
                    os.makedirs(save_path+'group_info')
                if os.path.exists(save_path+'relation') ==False:
                    os.makedirs(save_path+'relation')
                if os.path.exists(save_path+'user') ==False:
                    os.makedirs(save_path+'user')
                if os.path.exists(save_path+'image') ==False:
                    os.makedirs(save_path+'image')
                group_detial_path = save_path+'group/'+group_id+'_'+timestamp+'_group.json'
                group_relation_path = save_path+'relation/'+group_id+'_'+timestamp+'_relation.json'
                group_info_path = save_path+'group_info/'+group_id+'_'+timestamp+'_info.json'
                user_detail_path = save_path+'user/'+group_id+'_'+timestamp+'_user.json'
                
                user_detail_file = create_file(user_detail_path)
                group_detial_file = create_file(group_detial_path)
                group_relation_file = create_file(group_relation_path)
                group_info_file = create_file(group_info_path)
                information_list = []
                
                group_relation_list = []
                
                group_detail_list = []
                
                user_detail_list =[]
                
                group_user_number_tag_value = driver.find_element_by_css_selector('span[class="cursor-pointer"]')
                group_member = driver.find_element_by_css_selector('div[class="avatar avatar-xs avatar-initials rounded-circle bg-secondary text-white"]')
                #sleep_time()
                driver,member_list = get_group_member(driver,group_member)
                is_group,group_name,group_user_number =  group_user_number_tag(driver,group_user_number_tag_value)
                #sleep_time()
                
                div_list = get_div(driver,url1)
                #print(len(div_list))
                Massage_id,user_detial_id,user_relation_id,user_all_list,relation_all_list,group_list,flag,message_count,start_time, information_list,group_relation_list,group_detail_list,user_detail_list,last_message_count,div_flag,div_count = read_div(div_list,group_number,is_group,group_name,group_user_number,i,url1,Massage_id,member_list,user_detail_file,group_detial_file,group_relation_file,group_info_file,user_detial_id,user_relation_id,user_all_list,relation_all_list,group_list,flag,types,time2,number,start_time,information_path,message_count,information_list,group_relation_list,group_detail_list,user_detail_list,timestamp,div_flag,last_message_count,serviceid,save_path,div_count)
                
                #print(group_detail_list1)
                json.dump(information_list,group_info_file,ensure_ascii=False)
                json.dump(group_relation_list,group_relation_file,ensure_ascii=False)
                json.dump(group_detail_list,group_detial_file,ensure_ascii=False)
                json.dump(user_detail_list,user_detail_file,ensure_ascii=False)
                state = 'run'
                save_information(information_path,start_time,state,Massage_id,user_detial_id,user_relation_id,i)
                time.sleep(int(number))
                close_file(user_detail_file)
                close_file(group_detial_file)
                close_file(group_relation_file)
                close_file(group_info_file)
            else:
                continue
            
           
        time.sleep(int(number))
    quit(driver)
            
            




'''
程序入口
'''
if __name__ == '__main__':
    main1()
    
