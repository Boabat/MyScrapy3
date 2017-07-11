"""
爬虫闯关第三题
http://www.heibanke.com/lesson/crawler_ex02/
黑板客记账模拟登陆
"""
import bs4
from bs4 import BeautifulSoup
import requests
import urllib.request
import re

url = "http://www.heibanke.com/lesson/crawler_ex02/"
login_url = "http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/"
    
data = { 'username': 'medyg', 'password': '19931122bihu'}
data2 = {'username':'medyg', 'password': 1}

r = requests.get(login_url)
if r.status_code == 200:
    cookie = r.cookies
    print("Get login_url success.")
else:
    print("cannot access " + login_url)
data['csrfmiddlewaretoken'] = cookie['csrftoken']
print(data)

r2 = requests.post(login_url, data = data, allow_redirects=False, cookies = cookie) #重定向post
if r2.status_code == 302:
    cookie2 = r2.cookies
    print("Post login_url data success.")
else:
    print("post login_url falied")
data2['csrfmiddlewaretoken'] = cookie2['csrftoken']
print(data2)

for num in range(0, 31):
    data2['password'] = num
    r3 = requests.post(url, data2, cookies = cookie2)
    print("try " + str(num))
    result = re.findall(r'密码错误', r3.text)
    print(result)
    #soup = BeautifulSoup(r3.text, "lxml")
    #print(soup.body.h3.string)
    if not result: 
        print(num)
        print(r3.text)
        break

