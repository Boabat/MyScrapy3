"""
爬虫闯关第三题
http://www.heibanke.com/lesson/crawler_ex03/
黑板客爬虫之寻找长密码
"""

import bs4
from bs4 import BeautifulSoup
import requests
import urllib.request
import re
import threading
import queue

url = "http://www.heibanke.com/lesson/crawler_ex03/"
login_url = "http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex03/"
pw_url = "http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page="
pages = range(1,14)
data={'username': 'medyg', 'password': '19931122bihu', 'csrfmiddlewaretoken': ''}

""" 打开登陆页面 """
loginr = requests.get(login_url)
if loginr.status_code == 200:
    cookie = loginr.cookies
    print("get login_url success, csrftoken is :" + cookie['csrftoken'])
else:
    print("get login_url failed")
data['csrfmiddlewaretoken'] = cookie['csrftoken']

""" 登陆 """
pwr = requests.post(login_url, data = data, allow_redirects = False, cookies = cookie)
if pwr.status_code == 302:
    cookie2 = pwr.cookies
    print("post login_url success, csrftoken is :" + cookie2['csrftoken'])
else:
    print("post login_url failed, status_code is " + str(pwr.status_code))

""" 第四关闯关 """
pw_list = [-1]*101
count = 0
q = queue.Queue()
for i in range(3):
    q.put('finish')
""" 检索密码 """
def retrivePw(page):
    global count
    global threadCount
    global q
    print("retriving page: " + str(page))
    pwg = requests.get(pw_url + str(num), cookies = cookie2)
    soup = BeautifulSoup(pwg.text, "lxml")
    pos_list = soup.find_all('td', title='password_pos')
    val_list = soup.find_all('td', title='password_val')
    for i in range(len(pos_list)):
        if pw_list[int(pos_list[i].text)] == -1:
            pw_list[int(pos_list[i].text)] = int(val_list[i].text)
            count += 1
    q.put('finish')
    print("now queue lenth is " + str(q.qsize()))
    print("page: " + str(page) + " retrived. " + "Now has " + str(count) + " positions")
    threadCount -= 1
    #print(pw_list)
""" 多线程 """
threadCount = 0
while count != 100:
    for num in range(14):
        if q.get():
            print("now queue lenth is " + str(q.qsize()))
            threading.Thread(target = retrivePw, args=(num,)).start()
            threadCount += 1
            print(threadCount)
        if count >= 100:
            break;
pw = ""
for num in range(1, len(pw_list)):
    pw+=str(pw_list[num])
print(pw)
data['password'] = pw
data['csrfmiddlewaretoken'] = cookie2['csrftoken']
r = requests.post(url, data=data, cookies = cookie2)
print(r.text)