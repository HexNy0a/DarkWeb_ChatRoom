from flask import Flask, request

app = Flask(__name__)

# 接收最终明文
@app.route('/receive', methods = ['POST'])
def receive():
    plaintext = request.form.get('message') # 接收最终明文
    print(plaintext)
    return ''

app.run(host = '0.0.0.0', port = 6721)