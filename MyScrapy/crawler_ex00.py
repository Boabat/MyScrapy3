import urllib.request
import bs4
from bs4 import BeautifulSoup

url_head = "http://www.heibanke.com/lesson/crawler_ex00/"
tail = ""
while(True):
    data = urllib.request.urlopen(url_head + tail).read();
    data = data.decode('UTF-8')
    soup = BeautifulSoup(data, "lxml")
    h3_str = soup.body.h3.string
    tail = ""
    for s in h3_str:
        if not s.isdigit():
            continue
        else:
            tail+=s
    #tail = h3_str[11:len(h3_str)]
    if tail.isdigit():
        print(tail)
    else:
        print(h3_str)
        break
#print(data)