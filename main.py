import re
import os
from sendNotify import send
import time
import requests
from bs4 import BeautifulSoup
List = []

def main(laravel_session): #参数为cookie里的laravel_session 自行抓包获取
    s = requests.session()  # 创建会话
    loginurl = "https://service.jiangsugqt.org/youth/lesson"  # 江苏省青年大学习接口

    # 构造请求头
    headers = {
        # 'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x18001234) NetType/WIFI Language/zh_CN",
        'Cookie': "laravel_session="+laravel_session # 抓包获取
        #"laravel_session=ZBps3sXJdrXmeeciQ0LXCnoq0pBNujjmzOXaWpnQ"
        # 'Cookie':"8rAucTd84mpMLxilmCjeWO08rbtC7opDnrwo9YvJ"
        # 8rAucTd84mpMLxilmCjeWO08rbtC7opDnrwo9YvJ 周良宇 003831928
        # esX66JF8QROB5yx89KMpFBwnF2eNrVUbSpx8FVUX 姜宇 008629871
        # vf6yckniFRDqepGNSaSD2SN4IhCv1wj6LPPqfh74 李靖翔
    }
    login = s.get(url=loginurl, headers=headers)  # 登录
    # print(login.text)
    login_soup = BeautifulSoup(login.text, 'html.parser')  # 解析信息确认页面
    # print(soup.select(".confirm-user-info"))
    userinfo = login_soup.select(".confirm-user-info p")  # 找到用户信息div 课程姓名编号单位
    # print(userinfo)

    dict = {}  # 构建用户信息字典

    for i in userinfo:
        # print(i)
        info_soup = BeautifulSoup(str(i), 'html.parser')  # 分布解析课程姓名编号单位信息
        # print(info_soup.get_text())
        item = info_soup.get_text()  # 用户信息
        # print(item[:4],item[5:])
        dict[item[:4]] = item[5:]
    token = re.findall(r'var token ?= ?"(.*?)"', login.text)  # 获取js里的token
    lesson_id = re.findall(r"'lesson_id':(.*)", login.text)  # 获取js里的token
    # print("token:%s"%token[0])
    # print("lesson_id:%s"%lesson_id[0])
    dict['token'] = token[0]
    dict['lesson_id'] = lesson_id[0]


    #print(dict)
    List.append(f"{dict}")
    confirmurl = "https://service.jiangsugqt.org/youth/lesson/confirm"
    params = {
        "_token": token[0],
        "lesson_id": lesson_id[0]
    }
    res2 = s.post(url=confirmurl, params=params)
    # print(res2.text)
    res = res2.json()  # 返回结果转json
    #print("返回结果:%s" % res)
    #List.append(f"返回结果：{res}")
    if res["status"] == 1 and res["message"] == "操作成功":
        #print("青年大学习已完成")
        List.append(f"[账号{str(i)}]青年大学习已完成")
    else:
        print("error")


#if __name__ == '__main__':
#    laravel_session="ZBps3sXJdrXmeeciQ0LXCnoq0pBNujjmzOXaWpnQ"
#    main(laravel_session)
if __name__ == '__main__':
    i = 0
    if 'QNDXX' in os.environ:
        user = os.environ['QNDXX'].split('&')
        for x in user:
            i += 1
            user = x
            List.append(f'===> [账号{str(i)}]Start <===')
            main(user)
            List.append(f'===> [账号{str(i)}]End <===\n')
            time.sleep(1)
        tt = '\n'.join(List)
        print(tt)
        send('青年大学习', tt)
    else:
        print('未配置环境变量')
        send('青年大学习', '未配置环境变量')
