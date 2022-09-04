from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

#服务器的repository secret
today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthdayman = os.environ['BIRTHDAYMAN']
birthdaywoman = os.environ['BIRTHDAYWOMAN']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

#接口
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['low']), math.floor(weather['high']), weather['airQuality']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthdaywoman():
  next = datetime.strptime(str(date.today().year) + "-" + birthdaywoman, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days


def get_birthdayman():
  next = datetime.strptime(str(date.today().year) + "-" + birthdayman, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)



#输出内容
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, low, high, airQuality= get_weather()
data = {"weather":{"value":wea},"temperaturelow":{"value":low}, "temperaturehigh":{"value":high},"airQuality":{"value":airQuality}, "love_days":{"value":get_count(), "color":get_random_color()},"birthdaywoman_left":{"value":get_birthdaywoman(), "color":get_random_color()},"birthdayman_left":{"value":get_birthdayman(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
