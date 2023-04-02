import time
import requests
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from flask import Flask, request, abort

global flag
global public_key1, public_key2, public_key3
global private_key1, private_key2, private_key3

# 加密
def encrypt(plaintext, public_key):
    cipher = PKCS1_v1_5.new(RSA.importKey(public_key)) # 加密对象

    ciphertext = ''
    for i in range(0, len(plaintext), 128): # 太长了分组加密
        ciphertext += cipher.encrypt(plaintext[i:i+128].encode('utf-8')).hex()

    return ciphertext

# 读取flag
def read_flag():
    global flag

    f = open("./static/LeiyNeKo_Nighttac", 'r')
    flag = 'Get '+f.read()+' for discover dark web secrets. High quality, low price. Perfect for aspiring hackers!'
    f.close()

    if len(flag) < 135:
        flag += '*'*(135-len(flag))

# 分发私钥
def send_private_key():
    global public_key1, public_key2, public_key3
    global private_key1, private_key2, private_key3

    # 生成三组公钥、私钥
    key = RSA.generate(2048)
    public_key1 = key.publickey().export_key()
    private_key1 = key.export_key()
    key = RSA.generate(2048)
    public_key2 = key.publickey().export_key()
    private_key2 = key.export_key()
    key = RSA.generate(2048)
    public_key3 = key.publickey().export_key()
    private_key3 = key.export_key()

    time.sleep(5)

    # 分发
    code1 = code2 = code3 = 0
    while code1 != 200 or code2 != 200 or code3 != 200: # 节点可能未启动
        try:
            r1 = requests.post('http://127.0.0.1:1289/private',data={'private_key':private_key1})
            r2 = requests.post('http://127.0.0.1:5092/private',data={'private_key':private_key2})
            r3 = requests.post('http://127.0.0.1:9346/private',data={'private_key':private_key3})
            code1 = r1.status_code
            code2 = r2.status_code
            code3 = r3.status_code
        except:
            time.sleep(1) # 等待三个节点启动完毕

# 每分钟发送一次密文
def send_message():
    global flag

    threading.Timer(60, send_message).start() # 每分钟发送一次

    # 加密
    ciphertext = encrypt(flag+'2.56.67.21', public_key3)
    ciphertext = encrypt(ciphertext+'2.56.93.46', public_key2)
    ciphertext = encrypt(ciphertext+'2.56.50.92', public_key1)

    # 发送
    requests.post('http://127.0.0.1:1289/receive',data={'message':ciphertext})

######################################################################

read_flag() # 读取flag
send_private_key() # 分发私钥
send_message() # 每分钟发送一次密文

app = Flask(__name__)

# SSRF获取公钥
@app.route('/')
def SSRF():
    if request.remote_addr == '127.0.0.1':
        return '你先好好看看自己私钥啥格式，别漏了"\\n"\n"public_key1": "'+public_key1.decode()+'", "\npublic_key2": "'+public_key2.decode()+'", "\npublic_key3": "'+public_key3.decode()+'"'
    else:
        abort(403)

app.run(host = '0.0.0.0', port = 9999)