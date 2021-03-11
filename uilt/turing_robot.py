import requests
#import itchat

#还未激活
KEY = '******'  # KEY为图灵机器人的api密钥，自己可以去官网申请


def turing_get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'userid': 'wechat-robot',
        'key': KEY,
        'info': msg,
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return




