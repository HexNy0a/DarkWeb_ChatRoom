import re
import requests
from flask import Flask, request, render_template
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

global private_key
global show_private_key, show_ciphertext, show_plaintext
show_private_key = show_ciphertext = show_plaintext = ''

# 解密
def decrypt(ciphertext, private_key):
    global show_plaintext
    cipher = PKCS1_v1_5.new(RSA.importKey(private_key)) # 解密对象
    ciphertext = bytes.fromhex(ciphertext)

    try:
        plaintext = ''
        for i in range(0, len(ciphertext), 256): # 分组解密
            plaintext += cipher.decrypt(ciphertext[i:i+256], None).decode('utf-8')

        show_plaintext = plaintext

        return plaintext
    except:
        show_plaintext = 'Not a ciphertext'
        return ''

######################################################################

app = Flask(__name__)

# 接收私钥
@app.route('/private', methods = ['POST'])
def private():
    global private_key, show_private_key
    show_private_key = private_key = request.form.get('private_key') # 更新私钥
    return ''

# 接收密文
@app.route('/receive', methods = ['POST'])
def receive():
    global show_ciphertext
    show_ciphertext = ciphertext = request.form.get('message') # 接收密文
    decrypt(ciphertext, private_key) # 解密
    return ''

# 聊天室
@app.route('/')
def index():
    return render_template('index.html')

# 拦截插件页面
@app.route('/intercept')
def intercept():
    return render_template('intercept.html')

# 更新插件数据
@app.route('/update')
def update():
    return show_private_key.replace('Y-----\n','Y-----\\n').replace('\n-----E','\\n-----E') + '@' + show_ciphertext + '@' + show_plaintext

# 接收修改后的“明文”、传递“明文”
@app.route('/pass_message', methods = ['POST'])
def pass_message():
    plaintext = request.form.get('message') # 接收修改后的“明文”

    data = plaintext[:len(plaintext)-10] # 数据部分
    IP = plaintext[len(plaintext)-10:] # IP部分
    port = IP[5:7]+IP[8:] # IP转端口(题目模拟需要)

    # 发送
    requests.post('http://127.0.0.1:'+port+'/receive',data={'message':data})
    return '<script>window.location.href = "./intercept";</script>'

# robots.txt
@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')

# shop.py.bak
@app.route('/shop.py.bak')
def shop_py_bak():
    return render_template('shop.py.bak')

# shop
@app.route('/shop')
def shop():
    html = '''<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
非常抱歉，本网站因被黑客攻击正在抢修中...<br>
<br>
Your IP：2.56.12.89<br>
您的访问已记入日志。<br>
    '''
    if request.args.get('api', None) is not None:
        api = request.args.get('api')
        if re.search(r'^[\d\.:]+$', api):
            get = requests.get('http://'+api)
            html += '<!--'+get.text+'-->'
    return html

app.run(host = '0.0.0.0', port = 1289)