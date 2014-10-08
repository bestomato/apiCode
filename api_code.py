#-*- coding:utf-8 -*-

import base64
import time
import random
from urllib import unquote
import hashlib

""""
使用场景:各种api接口
加密方式:对身份验证,对传输数据验证,可一起使用或单个使用
此代码仅为测试代码,使用时加入自己的逻辑代码
"""

# ----------------------------------------------
def van_endata(data):

    # 使用base64处理
    one = base64.encodestring(data)

    # 翻转字符串
    two = ''
    for i in one:
        two = i + two

    # 插入key,即在第n位插入n位随机数，n位当前天
    dataLen = len(two)
    day = time.strftime('%d',time.localtime(time.time()))
    key = str(random.randint(0, 9))

    n = 1
    three = ''
    sign = True
    for i in two:
        now = str(n)
        if day == now:
            three = three + key + i
            sign = False
        else:
            three = three + i
        n += 1
    #for

    # 获取天数大于本身的数据长度，没有连接上key，这样的话把他放入最后一位
    if sign:
        three = three + key

    # 返回
    return three


def van_dndata(data):
    day = time.strftime('%d',time.localtime(time.time()))
    dataLen = len(data)

    n = 1
    three = ''
    sign = True
    for i in data:
        now = str(n)
        if day == now:
            three = three
            sign = False
        else:
            three = three + i
        n += 1
    #for

    # 截取
    if sign:
        three = three[:-1]

    # 翻转字符串
    two = ''
    for i in three:
        two = i + two

    # 使用base64处理
    one = base64.decodestring(two)
    return one


# ---------------------- 对传输数据加密 ------------------------
strinfo = '{"uid":"12251522222222222222222", "nickname": "van小白?", "sex": "1"}'

lockstr = van_endata(strinfo)
result = van_dndata(lockstr)

print strinfo
print lockstr
print result

# ---------------------- 请求用户身份验证  ----------------------
# 接收的参数 (get参数)
value = 'eyJwbGF0Zm9ybWNvZGUiOjQsInBhc3N3b3JkIjoiZDg1NzhlZGY4NDU4Y2UwNmZiYzViYjc2YTU4YzVjYTQiLCJhY2NvdW50IjoiMTAwMDAwMDAwMDEiLCJnZXhpbmNsaWVudGlkIjoiMTM3ZGM5ZDI4ZTYzNTQ3ZjM1ODQyNTMzODY3MDVhNDkiLCJtZWRpYV90eXBlIjozfQ%3d%3d'
# 验证key (get参数)
key = 'ba28dcf0ef16612072ad57a102d60505'

# 身份验证
baseValue = unquote(value)
strJson = "localKey321" + baseValue
nowKey = hashlib.md5(strJson).hexdigest()


if nowKey != key:
    # 检测身份失败
    print 'no'
else:
    # 检测身份合格

    # 使用数据 value
    print baseValue














