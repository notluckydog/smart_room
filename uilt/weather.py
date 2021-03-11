import requests
import json

def weatherforlifestyle():
    lifestyle = 'https://devapi.heweather.net/v7/weather/now?'
    # 该接口的请求方式也为GET

    value = {
            'location':'114.178108,22.808359',
            'key': '57e20e831816408784f111288c9fc25a',
            'lang': 'zh'

        }

    weather = requests.get(lifestyle, params=value).json()
    if weather["code"] != "200":
        print("查询失败")

    else:
        weather_now = weather["now"]
        icon = weather_now["icon"]
        text = weather_now["text"]
        temp = weather_now["temp"]
        print(icon)

    return [icon,text,temp]

def main():
    print(weatherforlifestyle())

if __name__=='__main_':
    main()