# This is a sample Python script.


from flask import Flask, render_template, jsonify, request, send_from_directory, make_response
import time
import os
import base64

app = Flask(__name__)
UPLOAD_FOLDER = '/root/attack/AdvCamera/pics'
# TODO:修改下载文件夹
DOWNLOAD_FOLDER = '/root/attack/AdvCamera/output/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', 'mp4'])

@app.route('/')
def index():
    return "Hello"
# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 用于测试上传
@app.route('/test/upload')
def upload_test():
    return render_template('upload.html')


# 文件下载
# @app.route('/api/download/', methods=['GET', 'POST'], strict_slashes=False)
@app.route('/api/download/<filename>', methods=['GET', 'POST'], strict_slashes=False)
def api_download(filename):
    # status 200, 404  -> 文件未找到/未处理完成 , 可返回
    # filename为请求图片名称,为 rawName+_adv+后缀
    try:
        if os.path.isdir(filename):
            # return '<h1>文件夹无法下载</h1>'
            return make_response("File is being processed", 404)
        else:
            # name = filename.rsplit('\\')[-1]  # 取得文件名称
            # filename = filename.replace(name, '')
            return send_from_directory(DOWNLOAD_FOLDER, filename=filename, as_attachment=True)  # 自动设置状态码为200
    except:
        return make_response("File is being processed", 404)


# 上传文件
@app.route('/api/upload/<type>', methods=['POST'], strict_slashes=False)
def api_upload(type):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = f.filename
        print(fname)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        #unix_time = int(time.time())
        #new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, fname))  # 保存文件到upload目录
        #print(new_filename)
        token = base64.b64encode(fname.encode('utf-8')).decode('ascii')
        print(token)
        # TODO: 1.添加对抗攻击调用代码
        tmp = fname.split('.')
        tmp[0] = tmp[0] + "_adv."
        fname_adv = tmp[0] + tmp[1]
        src = "/root/attack/AdvCamera/pics/" + fname
        dst = "/root/attack/AdvCamera/output/" + fname_adv
        if type == '0':
            os.system("python3 /root/attack/AdvCamera/example8/imagenet_tutorial_fgsm_pytorch.py " + src +" "+ dst)
        elif type == '1':
             os.system("python3 /root/attack/AdvCamera/example9/imagenet_tutorial_fgsm_mxnet.py " + src +" "+ dst)
        elif type == '2':
            os.system("python3 /root/attack/AdvCamera/blackbox/imagenet_tutorial_localsearchattack.py " + src +" "+ dst)
        print("success!")
        # TODO：2.添加放在服务器上download代码
        return jsonify({"errno": 0, "errmsg": "上传成功", "token": token})
    else:
        return jsonify({"errno": 1001, "errmsg": "上传失败"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
