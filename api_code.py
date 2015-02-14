#-*- coding:utf-8 -*-

import base64
from Crypto.Cipher import AES
from urllib import unquote,quote
import hashlib

""""
使用场景:各种api接口
加密方式:对身份验证,对传输数据验证,可一起使用或单个使用
此代码仅为测试代码,使用时加入自己的逻辑代码
"""

# -------------------- 加密解密数据 --------------------------
# AES 加密数据
# 测试和java（android）,oc(ios)都能很好的配合使用

# 配置信息
jiamikey = iv = '1234567890abcDEF' # 这里的16位秘钥需要自己生成设定，关键信息
PADDING = '\0'
pad_it = lambda s: s+(16 - len(s)%16)*PADDING

def van_endata(data):
    # 进行加密
    generator = AES.new(jiamikey, AES.MODE_CBC, iv)
    crypt = generator.encrypt(pad_it(data))
    crypt = base64.b64encode(crypt)

    print '-----加密-----'
    print crypt

    return crypt


def van_dndata(data):
    # 解密
    crypt = unquote(data)
    crypt = base64.b64decode(crypt)
    generator = AES.new(jiamikey, AES.MODE_CBC, iv)
    recovery = generator.decrypt(crypt)
    result = recovery.rstrip(PADDING)

    print '-----解密-----'
    print result

    return result




# ---------------------- 对传输数据加密 ------------------------
strinfo = '{"uid":"12251522222222222222222", "nickname": "van小白?", "sex": "1"}'

if False:

    lockstr = van_endata(strinfo)
    result = van_dndata(lockstr)

    print '-------------------------'
    print strinfo
    print '-------------------------'
    print lockstr
    print '-------------------------'
    print result
    print '-------------------------'


# ---------------------- 请求用户身份验证 构造请求  ----------------------
# 数据，这里可以使用加密或不加密，根据接口效率和安全性要求来决定,需要注意就是必须和另外一端配合使用就行
data = van_endata(str(strinfo))
# 配置秘钥 ， 重要部分
miyao = 'localKey'
# 验证key生成，供接口服务器进行身份验证
# 生成规则，原始数据拼接秘钥，然后进行md5
keyStr = "%s%s" % (miyao,data)
key = hashlib.md5(keyStr).hexdigest()
# url编码，主要是避免base64后的=号之类的东西，
# 但是应该在key生成后，因为接收到的参数一般会自动url解码，这样的话就会残生key验证失败
data = quote(data)
# 生成请求url
url = "%s%s%s%s" % ('http://api.xxx.com/val=', data, '&key=', key)
# 请求发送



# ---------------------- 请求用户身份验证 服务端处理  ----------------------
# 接收的参数 (get参数)
value = 'A1ZhiBxv4B%2Bg0HKBN5C0Q/WINM4gDcPJs3EUVoRYAZ08jrXOVO2CikhBMKCczixadXMUDbhGlIZgUwhNwwLHVGGqQyM0dFb1z8wtDi3JAW0%3D'
# 接收的验证key (get参数)
key = 'edd8b9c4b35a76f4e2613a1619d6a338'

# 身份验证
baseValue = unquote(value)
strJson = miyao + baseValue
nowKey = hashlib.md5(strJson).hexdigest()


if nowKey != key:
    # 检测身份失败
    print 'error api'
else:
    # 使用数据 baseValue
    # 如果请求方加密这里同步需要解密数据
    van_dndata(baseValue)


    # 检测身份合格,逻辑处理
    # 这里返回的数据也可以使用加密或不加密，同理请求方同步处理即可
















