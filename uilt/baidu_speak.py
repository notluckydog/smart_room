#!/usr/bin/python
# -*- coding: UTF-8 -*-
import snowboydetect
from aip import AipSpeech
#import tuling
import sys
import pyaudio
import wave
import requests
import json
import os, re
import time
import base64
import numpy as np
import random

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus

    timer = time.perf_counter
else:
    pass
    '''import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode'''

    #timer = time.time

#reload(sys)
sys.setdefaultencoding('utf-8')


def getSysVoice():
    result = str(os.popen("amixer get PCM | awk '{print $4}' |sed -n '5p'").readline().strip())
    volStr = result[1:3]
    print
    volStr
    return int(volStr)


voicePath = '/home/pi/share/tts/dvic/voice.pcm'
textPath = '/home/pi/share/tts/dtext/text.txt'
robotVoicePath = '/home/pi/share/tts/dvic/voice.mp3'
shaoyePath = '/home/pi/share/shaoye/kele'
novoicePath = '/home/pi/share/novoice/kele'
musicPath = '/home/pi/share/music'
''' 你的APPID AK SK  参数在申请的百度云语音服务的控制台查看'''
APP_ID = '23132382'
API_KEY = '1tSZS2GEcA6nRiewMyoeM1PG'
SECRET_KEY = 'ce4tP8kMkGsGa6zvgYB3XlF7vuQbEUqQ'

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
PER = 4
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 3

# FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
# FORMAT = FORMATS[AUE]
CUID = "123456gonepoo"
TTS_URL = 'http://tsn.baidu.com/text2audio'
TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE_TTS = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选
# 需要识别的文件
AUDIO_FILE = 'test.pcm'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
# 文件格式
FORMAT = AUDIO_FILE[-3:]  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
DEV_PID = 80001
ASR_URL = 'http://vop.baidu.com/pro_api'
SCOPE_STT = 'brain_enhanced_asr'  # 有此scope表示有极速版能力，没有请在网页里开通极速版
# 采样率
RATE = 16000  # 固定值

# 新建一个AipSpeech
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 最早的执行shell录音功能，已经不用了
def shellRecord_old(time):
    os.system('arecord -D "plughw:1,0" -d ' + str(time) + ' -r 16000  -t wav -f S16_LE ' + voicePath)


# 根据你录音的长短决定，这里更新了录音时间，可长可短，最短2秒，最长7秒，用110/16约等于7秒
# 假如你不说话，2秒钟+1秒判断后识别，假如你说话，最多可以连续7秒钟再识别，很人性化
def shellRecord():
    # 最小说话音量
    MIN_VOICE = 4000
    # 最大说话音量，防止干扰出现30000+的音量
    MAX_VOICE = 28000
    # 录音判断开始时间，前面的时间可能是回复的语音音量过大导致误判断
    START_SEC = 5
    # 录音判断间隔，约等于8/16=0.5秒
    INTERVAL = 5
    # 最大录音时间,16*10=160,十秒钟
    MAX_RECORD_TIME = 160
    temp = 20  # temp为检测声音值
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    # 录音文件输出路径
    WAVE_OUTPUT_FILENAME = voicePath
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    # snowboydecoder.play_audio_file()
    print("录音开始")

    frames = []
    flag = False  # 一重判断,判断是否已经开始说话，这个判断从第5个数字开始，防止前面数字大于30000的情况
    stat2 = False  # 二重判断,第一次判断声音变小
    stat3 = False  # 三重判断,第二次判断声音变小
    tempnum = 0  # tempnum、tempnum2、tempnum3为时间
    tempnum2 = 0
    tempnum3 = 0
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.short)
        # 获取录音的音量
        temp = np.max(audio_data)
        # 如果时间大于其实判断时间并且音量在正常范围之内
        if tempnum > START_SEC and flag == False and temp > MIN_VOICE and temp < MAX_VOICE:
            # 判断出开始说话
            flag = True
        # 如果已经开始说话，那么开始判断
        if (flag):
            # 如果声音小于正常范围
            if temp < MIN_VOICE:
                # 如果是stat2还是False状态，证明还未开始判断
                if stat2 == False:
                    # 时间点2和时间点3
                    tempnum2 = tempnum + INTERVAL
                    tempnum3 = tempnum + INTERVAL
                    # 状态2开始变为True，说明第一次判断开始
                    stat2 = True
                # 开始第二次判断，stat2为True表示已经第一次判断，超过第一次时间段开始第二次判断
                elif stat2 and stat3 == False and tempnum > tempnum2:
                    # 已经超过了第一个时间段，那么stat3为True,这是第二次判断
                    stat3 = True
                # stat2和stat3都为True并且超过第二个时间段，这是最后一次判断
                if stat2 and stat3 and tempnum > tempnum3:
                    print("录音完毕")
                    # 跳出循环
                    break
            else:
                # 只要声音变大了，那么就重置状态
                stat2 = False
                stat3 = False
        # 时间约1/16秒每次递增
        tempnum = tempnum + 1
        if tempnum > MAX_RECORD_TIME:  # 超时直接退出
            print("录音结束")
            # 跳出循环
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# 以前的录音代码
def shellRecord_second(time):
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = time
    WAVE_OUTPUT_FILENAME = voicePath

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("done")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# 播放语音
def mplayerSYMp3():
    os.system('mplayer ' + shaoyePath + str(random.randint(1, 10)) + '.mp3 > /dev/null 2>&1 &')


# 播放语音
def mplayerNOMp3():
    os.system('mplayer ' + novoicePath + str(random.randint(1, 10)) + '.mp3 > /dev/null 2>&1 &')


# 播放语音
def mplayerMp3():
    os.system('mplayer ' + robotVoicePath + ' > /dev/null 2>&1 &')


# 打开摄像头
def openCamera():
    os.system('sh /usr/local/mjpg/camera.sh > /dev/null 2>&1 &')


# 关闭摄像头
def closeCamera():
    os.system("ps -ef | grep mjpg | grep -v grep | awk '{print $2}' | xargs kill -9")


# 播放音乐
def mplayerMusic(fileName):
    os.system('mplayer ' + musicPath + '/' + '*' + fileName + '*' + ' > /dev/null 2>&1 &')


# 关闭音乐播放，关闭后台的循环音乐播放
def closeMplayer():
    isRunStr = str(os.popen("ps -ef | grep mplayer | grep -v grep | awk '{print $1}' |sed -n '1p'").readline().strip())
    if isRunStr == 'pi':
        print
        'isRun'
        os.system("ps -ef | grep mplayer | grep -v grep | awk '{print $2}' | xargs kill -9")
        musicLoopStr = str(
            os.popen("ps -ef | grep musicLoop | grep -v grep | awk '{print $1}' |sed -n '1p'").readline().strip())
        if musicLoopStr == 'pi':
            print
            'isRun'
            os.system("ps -ef | grep musicLoop | grep -v grep | awk '{print $2}' | xargs kill -9")


def compareStr(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


# 读取文件
def get_file_content(filePath):  # filePath  待读取文件名
    with open(filePath, 'rb') as fp:
        return fp.read()


def stt_normal(filename):  # 语音识别
    wordStr = ''
    # 识别本地文件
    result = client.asr(get_file_content(filename),
                        'pcm',
                        16000,
                        {'dev_pid': 1537, }  # dev_pid参数表示识别的语言类型 1536表示普通话
                        )
    print
    result

    # 解析返回值，打印语音识别的结果
    if result['err_msg'] == 'success.':
        print
        "stt successful"
        word = result['result'][0].encode('utf-8')  # utf-8编码
        if word != '':
            if word[len(word) - 3:len(word)] == '，':
                print
                word[0:len(word) - 3]
                with open(textPath, 'w') as f:
                    f.write(word[0:len(word) - 3])
                f.close()
            else:
                print(word.decode('utf-8').encode('utf-8'))
                print(word.decode('utf-8'))
                wordStr = word.decode('utf-8').encode('utf-8')
                with open(textPath, 'w') as f:
                    f.write(word)
                f.close()
        else:
            print
            "音频文件不存在或格式错误"
    else:
        print
        "错误"
    return wordStr


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 将本地文件进行语音合成
def tts(word):
    result = client.synthesis(word, 'zh', 1, {
        'vol': VOL, 'per': PER, 'spd': SPD, 'pit': PIT
    })

    # 合成正确返回audio.mp3，错误则返回dict
    if not isinstance(result, dict):
        with open(robotVoicePath, 'wb') as f:
            f.write(result)
        f.close()
        print
        'tts successful'


################################################## 最新版本百度极速语音识别和语音合成 ########################################
class DemoError(Exception):
    pass


"""  TOKEN start """


def getBaiduToken():  # 百度语音识别极速版
    print("fetch token begin")
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE_TTS in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """


def tts_new(word):
    token = getBaiduToken()
    tex = quote_plus(word)  # 此处TEXT需要两次urlencode
    print(tex)
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)
    print('test on Web Browser' + TTS_URL + '?' + data)

    req = Request(TTS_URL, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value) for name, value in f.headers.items())

        has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
    except  URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True

    # save_file = "error.txt" if has_error else 'result.' + FORMAT
    save_file = "error.txt" if has_error else robotVoicePath
    with open(save_file, 'wb') as of:
        of.write(result_str)

    if has_error:
        if (IS_PY3):
            result_str = str(result_str, 'utf-8')
        print("tts api  error:" + result_str)

    print("result saved as :" + save_file)


def stt(filename):
    token = getBaiduToken()

    speech_data = []
    with open(filename, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)
    speech = base64.b64encode(speech_data)
    if (IS_PY3):
        speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
              # "lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    # print post_data
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        print("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    if (IS_PY3):
        result_str = str(result_str, 'utf-8')
    print(result_str)

    wordStr = ''
    # 解析返回值，打印语音识别的结果
    print(result_str)
    result = json.loads(result_str)
    # 解析返回值，打印语音识别的结果
    if result['err_msg'] == 'success.':
        print
        "stt successful"
        word = result['result'][0].encode('utf-8')  # utf-8编码
        if word != '':
            if word[len(word) - 3:len(word)] == '，':
                print
                word[0:len(word) - 3]
                with open(textPath, 'w') as f:
                    f.write(word[0:len(word) - 3])
                f.close()
            else:
                print(word.decode('utf-8').encode('utf-8'))
                wordStr = word.decode('utf-8').encode('utf-8')
                with open(textPath, 'w') as f:
                    f.write(wordStr)
                f.close()
        else:
            print
            "音频文件不存在或格式错误"
            print
            "音频文件不存在或格式错误"
    else:
        print
        "错误"
    return wordStr


############################################################# 最新版本百度语音极速识别和语音合成 ###################################

def getWeatherTemp():
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=武汉'
    response = requests.get(url)
    wearher_json = json.loads(response.text)
    weather_dict = wearher_json['data']
    str = '%s%s%s%s' % (
        '亲爱的少爷',
        '当前温度', weather_dict['wendu'], '℃')
    return str


# 今日天气预报
def getWeather():
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=武汉'
    response = requests.get(url)
    wearher_json = json.loads(response.text)
    weather_dict = wearher_json['data']
    str = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (
        '亲爱的少爷',
        '今天是', weather_dict['forecast'][0]['date'], '，', '\n',
        '天气', weather_dict["forecast"][0]['type'], '，', '\n',
        weather_dict['city'], '最', weather_dict['forecast'][0]['low'], '，', '\n',
        '最', weather_dict['forecast'][0]['high'], '，', '\n',
        '当前温度', weather_dict['wendu'], '℃', '，', '\n',
        weather_dict["forecast"][0]['fengxiang'],
        weather_dict["forecast"][0]['fengli'].split("[CDATA[")[1].split("]")[0])
    return str


# 明日天气预报
def getTWeather():
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=武汉'
    response = requests.get(url)
    wearher_json = json.loads(response.text)
    weather_dict = wearher_json['data']
    str = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (
        '亲爱的少爷',
        '明天是', weather_dict['forecast'][1]['date'], '，', '\n',
        '天气', weather_dict["forecast"][1]['type'], '，', '\n',
        weather_dict['city'], '最', weather_dict['forecast'][1]['low'], '，', '\n',
        '最', weather_dict['forecast'][1]['high'], '，', '\n',
        weather_dict["forecast"][1]['fengxiang'],
        weather_dict["forecast"][1]['fengli'].split("[CDATA[")[1].split("]")[0],
        '。', '\n')
    return str


# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return (res.replace("temp=", "").replace("'C\n", ""))


# Return % of CPU used by user as a character string
def getCPUuse():
    return (str(os.popen("top -bn1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))


# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
# Index 3: perc RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:6])


# 改变声音大小
def changeVoiceMax(number):
    os.system("amixer set PCM " + str(number) + "%")


def getMplayerIsRun():
    isRunStr = str(os.popen("ps -ef | grep mplayer | grep -v grep | awk '{print $1}' |sed -n '1p'").readline().strip())
    if isRunStr == 'pi':
        print
        'isRun'
        return True
    else:
        print
        'noRun'
        return False


# 基本的业务逻辑
def loopRecord():
    textStr = ''
    mplayerSYMp3()
    time.sleep(1)
    shellRecord()
    textStr = stt(voicePath)
    print
    textStr
    if '明' in textStr and '天' in textStr and '气' in textStr:
        tts(getTWeather())
        mplayerMp3()
        time.sleep(10)
    elif '音量' in textStr or '声' in textStr:
        if '低' in textStr or '小' in textStr:
            changeVoiceMax(60)
        elif '恢复' in textStr or '正常' in textStr:
            changeVoiceMax(75)
        elif '最大' in textStr:
            changeVoiceMax(100)
        elif '大' in textStr or '高' in textStr:
            changeVoiceMax(90)
        tts('主人，音量已调到最悦耳的大小啦')
        mplayerMp3()
        time.sleep(4)
    elif '今' in textStr and '天' in textStr and '气' in textStr:
        tts(getWeather())
        mplayerMp3()
        time.sleep(13)
    elif 'cpu' in textStr or 'CPU' in textStr:
        # CPU informatiom
        CPU_temp = getCPUtemperature()
        CPU_usage = getCPUuse()
        tts('CPU温度' + str(CPU_temp) + '度' + '，' + 'CPU使用率百分之' + str(CPU_usage))
        mplayerMp3()
        time.sleep(7)
    elif '温度' in textStr:
        tts(getWeatherTemp())
        mplayerMp3()
        time.sleep(5)
    elif '内存' in textStr:
        # Output is in kb, here I convert it in Mb for readability
        RAM_stats = getRAMinfo()
        RAM_perc = round(100 * float(RAM_stats[1]) / float(RAM_stats[0]), 2)
        RAM_realPerc = round(100 * (float(RAM_stats[1]) + float(RAM_stats[4])) / float(RAM_stats[0]), 2)
        tts('内存已使用百分之' + str(RAM_perc) + '，' + '实际已使用百分之' + str(RAM_realPerc))
        mplayerMp3()
        time.sleep(8)
    elif '打开' in textStr and '摄像' in textStr:
        openCamera()
        tts('摄像头已打开')
        mplayerMp3()
        time.sleep(2)
    elif '关闭' in textStr and '摄像' in textStr:
        closeCamera()
        tts('摄像头已关闭')
        mplayerMp3()
        time.sleep(2)
    elif '随便' in textStr or '随机' in textStr or '放首歌' in textStr or '播放音乐' in textStr:
        # 后台调用随机播放歌曲
        os.system("python musicLoop.py > /dev/null 2>&1 &")
    elif '换一首' in textStr or '下一首' in textStr or '下一曲' in textStr:
        closeMplayer()
        time.sleep(2)
        fileNameList = os.listdir(musicPath)
        fileName = fileNameList[random.randint(0, len(fileNameList) - 1)]
        mplayerMusic(fileName)
    elif '停止' in textStr or '暂停' in textStr or '不要' in textStr or '休息' in textStr or '关闭音乐' in textStr or '安静' in textStr:
        closeMplayer()
    elif '防守' in textStr or '放手' in textStr or '放首' in textStr or '播放' in textStr or '放一首' in textStr or '唱一首' in textStr or '听一下' in textStr or '听一首' in textStr:
        newStr = textStr.replace('播放', '').replace('放一首', '').replace('唱一首', '').replace('听一下', '').replace('听一首',
                                                                                                            '').replace(
            '放首', '').replace('放手', '').replace('防守', '').replace('。', '')
        closeMplayer()
        mplayerMusic(newStr)
        time.sleep(1)
        if getMplayerIsRun() == False:
            tts("没有找到你想要播放的歌曲")
            mplayerMp3()
            time.sleep(3)
    # 这里你可以加上你的图灵机器人，我这里没加，你们自己看情况加，因为我有小爱同学了，哈哈哈哈
    else:
        mplayerNOMp3()
        time.sleep(2)

