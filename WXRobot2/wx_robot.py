import itchat
import requests
from datetime import datetime
import json
from multiprocessing import Pool
import time
import random
import threading


# 获取天数信息
def get_days():
    # 天数
    now = datetime.now()
    start_day = datetime(20XX, XX, XX)
    days_num = (now - start_day).days
    day = now.strftime('%Y年%m月%d日') + '，在一起的第' + str(days_num) + '天。'
    return day


# 获取天气信息
def get_weather_msg():
    # 天气情况
    # api：https://free-api.heweather.com/s6/weather?location=CITY&key=KEY
    weather_response = requests.get(
        'https://free-api.heweather.com/s6/weather?location=CITY&key=KEY')
    weather_json_body = json.loads(weather_response.text)
    weather_infos = weather_json_body['HeWeather6'][0]
    weather_status = weather_infos['status']

    # 空气质量实况
    # api：https://free-api.heweather.com/s6/air/now?location=CITY&key=KEY
    air_response = requests.get(
        'https://free-api.heweather.com/s6/air/now?location=CITY&key=KEY')
    air_json_body = json.loads(air_response.text)
    air_infos = air_json_body['HeWeather6'][0]
    air_status = air_infos['status']

    if weather_status == 'ok' and air_status == 'ok':
        basic = weather_infos['basic']
        location = basic['location']
        parent_city = basic['parent_city']
        admin_area = basic['admin_area']
        # 地点
        pos = admin_area + '省-' + parent_city + '市-' + location + '区'

        daily_forecast = weather_infos['daily_forecast'][0]
        # 天气
        weather = daily_forecast['cond_txt_d']
        # 最高温度
        tmp_max = daily_forecast['tmp_max']
        # 最低温度
        tmp_min = daily_forecast['tmp_min']
        # 日出时间
        sr = daily_forecast['sr']
        # 日落时间
        ss = daily_forecast['ss']
        # 风向
        wind_dir = daily_forecast['wind_dir']
        # 风力
        wind_sc = daily_forecast['wind_sc']
        # 相对湿度
        hum = daily_forecast['hum']
        # 降水概率
        pop = daily_forecast['pop']
        # 降水量
        pcpn = daily_forecast['pcpn']
        # 紫外线强度指数
        uv_index = daily_forecast['uv_index']
        # 能见度
        vis = daily_forecast['vis']

        lifestyle = weather_infos['lifestyle']
        # 舒适度指数
        comf_brf = lifestyle[0]['brf']
        comf_txt = lifestyle[0]['txt']
        # 穿衣指数
        drsg_brf = lifestyle[1]['brf']
        drsg_txt = lifestyle[1]['txt']
        # 感冒指数
        flu_brf = lifestyle[2]['brf']
        flu_txt = lifestyle[2]['txt']
        # 运动指数
        sport_brf = lifestyle[3]['brf']
        sport_txt = lifestyle[3]['txt']
        # 紫外线指数
        uv_brf = lifestyle[5]['brf']
        uv_txt = lifestyle[5]['txt']
        # 空气污染扩散条件指数
        air_brf = lifestyle[7]['brf']
        air_txt = lifestyle[7]['txt']

        air_now_city = air_infos['air_now_city']
        # 空气质量指数
        aqi = air_now_city['aqi']
        # 空气质量
        qlty = air_now_city['qlty']
        # 首要污染物
        main = air_now_city['main']

        weather_msg = pos + '今日天气：' + weather + '。最高温度：' + tmp_max + '℃，最低温度' + tmp_min + '℃。' + drsg_txt \
                      + '空气质量指数：' + aqi + '，空气质量：' + qlty + '，首要污染物：' + main + '。' + air_txt + '日出时间：' \
                      + sr + '，日落时间：' + ss + '。' + comf_txt + wind_dir + wind_sc + '级。' + sport_txt + '相对湿度：' \
                      + hum + '。降水概率：' + pop + '，降水量：' + pcpn + '。紫外线强度：' + uv_index + '。' + uv_txt + '能见度：' \
                      + vis + '公里。' + flu_txt
        return weather_msg
    else:
        # error_code = '请求失败,weather_status:' + weather_status + ',air_status:' + air_status
        return 'Error'


# 获取语句信息
with open('SweetNothings.txt', encoding='utf-8') as f:
    sweets = f.readlines()

TulingKey = '自己的图灵KEY'
TulingApi = 'http://openapi.tuling123.com/openapi/api/v2'


def tuling_msg(msg):
    # 构造了要发送给服务器的数据
    data = {
        "reqType": 0,
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
        r = requests.post(TulingApi, json=data).json()
        # 通过字典和列表的查找，没找到时返回None而不会抛出异常
        return r['results'][0]['values']['text']
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个空值
        return


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 为了保证在图灵出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = '仿佛出现了点问题，算了别问了，我爱你！'
    # 如果图灵Key出现问题，那么reply将会是None
    reply = tuling_msg(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    return reply or defaultReply


def cycle_to_remind():
    while True:
        now_time = datetime.now()
		# 每天早上七点二十发送信息
        if now_time.hour == 7 and now_time.minute == 20:
            if get_weather_msg() != 'Error':
                print('Send Message')
                message = get_days() + get_weather_msg() + '-----' + sweets[random.randint(0, len(sweets) - 1)]
                userinfo = itchat.search_friends(remarkName='XXX1')
                username = userinfo[0]['UserName']
                itchat.send(message, toUserName=username)
            else:
                print('Send Error Message')
                admininfo = itchat.search_friends(remarkName='XXX2')
                adminname = admininfo[0]['UserName']
                itchat.send('Something Error!', toUserName=adminname)
        time.sleep(60)


def load_wechat():
	# 退出时重新调用该方法进行登录
    itchat.auto_login(hotReload=True, exitCallback=load_wechat)


load_wechat()
t1 = threading.Thread(target=cycle_to_remind)
t2 = threading.Thread(target=itchat.run)
t1.start()
t2.start()
t1.join()
t2.join()
