import bs4
from bs4 import BeautifulSoup
import urllib.request
import string
import re
import http.cookiejar

url = "http://www.heibanke.com/lesson/crawler_ex01/"
cj = http.cookiejar.LWPCookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

data = urllib.request.urlopen(url).read()
data = data.decode('utf-8')

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr',
    'Referer': 'http://www.heibanke.com/lesson/crawler_ex01/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
password = 0
while True:
    postData = {
    'csrfmiddlewaretoken' : 'sczCT2OaFZ5BAxTXR0rBNSFuqummuY2y',
    'username' : 'medyg',
    'password' : password 
    }
    postData = urllib.parse.urlencode(postData)
    postData = postData.encode('utf-8') #进行编码，否则会报POST data should be bytes or an iterable of bytes. It cannot be str.错误.
    req = urllib.request.Request(url, postData, headers)
    print(req)
    response = urllib.request.urlopen(req)
    text = response.read().decode('utf-8')
    #print(text)
    soup = BeautifulSoup(text, "lxml")
    msg = soup.body.h3.string
    if msg == "您输入的密码错误, 请重新输入":
        password+=1
        continue
    else:
        print(msg)
        print("password is : " + str(password))
        break
    #print(data)