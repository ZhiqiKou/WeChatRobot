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

# 消息输出格式
def informationPrint(txtline,detailedInformation):
    startday = datetime.datetime(2017, 11, 17)
    # 服务器时间比所在地晚12个小时，所以获取的时间需要加上12小时
    fix = datetime.timedelta(hours=12)
    localtime = (datetime.datetime.now() + fix).strftime("%Y-%m-%d")

    daydiff = (datetime.datetime.now() + fix - startday).days

    finalPrint = '早上好！今天是{}，我们已经在一起{}天了，{}今天天气：{},{}。气温：{},{}{}{}，{}{}--------{}——Form：XXX'.format(localtime,daydiff,detailedInformation['city'],detailedInformation['weather'],detailedInformation['umbrella'],detailedInformation['temperature'],detailedInformation['dress'],detailedInformation['Ultraviolet'],detailedInformation['air'],detailedInformation['allergy'],detailedInformation['sun'],txtline,)
    return finalPrint

TulingKey = '59XXXXXXXXXXXXXXXXXXXXb470'
TulingApi = 'http://openapi.tuling123.com/openapi/api/v2'

def get_response(msg):
    # 构造了要发送给服务器的数据
    data = {
	"reqType":0,
    "perception": {
        "inputText": {
            "text": msg
        },
        "inputImage": {
            "url": "imageUrl"
        },
        "selfInfo": {
            "location": {
                "city": "XX",
            }
        }
    },
    "userInfo": {
        "apiKey": TulingKey,
        "userId": "WechatRobot"
    }
}
    try:
        r = requests.post(TulingApi, json = data).json()
        # 通过字典和列表的查找，没找到时返回None而不会抛出异常
        return r['results'][0]['values']['text']
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个空值
        return

@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = '仿佛出现了点问题，算了别问了，我爱你！' #'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    return reply or defaultReply


weatherurl = 'https://www.tianqi.com/XXXX/life.html'

f = open('SweetNothings.txt', 'r', encoding=u'utf-8')
s = f.readlines()
lines = len(s)
n = 1

# 给特定好友发送
friends = ['XX', ]
itchat.auto_login(hotReload=True,)
itchat.run(blockThread = False)
while(True):
    # 服务器时间差12个小时
    if (datetime.datetime.now().hour == 19) and (datetime.datetime.now().minute == 30) and (datetime.datetime.now().second == 0):
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
            time.sleep(3)