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
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#


def getmd5(string):
    md5 = hashlib.md5()
    md5.update(string.encode())
    md5res = md5.hexdigest()
    return md5res
#


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
}
# 命令行参数 =  end  =

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
sleep(2)
driver.find_element(By.XPATH, './/span[@data-testid=\"log-in-btn\"]').click()
WebDriverWait(driver, 5, 0.5).until(
    EC.presence_of_element_located((By.ID, "email"))
).send_keys(email)
WebDriverWait(driver, 5, 0.5).until(
    EC.presence_of_element_located((By.ID, "password"))
).send_keys(password)
driver.find_element(By.XPATH, './/button[@data-testid=\"submit-btn\"]').click()
# driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[2]/div/div/form/div[3]/button').click()
tmp = 1
sleep(5)
while len(driver.find_elements(By.ID, 'ember30')) <= 0:
    print(f'sleep ... wait for login {tmp}')
    sleep(1)
    tmp += 1
# while driver.find_elements(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div/form/div[3]/button'):
#     print(f'sleep ... wait for login {tmp}')
#     sleep(1)
#     tmp += 1
#
title = argv['group'].split('/')[-1]

num = 0  # 用于计数
messages = {title: []}
comment = {title: []}
user = {title: {}}
allMessagePostId = []
allCommentPostId = []
allUserUrl = []
oneLoopUserUrl = []
current_window = ''
user_window = ''
state = {
    'start_time': strftime("%Y-%m-%d %H:%M:%S", localtime()),
    'state': 'run',
    'group': title,
    'messages': 0,
    'comments': 0,
    'users': 0,
}
while(1):
    start_time = time.time()  # 采集开始时间
    sleep(3)
    if current_window:
        oneLoopUserUrl = []
        driver.switch_to.window(current_window)
        sleep(1)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)  # 翻页
    div_element = driver.find_element(By.ID, 'ember30')  # 所有message的父div
    sonDiv_eles = div_element.find_elements(By.XPATH, "./*")  # 父div下的子div
    tmp = 0
    for div in sonDiv_eles[::-1]:
        tmp += 1
        state['messages'] += 1
        oneMessage = {
            'user_url': '',
            'md5': '',
            'post_id': '',
            'pubtime': '',
            'content': [],
            'share': 0,
            'emoji': 0,
            'crawler_time': strftime("%Y-%m-%d %H:%M:%S", localtime()),
            'user_name': ''
        }
        try:
            for i in div.find_elements(By.TAG_NAME, 'div'):
                if 'post_header' in i.get_attribute('class') and 'items-start' in i.get_attribute('class'):  # 获取postid
                    oneMessage['post_id'] = i.get_attribute('data-postid')
                    break
            oneMessage['user_url'] = div.find_element(By.XPATH, ".//a[@class=\"ember-view c-profile-link d-inline-flex post-author_name\"]").get_attribute('href')
            oneMessage['md5'] = getmd5(oneMessage['user_url'])
            oneMessage['pubtime'] = div.find_element(By.XPATH, ".//time[@class=\"timeago\"]").get_attribute('datetime')
            oneMessage['user_name'] = div.find_element(By.XPATH, ".//span[@class=\"items-center h-trim\"]").text
            #
            #
            #
            # if oneMessage['post_id'] not in allMessagePostId:
            #     allMessagePostId.append(oneMessage['post_id'])
            if oneMessage['user_url'] not in allUserUrl:
                allUserUrl.append(oneMessage['user_url'])
                oneLoopUserUrl.append(oneMessage['user_url'])
            #
            #
            #
            #
            #
            # 文字 = start =
            p_content = div.find_elements(By.XPATH, ".//p[@dir=\"auto\"]")
            for i in p_content:
                oneMessage['content'].append({'p': i.text})
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
                    oneMessage['content'].append({'img': i.get_attribute('src')})
            # 图片 = end =
            # 视频 = start =
            video_content = div.find_elements(By.XPATH, ".//video")
            for i in video_content:
                oneMessage['content'].append({'video': i.get_attribute('src')})
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
        except Exception as e:
            print('group message error: ', e)
        # 评论 = start =
        try:
            alldiv = div.find_elements(By.XPATH, ".//div")
            for commentDiv in alldiv:
                if 'c-mw-comments-table' in commentDiv.get_attribute('class') and 'comments-table_wrapper' in commentDiv.get_attribute('class'):
                    commentallSonDiv = commentDiv.find_elements(By.TAG_NAME, "div")
                    for oneCom in commentallSonDiv:
                        if 'c-mw-comment comment' in oneCom.get_attribute('class') and 'not-reply' in oneCom.get_attribute('class'):
                            state['comments'] += 1
                            oneComment = {
                                'message_id': oneMessage['post_id'],
                                'mblog_info_md5': getmd5(str(oneMessage['post_id'])),
                                'comment_id': '',
                                'user_url': '',
                                'pubtime': '',
                                'content': [],
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
                            # if oneComment['comment_id'] not in allCommentPostId:
                            #     allCommentPostId.append(oneComment['comment_id'])
                            if oneComment['user_name'] not in allUserUrl:
                                allUserUrl.append(oneComment['user_url'])
                                oneLoopUserUrl.append(oneComment['user_url'])
                            #
                            #
                            #
                            #
                            #
                            oneComment['pubtime'] = sonCommentDiv.find_element(By.XPATH, ".//time[@class=\"timeago\"]").get_attribute('datetime')
                            # 文字 = start =
                            p_content = sonCommentDiv.find_elements(By.XPATH, ".//p[@dir=\"auto\"]")
                            for i in p_content:
                                oneComment['content'].append({'p': i.text})
                            # 文字 = end =
                            # 链接 = start =
                            a_content = sonCommentDiv.find_elements(By.XPATH, ".//a[@class=\"group-color\"]")
                            for i in a_content:
                                oneComment['content'].append({'a': i.get_attribute('href')})
                            # 链接 = end =
                            # 图片 = start =
                            img_content = sonCommentDiv.find_elements(By.XPATH, ".//img")
                            for i in img_content:
                                if 'photo/profile/150x150' not in i.get_attribute('src'):
                                    oneComment['content'].append({'img': i.get_attribute('src')})
                            # 图片 = end =
                            # 视频 = start =
                            video_content = sonCommentDiv.find_elements(By.XPATH, ".//video")
                            for i in video_content:
                                oneComment['content'].append({'video': i.get_attribute('src')})
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
                                comment[title].append(oneComment)
                                # print('comment: ', oneComment)
                                stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
                                stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
                                stateF.close()
        except Exception as e:
            print('comment error: ', e)
        # 评论 =  end  =
        if oneMessage['post_id'] not in allMessagePostId:
            allMessagePostId.append(oneMessage['post_id'])
            messages[title].append(oneMessage)
            # newuser.append(oneMessage)
            # print('messages: ', oneMessage)
            num += 1
            if argv['type'] == 'i':
                if num >= argv['type_data']:
                    state['state'] = 'sleep'
                    stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
                    stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
                    stateF.close()
                    sleep(argv['interval'])
                    state['state'] = 'run'
                    stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
                    stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
                    stateF.close()
                    num = 0
        else:
            break
        if tmp == 10:
            break
    #
    # 若满足条件则休眠 = start =
    end_time = time.time()  # 采集结束时间
    if argv['type'] == 't':
        if end_time - start_time >= argv['type_data']:
            sleep(argv['interval'])
            state['state'] = 'sleep'
            stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
            stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
            stateF.close()
            sleep(argv['interval'])
            state['state'] = 'run'
            stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
            stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
            stateF.close()
            start_time = time.time()
    # 若满足条件则休眠 = end =
    # 用户信息 = start =
    try:
        if oneLoopUserUrl:
            current_window = driver.current_window_handle  # 获取当前窗口句柄
            if len(driver.window_handles) <= 1:
                # 跳转新窗口
                driver.execute_script("window.open('', '_blank')")
                user_window = driver.window_handles[-1]
            driver.switch_to.window(user_window)
            for iuser in oneLoopUserUrl:
                driver.get(iuser)
                sleep(3)
                # 在新窗口中爬取数据
                # 跳转
                mainProfile = driver.find_elements(By.XPATH, "//*[@data-testid=\"go-to-main-profile-link\"]")
                userUrl = mainProfile[0].get_attribute('href')
                # if userUrl in oneLoopUserUrl:
                #     pass
                # # if userUrl in user[title].keys():
                # #     if iuser['post_id'] not in user[title][userUrl]['post_id']:
                # #         user[title][userUrl]['post_id'].append(iuser['post_id'])
                # #         print('same user: ', userUrl)
                # else:
                # oneLoopUserUrl.append(userUrl)
                state['users'] += 1
                oneUser = {
                    'user_url': userUrl,
                    'user_character_url': userUrl,
                    'md5': getmd5(userUrl),
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
                oneUser['since_time'] = driver.find_element(By.XPATH, "//*[@class=\"f-14t mb-16 break-word align-content-m\"]").get_attribute('title')
                for span in driver.find_elements(By.TAG_NAME, 'span'):
                    if 'stats-value' in span.get_attribute('class') or 'stats-name' in span.get_attribute('class'):
                        oneUser['description'].append(span.text)
                # userDiv = driver.find_elements(By.TAG_NAME, 'div')
                # for i in userDiv:
                #     if 'c-field-editable' in i.get_attribute('class') and 'field-editable' in i.get_attribute('class'):
                #         itemtitle = i.find_elements(By.XPATH, ".//span[@class=\"info-label group-color\"]")
                #         if itemtitle:
                #             itemtitle = itemtitle[0].text
                #             value = i.find_elements(By.XPATH, ".//span[@data-testid=\"user-answer-value\"]")
                #             if value:
                #                 oneUser['description'].append({str(itemtitle): value[0].text})
                user[title][userUrl] = oneUser
                print('user: ', oneUser)
                stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
                stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
                stateF.close()
                # 若满足条件则休眠 = start =
                end_time = time.time()  # 采集结束时间
                if argv['type'] == 't':
                    if end_time - start_time >= argv['type_data']:
                        state['state'] = 'sleep'
                        stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
                        stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
                        stateF.close()
                        sleep(argv['interval'])
                        state['state'] = 'run'
                        stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
                        stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
                        stateF.close()
                        start_time = time.time()
                # 若满足条件则休眠 = end =
    except Exception as e:
        print('user error: ', e)

    # 用户信息 =  end  =
    saveFile = open(f'{argv["save_path"]}/messages.json', 'w', encoding='utf-8')
    saveFile.write(json.dumps(messages, ensure_ascii=False, indent=4))
    saveFile.close()
    saveFile = open(f'{argv["save_path"]}/comments.json', 'w', encoding='utf-8')
    saveFile.write(json.dumps(comment, ensure_ascii=False, indent=4))
    saveFile.close()
    saveFile = open(f'{argv["save_path"]}/user.json', 'w', encoding='utf-8')
    saveFile.write(json.dumps(user, ensure_ascii=False, indent=4))
    saveFile.close()
    # 若满足条件则休眠 = start =
    end_time = time.time()  # 采集结束时间w
    if argv['type'] == 't':
        if end_time - start_time >= argv['type_data']:
            state['state'] = 'sleep'
            stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
            stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
            stateF.close()
            sleep(argv['interval'])
            state['state'] = 'run'
            stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
            stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
            stateF.close()
            start_time = time.time()
    if argv['type'] == 'i':
        if num >= argv['type_data']:
            state['state'] = 'sleep'
            stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
            stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
            stateF.close()
            sleep(argv['interval'])
            state['state'] = 'run'
            stateF = open(f'{argv["save_path"]}/state.json', 'w', encoding='utf-8')
            stateF.write(json.dumps(state, ensure_ascii=False, indent=4))
            stateF.close()
    # 若满足条件则休眠 = end =
