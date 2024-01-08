"""
@Author  ：段龙
@Date    ：2024/1/5 23:00
"""
# 百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json

appid = '*'  # 填写你的appid
secretKey = '*'  # 填写你的密钥
# appid = '20240105001932414'  # 填写你的appid
# secretKey = 'bQnMXu9MC_G3ynLOHCJQ'  # 填写你的密钥
httpClient = None
fromLang = 'en'  # 原文语种
toLang = 'zh'  # 译文语种
salt = random.randint(32768, 65536)


def translate(words, myurl='/api/trans/vip/translate'):
    return "翻译API限制，回头咱就换."
    # words = 'apple'
    sign = appid + words + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        words) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        print(result)
        return result.get('trans_result')[0].get('dst')
    except Exception as e:
        print(e)
        return ""
    finally:
        if httpClient:
            httpClient.close()

# print(translate("this is a dog!"))
