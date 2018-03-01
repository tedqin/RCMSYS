#encoding:utf-8
import time
from flask import Flask
from flask import render_template,redirect,request,url_for,session,json
import pickle
from rcmapi.rec_api import *
import sys
reload(sys)
sys.setdefaultencoding('gbk')

_path = sys.path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/overall')
def overall():
    return render_template('overall.html')

@app.route('/get_id_page')
def get_id_page():
    return render_template('getid.html')

@app.route('/get_id',methods =['POST'])
def get_id():
    try:
        _id = request.form['userid']
        print(_id)
        base_user,base_item,ranklist = recbooks(_id)
        return render_template('books.html', id = _id, base_user = base_user, base_item = base_item, ranklist = ranklist)
    except Exception as e:
        return render_template('error.html',e = e)

@app.route('/adduser',methods=['POST'])
def adduser():
    return render_template('adduser.html')

@app.route('/get_department',methods=["POST"])
def get_department():
    try:
        _department = request.form['department']
        department_list = {1:'cailiao',2:'caiwuchu',3:'chengshiyutiedao',4:'dianxin',5:'chuanmei',6:'hangli',7:'jianzhu',8:'jiaoyun',9:'jingguan',10:'jixie',11:'qiche',12:'ruanjian',13:'tumu',14:'zhongde'}
        rankings = pickle.load(open(_path[0] + "/data/tmp.txt", "r"))
        ranklist = load_rank(_path[0] + '\\data\\sc\\')
        return render_template('newman.html',books=rankings['tmp\\' + department_list[int(_department)]],ranklist=ranklist)
    except Exception as e:
        return render_template('error.html',e = e)

if __name__ == '__main__':
    app.run()
