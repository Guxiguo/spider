'''
Author: hc J
Date: 2023-05-05 16:41:58
LastEditTime: 2023-07-26 13:44:31
Description: file content
'''
import hashlib
import json
import re
import sys
import time
from time import gmtime, localtime, sleep, strftime
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests

# 命令行参数 = start =
argv = {
    'fileName': sys.argv[0],
    'email': sys.argv[1],
    'password': sys.argv[2],
    'type': sys.argv[3],
    'type_data': int(sys.argv[4]),
    'interval': int(sys.argv[5]),
    'group': sys.argv[6],
    'save_path': sys.argv[7],
    'browser': sys.argv[8],
    'browser_data': sys.argv[9],
    'serviceid': sys.argv[10],
    'online': sys.argv[11],
}
proxies = {
    "http": "http://127.0.0.1:7890"  # WARNING: 修改代理链接
}
# 命令行参数 =  end  =
title = argv['group'].split('/')[-1]
messages = []
comment = []
user = []
save_path = f'{argv["save_path"]}'
if not os.path.exists(save_path):
    os.makedirs(save_path)
#
round = 1  # 爬虫轮次计数
num = 0  # 全局变量-用于计数

allMessagePostId = []  # 全部Message发送ID，用于去重
allimage = []  # 全部image名字，用于去重
allCommentPostId = []  # 全部Comment发送ID，用于去重
allUserUrl = []  # 全部User的Url，用于去重
oneLoopUserUrl = []
current_window = ''
user_window = ''
start_time = 0  # 全局变量-开始时间


def getmd5(string):
    """_summary_
    进行md5转换

    Args:
        string (_str_): 输入字符串

    Returns:
        _str_: 转换后的md5
    """
    md5 = hashlib.md5()
    md5.update(string.encode())
    md5res = md5.hexdigest()
    return md5res
#


# def item_check():
#     """_summary_
#     检查条数-以决定是否停止爬虫
#     """
#     global num
#     if num >= argv['type_data']:
#         state['state'] = 'sleep'
#         stateF = open(f'{save_path}/state.json', 'w', encoding='utf-8')
#         stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
#         stateF.close()
#         sleep(argv['interval'])
#         state['state'] = 'run'
#         stateF = open(f'{save_path}/state.json', 'w', encoding='utf-8')
#         stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
#         stateF.close()
#         num = 0
#         return True
#     return False


def time_check():
    """_summary_
    检查时间-以决定是否停止爬虫
    """
    global start_time
    global round
    end_time = time.time()  # 采集结束时间
    if end_time - start_time >= argv['type_data']:
        # state['state'] = 'sleep'
        # stateF = open(f'{save_path}/state.json', 'w', encoding='utf-8')
        # stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
        # stateF.close()
        sleep(argv['interval'])
        # state['state'] = 'run'
        # stateF = open(f'{save_path}/state.json', 'w', encoding='utf-8')
        # stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
        # stateF.close()
        start_time = time.time()
        save_data()
        round += 1
        return True
    return False


def save_data():
    """_summary_
    用于写入数据
    """
    global messages
    global comment
    global user
    # 检查文件夹是否已存在
    messages_folder_path = f'{save_path}/messages'
    comments_folder_path = f'{save_path}/comments'
    user_folder_path = f'{save_path}/user'
    if not os.path.exists(messages_folder_path):
        os.makedirs(messages_folder_path)
    if not os.path.exists(comments_folder_path):
        os.makedirs(comments_folder_path)
    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)
    timestamp = str(int(time.time()))
    saveFile = open(f'{messages_folder_path}/messages_{timestamp}.jsons', 'w', encoding='utf-8')
    saveFile.write(json.dumps(messages, ensure_ascii=False, indent=4))
    saveFile.close()
    saveFile = open(f'{comments_folder_path}/comments_{timestamp}.jsons', 'w', encoding='utf-8')
    saveFile.write(json.dumps(comment, ensure_ascii=False, indent=4))
    saveFile.close()
    saveFile = open(f'{user_folder_path}/user_{timestamp}.jsons', 'w', encoding='utf-8')
    saveFile.write(json.dumps(user, ensure_ascii=False, indent=4))
    saveFile.close()
    os.rename(f'{messages_folder_path}/messages_{timestamp}.jsons', f'{messages_folder_path}/messages_{timestamp}.json')
    os.rename(f'{comments_folder_path}/comments_{timestamp}.jsons', f'{comments_folder_path}/comments_{timestamp}.json')
    os.rename(f'{user_folder_path}/user_{timestamp}.jsons', f'{user_folder_path}/user_{timestamp}.json')
    messages = []
    comment = []
    user = []

'''def save_data():
    """_summary_
    用于写入数据
    """
    global messages
    global comment
    global user
    # 检查文件夹是否已存在
    messages_folder_path = f'{save_path}/messages'
    comments_folder_path = f'{save_path}/comments'
    user_folder_path = f'{save_path}/user'
    if not os.path.exists(messages_folder_path):
        os.makedirs(messages_folder_path)
    if not os.path.exists(comments_folder_path):
        os.makedirs(comments_folder_path)
    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)
    saveFile = open(f'{messages_folder_path}/messages_{round}.json', 'w', encoding='utf-8')
    saveFile.write(json.dumps(messages, ensure_ascii=False, indent=4))
    saveFile.close()
    saveFile = open(f'{comments_folder_path}/comments_{round}.json', 'w', encoding='utf-8')
    saveFile.write(json.dumps(comment, ensure_ascii=False, indent=4))
    saveFile.close()
    saveFile = open(f'{user_folder_path}/user_{round}.json', 'w', encoding='utf-8')
    saveFile.write(json.dumps(user, ensure_ascii=False, indent=4))
    saveFile.close()
    messages = []
    comment = []
    user = []'''


def save_img(imgUrl):
    if argv['type'] == 't':
        time_check()
    try:
        imgUrl = imgUrl.replace("https://", "http://")
        if imgUrl not in allimage:
            imgDict = {
                "type": "jpg",
                "url": imgUrl,
                "path": "",
                "name": "",
                "length": 0,
                "download_datetime": strftime("%Y-%m-%d %H:%M:%S", localtime())
            }
            img_save_path = f'{save_path}/img'
            if not os.path.exists(img_save_path):
                os.makedirs(img_save_path)
            # try:
            # 获取图片内容
            response = requests.get(imgUrl, stream=True, proxies=proxies)
            response.raise_for_status()

            # 计算图片的哈希值
            img_hash = hashlib.sha256(response.content).hexdigest()

            # 检查是否已经有相同哈希值的图片
            for existing_file in os.listdir(img_save_path):
                existing_file_path = os.path.join(img_save_path, existing_file)
                if os.path.isfile(existing_file_path):
                    with open(existing_file_path, 'rb') as f:
                        existing_file_hash = hashlib.sha256(f.read()).hexdigest()
                    if existing_file_hash == img_hash:
                        # print(f"图片 {imgUrl} 与已存在的图片 {existing_file} 重复，不再保存。")
                        return
            # 从响应的 Content-Type 中确定文件扩展名
            content_type = response.headers.get('Content-Type')
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            else:
                ext = ''  # 或者可以选择一个默认的扩展名，例如 '.jpg'

            # 如果图片不重复，保存图片
            img_filename = os.path.join(img_save_path, f"{img_hash}{ext}")
            with open(img_filename, 'wb') as f:
                f.write(response.content)
            imgDict['path'] = img_filename
            imgDict['name'] = f"{img_hash}{ext}"
            imgDict['length'] = os.path.getsize(img_filename)
            allimage.append(imgUrl)
            return imgDict
    except Exception:
        pass
        # print(f"保存图像错误：{e}")
    return None

def convert_time_format(time_str):
    # 将原始时间字符串解析为datetime对象
    dt_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    # 将datetime对象格式化为所需的格式
    return dt_obj.strftime("%Y-%m-%d %H:%M:%S")


email = argv['email']
password = argv['password']
driver = ''
if argv['browser'] == 'edge':
    driver = webdriver.Edge(argv['browser_data'])
elif argv['browser'] == 'chrome':
    driver = webdriver.Chrome(argv['browser_data'])
driver.set_window_size(1300, 900)
# driver.get("https://mewe.com/login")
driver.get(argv['group'])
while len(driver.find_elements(By.XPATH, './/span[@data-testid=\"log-in-btn\"]')) <= 0:
    print('sleep ... wait for web')
    sleep(1)
sleep(3)
driver.find_element(By.XPATH, './/span[@data-testid=\"log-in-btn\"]').click()
WebDriverWait(driver, 5, 0.5).until(
    EC.presence_of_element_located((By.ID, "email"))
).send_keys(email)
WebDriverWait(driver, 5, 0.5).until(
    EC.presence_of_element_located((By.ID, "password"))
).send_keys(password)
driver.find_element(By.XPATH, './/button[@data-testid=\"submit-btn\"]').click()
tmp = 1
sleep(5)
while len(driver.find_elements(By.ID, 'ember3')) <= 0:  # 用于检测已完成登录  # WARNING: 每次迭代需修改
    print(f'sleep ... wait for login {tmp}')
    sleep(1)
    tmp += 1
#

# state = {
#     'start_time': strftime("%Y-%m-%d %H:%M:%S", localtime()),
#     'state': 'run',
#     'group': title,
#     'messages': 0,
#     'comments': 0,
#     'users': 0,
# }
start_time = time.time()  # 采集开始时间
while (True):
    # folder_path = f'{save_path}/{round}'
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)
    if argv['type'] == 't':
        time_check()
    # if argv['type'] == 'i':
    #     item_check()
    if current_window:
        oneLoopUserUrl = []
        driver.switch_to.window(current_window)
        sleep(1)
    driver.get(argv['group'])
    sleep(3)
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)  # 翻页
    div_element = driver.find_element(By.ID, 'ember29')  # 所有message的父div # WARNING: 每次迭代需修改
    sonDiv_eles = div_element.find_elements(By.XPATH, "./*")  # 父div下的子div
    tmp = 0
    for div in sonDiv_eles[::-1]:
        tmp += 1
        # state['messages'] += 1
        oneMessage = {
            'serviceid': argv['serviceid'],
            'user_url': '',
            'md5': '',
            'post_id': '',
            'pubtime': '',
            'content': '',
            'image_info': [],
            'share': 0,
            'emoji': 0,
            'crawler_time': strftime("%Y-%m-%d %H:%M:%S", localtime()),
            'user_name': ''
        }
        try:  # 消息-try
            for i in div.find_elements(By.TAG_NAME, 'div'):
                if 'post_header' in i.get_attribute('class') and 'items-start' in i.get_attribute('class'):  # 获取postid
                    oneMessage['post_id'] = i.get_attribute('data-postid')
                    break
            oneMessage['user_url'] = div.find_element(By.XPATH, ".//a[@class=\"ember-view c-profile-link d-inline-flex post-author_name\"]").get_attribute('href')
            oneMessage['md5'] = getmd5(oneMessage['user_url']+oneMessage['post_id'])
            oneMessage['pubtime'] = convert_time_format(div.find_element(By.XPATH, ".//time[@class=\"timeago\"]").get_attribute('datetime'))
            oneMessage['user_name'] = div.find_element(By.XPATH, ".//span[@class=\"items-center h-trim\"]").text
            #
            #
            #
            if oneMessage['user_url'] not in allUserUrl:  # 获取用户url
                allUserUrl.append(oneMessage['user_url'])
                oneLoopUserUrl.append(oneMessage['user_url'])
            #
            #
            #
            # 文字 = start =
            p_content = div.find_elements(By.XPATH, ".//p[@dir=\"auto\"]")
            for i in p_content:
                oneMessage['content'] += f'\n{i.text}'
            # 文字 = end =
                # 链接 = start = 暂时废弃
                # a_content = div.find_elements(By.XPATH, ".//a[@class=\"group-color\"]")
                # for i in a_content:
                #     oneMessage['content'].append({'a': i.get_attribute('href')})
                # 链接 = end =
            # 图片 = start =
            img_content = div.find_elements(By.XPATH, ".//img")
            for i in img_content:
                if 'photo/profile/150x150' not in i.get_attribute('src'):
                    oneMessage['content'] += f'\n{i.get_attribute("src")}'
                    img_dict = save_img(i.get_attribute('src'))
                    if img_dict:
                        oneMessage['image_info'].append(img_dict)
            # 图片 = end =
            # 视频 = start =
            video_content = div.find_elements(By.XPATH, ".//video")
            for i in video_content:
                oneMessage['content'] += f'\n{i.get_attribute("src")}'
                # oneMessage['content'].append({'video': i.get_attribute('src')})
            # 视频 = end =
            # 分享 = start =
            share = div.find_element(By.XPATH, ".//div[@class=\"dropdown-positioner no-wrap\"]")
            number = re.findall(r'\d+', share.text)
            if number:
                oneMessage['share'] = int(number[0])
            # 分享 =  end  =
            # emoji = start =
            emoji = div.find_elements(By.XPATH, ".//li[@data-testid=\"postbar-emoji\"]")
            for i in emoji:
                span = i.find_elements(By.TAG_NAME, 'span')
                for j in span:
                    if j.get_attribute('class') != 'emoji':
                        oneMessage['emoji'] += 1
            # emoji =  end  =
        except Exception:  # 消息-except
            # print('group message error: ', e)
            pass
        # 评论 = start =
        try:  # 评论-try
            alldiv = div.find_elements(By.XPATH, ".//div")
            for commentDiv in alldiv:
                if 'c-mw-comments-table' in commentDiv.get_attribute('class') and 'comments-table_wrapper' in commentDiv.get_attribute('class') and 'len-0' not in commentDiv.get_attribute('class'):
                    commentallSonDiv = commentDiv.find_elements(By.TAG_NAME, "div")
                    for oneCom in commentallSonDiv:
                        if 'c-mw-comment comment' in oneCom.get_attribute('class') and 'not-reply' in oneCom.get_attribute('class'):
                            # state['comments'] += 1
                            oneComment = {
                                'serviceid': argv['serviceid'],
                                'message_id': oneMessage['post_id'],
                                'mblog_info_md5': getmd5(str(oneMessage['post_id'])),
                                'comment_id': '',
                                'user_url': '',
                                'pubtime': '',
                                'content': '',
                                'image_info': [],
                                'share': 0,
                                'emoji': 0,
                                'crawler_time': strftime("%Y-%m-%d %H:%M:%S", localtime()),
                                'user_name': '',
                            }
                            sonCommentDiv = oneCom
                            oneComment['comment_id'] = sonCommentDiv.find_element(By.XPATH, ".//div[@class=\"comment_header\"]").get_attribute('data-commentid')
                            oneComment['user_name'] = sonCommentDiv.find_element(By.XPATH, ".//span[@class=\"items-center h-trim\"]").text
                            oneComment['user_url'] = sonCommentDiv.find_element(By.XPATH, ".//a[@class=\"ember-view c-profile-link d-inline-flex post-author_name\"]").get_attribute('href')
                            #
                            #
                            #
                            if oneComment['user_url'] not in allUserUrl:  # 获取用户url
                                allUserUrl.append(oneComment['user_url'])
                                oneLoopUserUrl.append(oneComment['user_url'])
                            #
                            #
                            #
                            oneComment['pubtime'] = convert_time_format(sonCommentDiv.find_element(By.XPATH, ".//time[@class=\"timeago\"]").get_attribute('datetime'))
                            # 文字 = start =
                            p_content = sonCommentDiv.find_elements(By.XPATH, ".//p[@dir=\"auto\"]")
                            for i in p_content:
                                oneComment['content'] += f'\n{i.text}'
                            # 文字 = end =
                            # 链接 = start =
                            a_content = sonCommentDiv.find_elements(By.XPATH, ".//a[@class=\"group-color\"]")
                            for i in a_content:
                                # oneComment['content'].append({'a': i.get_attribute('href')})
                                oneComment['content'] += f'\n{i.get_attribute("src")}'
                            # 链接 = end =
                            # 图片 = start =
                            img_content = sonCommentDiv.find_elements(By.XPATH, ".//img")
                            for i in img_content:
                                if 'photo/profile/150x150' not in i.get_attribute('src'):
                                    oneComment['content'] += f'\n{i.get_attribute("src")}'
                                    # oneComment['content'].append({'img': i.get_attribute('src')})
                                    img_dict = save_img(i.get_attribute('src'))
                                    if img_dict:
                                        oneComment['image_info'].append(img_dict)
                            # 图片 = end =
                            # 视频 = start =
                            video_content = sonCommentDiv.find_elements(By.XPATH, ".//video")
                            for i in video_content:
                                # oneComment['content'].append({'video': i.get_attribute('src')})
                                oneComment['content'] += f'\n{i.get_attribute("src")}'
                            # 视频 = end =
                            # # 分享 = start =
                            # share = sonCommentDiv.find_elements(By.XPATH, ".//span[@data-testid=\"reply-btn\"]")
                            # for i in share:
                            #     number = re.findall(r'\d+', i.text)
                            #     if number:
                            #         oneComment['share'] = int(number[0])
                            # # 分享 =  end  =
                            # emoji = start =
                            emoji = sonCommentDiv.find_elements(By.XPATH, ".//li")
                            for i in emoji:
                                span = i.find_elements(By.TAG_NAME, 'span')
                                for j in span:
                                    if j.get_attribute('class') != 'emoji' and j.get_attribute('class') != 'all-tab f-12 f-l font-2 mr-7 py-8 cursor-pointer':
                                        oneComment['emoji'] += 1
                            # emoji =  end  =
                            if oneComment['comment_id'] not in allCommentPostId:
                                allCommentPostId.append(oneComment['comment_id'])
                                comment.append(oneComment)
                                if argv['type'] == 't':
                                    time_check()
                                # print('comment: ', oneComment)
                                # stateF = open(f'{save_path}/state.json', 'w', encoding='utf-8')
                                # stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
                                # stateF.close()
        except Exception:  # 评论-except
            # print('comment error: ', e)
            pass
        # 评论 =  end  =
        # allMessagePostId.append(oneMessage['post_id'])
        # messages[title].append(oneMessage)
        # num += 1
        if argv['type'] == 't':
            time_check()
        if oneMessage['post_id'] not in allMessagePostId:
            allMessagePostId.append(oneMessage['post_id'])
            messages.append(oneMessage)
            num += 1
            if argv['type'] == 't':
                time_check()
            # if argv['type'] == 'i':
            #     item_check()
        if tmp == 10:
            break
    #
    # 若满足条件则休眠 = start =

    # 若满足条件则休眠 = end =
    # 用户信息 = start =
    try:  # 用户-try
        if oneLoopUserUrl:
            current_window = driver.current_window_handle  # 获取当前窗口句柄
            if len(driver.window_handles) <= 1:
                # 跳转新窗口
                driver.execute_script("window.open('', '_blank')")
                user_window = driver.window_handles[-1]
            driver.switch_to.window(user_window)
            for iuser in oneLoopUserUrl:
                try:  # 用户2-try
                    driver.get(iuser)
                    sleep(3)
                    # 在新窗口中爬取数据
                    mainProfile = driver.find_elements(By.XPATH, "//*[@id=\"ember22\"]")  # WARNING: 每次迭代需修改
                    userUrl = mainProfile[0].get_attribute('href')
                    # state['users'] += 1
                    oneUser = {
                        'serviceid': argv['serviceid'],
                        'user_url': userUrl,
                        'user_character_url': userUrl,
                        'md5': getmd5(userUrl),
                        'group_id':title,
                        'user_name': '',
                        'since_time': '',
                        'description': [],
                        # 'post_id': [],
                        'crawler_time': strftime("%Y-%m-%d %H:%M:%S", localtime()),
                    }
                    # oneUser['post_id'].append(iuser['post_id'])
                    driver.get(userUrl)
                    sleep(3)
                    oneUser['user_name'] = driver.find_element(By.XPATH, "//*[@data-testid=\"my-profile-name\"]").text
                    oneUser['since_time'] = driver.find_element(By.XPATH, "//*[@class=\"f-14t mb-16 break-word\"]").get_attribute('title')
                    for span in driver.find_elements(By.TAG_NAME, 'span'):
                        if 'stats-value' in span.get_attribute('class') or 'stats-name' in span.get_attribute('class'):
                            oneUser['description'].append(span.text)
                    #
                    user.append(oneUser)
                    print('user: ', oneUser)
                    # stateF = open(f'{save_path}/state.json', 'w', encoding='utf-8')
                    # stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
                    # stateF.close()
                    # 若满足条件则休眠 = start =
                    if argv['type'] == 't':
                        time_check()
                    # 若满足条件则休眠 = end =
                except Exception as e:  # 用户-except
                    print('user error2: ', e)
                    if argv['type'] == 't':
                        time_check()
    except Exception as e:  # 用户-except
        print('user error: ', e)
        # pass
    # 用户信息 =  end  =
