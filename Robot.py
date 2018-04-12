# 图灵机器人
import itchat
import requests

TulingKey = '593XXXXXXXXXXXXXX470'
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
    defaultReply = '仿佛出现了点问题，算了别问了，' #'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    return reply or defaultReply

# 将登陆二维码显示在控制台
itchat.auto_login()
itchat.run()