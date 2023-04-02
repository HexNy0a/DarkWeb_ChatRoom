import requests
from flask import Flask, request
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

global private_key

# 解密
def decrypt(ciphertext, private_key):
    cipher = PKCS1_v1_5.new(RSA.importKey(private_key)) # 解密对象
    ciphertext = bytes.fromhex(ciphertext)

    try:
        plaintext = ''
        for i in range(0, len(ciphertext), 256): # 分组解密
            plaintext += cipher.decrypt(ciphertext[i:i+256], None).decode('utf-8')

        return plaintext
    except:
        return ''

# 传递密文
def pass_message(plaintext):
    if plaintext == '':
        return

    data = plaintext[:len(plaintext)-10] # 数据部分
    IP = plaintext[len(plaintext)-10:] # IP部分
    port = IP[5:7]+IP[8:] # IP转端口(题目模拟需要)

    # 发送
    requests.post('http://127.0.0.1:'+port+'/receive',data={'message':data})

######################################################################

app = Flask(__name__)

# 接收私钥
@app.route('/private', methods = ['POST'])
def private():
    global private_key
    private_key = request.form.get('private_key') # 更新私钥
    return ''

# 接收密文
@app.route('/receive', methods = ['POST'])
def receive():
    ciphertext = request.form.get('message') # 接收密文
    plaintext = decrypt(ciphertext, private_key) # 解密
    pass_message(plaintext) # 传递密文
    return ''

app.run(host = '0.0.0.0', port = 9346)