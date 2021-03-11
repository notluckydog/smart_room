import requests
import json
import socket



AK = 'TD9rhDMNi0K54nFWOXaPvx8WBQqUrRif'

url_ip = 'https://api.map.baidu.com/location/ip?ak=您的AK&ip=您的IP&coor=bd09ll'

url_weather = 'http://api.map.baidu.com/weather/v1/?data_type=all&ak='+AK

def main():

    '''data = requests.get(url_weather).json()
    print(data)'''

    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    print(ip)

    value = {
        'ak': AK,
        'ip': '58.60.230.210',
        'coor': 'bd09ll'
#coor=bd09ll
    }

    '''weather = requests.get(url_ip, params=value).json()
    print(weather)'''

    url = 'https://ip.cn/'
    res = requests.get(url)
    print(res)

if __name__=='__main__':
    main()
