import os
from flask import Flask, jsonify, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from clear_mask import Vibrato
import re
IS_SERVERLESS = bool(os.environ.get('SERVERLESS'))
print(IS_SERVERLESS)
vibrato = Vibrato()
app = Flask(__name__)

# 初始化上传临时目录


def init_upload_dir():
    UPLOAD_DIR = '/tmp/uploads' if IS_SERVERLESS else os.getcwd() + '/uploads'
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    app.config['UPLOAD_DIR'] = UPLOAD_DIR


init_upload_dir()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/mp4', methods=['GET', 'POST'])
def save_mp4():
    url = request.form.get('url')
    print(url)
    regx = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    listurl = re.findall(regx, url)
    if len(listurl) == 0:
        print("解析链接失败")
        res = {"error": "No avatar file selected"}
    else:
        vid = vibrato.run(listurl[0])
        file_name = vid + ".mp4"
        filePath = os.path.join(app.config['UPLOAD_DIR'], vid + ".mp4")
        res = {'path': filePath}

    return jsonify(data=res)


@app.route('/mp4url', methods=['GET', 'POST'])
def mp4url():
    url = request.form.get('url')
    print(url)
    regx = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    listurl = re.findall(regx, url)
    if len(listurl) == 0:
        print("解析链接失败")
        res = {"error": "No avatar file selected"}
    else:
        vid = vibrato.reurl(listurl[0])
        res = {'path': vid}
    return jsonify(data=res)

    return jsonify(data=res)


# 启动服务，监听 9000 端口，监听地址为 0.0.0.0
app.run(debug=IS_SERVERLESS != True, port=9000, host='0.0.0.0')
