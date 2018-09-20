import requests
from lxml import etree
import datetime
import time
import itchat

# 得到网页源代码
def getHtmlText(url):
    kv = {'user-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=kv,timeout=30)
        # 如果状态码不是200 则应发HTTPError异常
        r.raise_for_status()
        # 设置正确的编码方式
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Something Wrong!"

# 解析网页源代码
def parsingHtmlText(html):
    tree = etree.HTML(html)
    city = tree.xpath('//div[@class = "tit_weather"]/h2/text()')[0]
    weather = tree.xpath('//dd[@class = "txt"]/b/text()')[0]
    temperature = tree.xpath('//dd[@class = "txt"]/text()')[0]
    air = tree.xpath('//dd[@class = "air"]/b/text()')[0]
    lifenote = tree.xpath('//ul[@class = "lifeindex"]//p/text()')
    umbrella = lifenote[0]
    Ultraviolet = lifenote[2]
    allergy = lifenote[3]
    dress = lifenote[5]
    sun = lifenote[7]

    detailedInformation = {'city':city,
                           'weather':weather,
                           'temperature':temperature,
                           'air':air,
                           'umbrella':umbrella,
                           'Ultraviolet':Ultraviolet,
                           'allergy':allergy,
                           'dress':dress,
                           'sun':sun,
                           }
    return detailedInformation

def informationPrint(txtline,detailedInformation):
    startday = datetime.datetime(20XX, XX, XX)
    localtime = datetime.datetime.now().strftime("%Y-%m-%d")
    daydiff = (datetime.datetime.now() - startday).days

    finalPrint = '今天是{}，已经{}天了，{}今天天气：{},{}。气温：{},{}{}{}，{}{}-----{}'.format(localtime,daydiff,detailedInformation['city'],detailedInformation['weather'],detailedInformation['umbrella'],detailedInformation['temperature'],detailedInformation['dress'],detailedInformation['Ultraviolet'],detailedInformation['air'],detailedInformation['allergy'],detailedInformation['sun'],txtline,)
    return finalPrint


weatherurl = 'https://www.tianqi.com/XXXX/life.html'

f = open('123.txt', 'r', encoding=u'utf-8')
s = f.readlines()
lines = len(s)
n = 1

# 给特定好友发送
friends = ['XX', ]
itchat.auto_login(hotReload=True,)
while(True):
    # 每10秒提醒一次
    if datetime.datetime.now().second % 10 == 0:
            html = getHtmlText(weatherurl)
            detailedInformation = parsingHtmlText(html)
            if n <= lines:
                finalPrint = informationPrint(s[n - 1],detailedInformation)
                # print(finalPrint)
                for f in friends:
                    # 给所有微信好友发送
                    # username = f.UserName
                    users = itchat.search_friends(name = f)
                    userName = users[0]['UserName']
                    itchat.send(finalPrint, toUserName=userName)
                n += 1
            else:
                n = 1
            time.sleep(5)
