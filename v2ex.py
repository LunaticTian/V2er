# -*- coding: utf-8 -*-
import datetime
import hashlib
import requests
from bs4 import BeautifulSoup
import re


heard = {
    "authority": "www.v2ex.com",
    "method": "GET",
    "path": "/go/flamewar?p=1",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "cookie": '_ga=GA1.2.39129319.1594622347; __gads=ID=043d6a87b305c2fa:T=1594622347:S=ALNI_MYxvZs8jISFiRaeb5xvTo3mUiGRZA; PB3_SESSION="2|1:0|10:1597026505|11:PB3_SESSION|36:djJleDoxMTkuMjguMTAuMTY3OjI0NzMxMjE1|a5b5feed68c8856fe23a22a10eff515d675860025125f4f901aa50dd5c8afd85"; _gid=GA1.2.1161767240.1597026508; __cfduid=d179e866f124e7b7d354b82808a770c311597214357; A2="2|1:0|10:1597227977|2:A2|48:ZDVjOGM5YTItOGQ1MC00YzFhLWE3NzAtYTgyNmNiNzM1YzQ2|f576fd971ed7f25522b6d1e13111422dd7ffcb3b362d9350bc812a727d70a766"; V2EX_LANG=zhcn; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; V2EX_REFERRER="2|1:0|10:1597374396|13:V2EX_REFERRER|12:Y29vbGt1MTIz|d1960c82f06faba562be315853f950c762a9cdaf5a7b00a823d64c24ea07102a"; V2EX_TAB="2|1:0|10:1597396058|8:V2EX_TAB|12:Y3JlYXRpdmU=|e18c67474904672366de8a4537a5faf6544d1b2a4c1a68cb8ba4c983697ec1d4"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
}


urllist  = ['https://www.v2ex.com/go/flamewar','https://www.v2ex.com/go/chamber','https://www.v2ex.com/?tab=hot']
listSubjecId = []
# 获取每个节点的主题url以及页数
def getSubjectUrl(url):
    req = requests.get(url=url + '?p=1',headers = heard)
    # print(req.text)
    soup = BeautifulSoup(req.text,"lxml")
    a = soup.select("#TopicsNode > div")
    #print(len(a))

    for i in a :
        pattern = re.compile('topic-link" href="(.*?)">', re.S)
        items = re.findall(pattern, str(i))
        timeK = True
        pattern = re.compile('</a></strong>  •  (.*?)前', re.S)
        items1 = re.findall(pattern, str(i))

        pattern = re.compile('.*<a class=".*?" href=.*">(.*?)</a>', re.S)
        items2 = re.findall(pattern, str(i))
        # 记录页数
        page = 0
        try:
            page = int(items2[0])/100
        except Exception:
            continue
        a = str(page).split('.')[1]
        page = int(page)
        if int(a) > 0:
            page = int(page) + 1
        else:
            page = int(page) + 0
        # 这里对回复时间进行判断如果超过循环的时间，不对该贴进行爬虫
        link = (str(items[0]).split("#")[0], page)
        if (timeK):
            listSubjecId.append(link)
        else:
            items1Str = str(items1[0])
            if (not("天" in items1Str or "小时" in items1Str)):
                listSubjecId.append(link)



# 获取单个帖子的回复
def getSubject(tiezi):
    for i in range(1,int(tiezi[1])+1):
        url = 'https://www.v2ex.com' + tiezi[0]+"?p="+str(i)
        req = requests.get(url=url,headers = heard)
        soup = BeautifulSoup(req.text,"lxml")
        a = soup.select("#Main > div:nth-child(4) > div.cell")
        # print(a)
        for ai in a:

            soup1 = BeautifulSoup(str(ai), "lxml")
            a1 = soup1.select("div.reply_content")
            try:
                # 获取回复
                # 进行MD5
                print(a1[0].get_text())
            except Exception as e:
                continue
            pattern = re.compile('<a class="dark".*">(.*?)</a>.*ago">(.*?)前', re.S)
            items = re.findall(pattern, str(ai))
            # 获取回复的时间与作者
            #print(items)

            #print(items[0][0] + "   "+items[0][1])
            day = 0
            if "天" in items[0][1]:
                number = re.sub("\D", "", items[0][1])
                day = replyTimeCompute(int(number))
            else:
                day = replyTimeCompute(0)
            print(items[0][0] + "    "+ str(day) + "  " + tiezi[0])
            print("===========================")





# 获取单个用户的回复
def getReplyList(user):
    url = "https://www.v2ex.com/member/" + user+"/replies"
    req = requests.get(url=url)
    soup = BeautifulSoup(req.text, "lxml")
    #a = soup.select("#Main > div:nth-child(6)")  #Main > div.box
    a = soup.select("#Main > div.box")
    soup1 = BeautifulSoup(str(a), "lxml")
    reply = soup1.select("div.reply_content")  # reply
    replyInfo = soup1.select("div.dock_area")  # reply info
    ReplyList = []
    for i in range(len(reply)):
        # 获取时间/url
        pattern = re.compile('"fade">(.*?)</span></div>.*a href="(.*?)">', re.S)
        items = re.findall(pattern, str(replyInfo[i]))
        # print(items[0]) # ('1 天前', '/t/697703#reply47')
        items1 = reply[i].get_text()
        md5 = replyContentMD5(items1[0])
        day = 0
        if "天" in items[0][0]:
            number = re.sub("\D", "", items[0][0])
            day = replyTimeCompute(int(number))
        else:
            day = replyTimeCompute(0)
        ReplyList.append((day,items1,md5,items[0][1]))
    return user,ReplyList


def replyTimeCompute(day):
    new = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
    replyDay = datetime.timedelta(days=day)
    replyTime = (new - replyDay).strftime("%Y-%m-%d")
    return replyTime

def replyContentMD5(reply):
    return hashlib.md5(reply.encode(encoding='utf-8')).hexdigest()


# if __name__ == '__main__':
#     for i in urllist:
#         getSubjectUrl(i)
#     for i in listSubjecId:
#         getSubject(i)


'''
用户名单 以及 节点名单均在数据库中存放方便及时添加用户或节点
'''