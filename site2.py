import json 
from flask import request
from flask import Flask 
from flask import make_response,Response
from flask import render_template
import time
import datetime
import os 

button_signal_path = "./signal/button_signal.sig"
result_signal_path = "./signal/result_signal.sig"
pi_addr = "pi@10.42.0.150"
voice_path = "~/voice_response/"


app = Flask(__name__)

@app.route('/login', methods=['POST', 'GET'])
def login():
    result = ""
    start_time = ""
    end_time = ""
    start = 0
    end = 0
    if request.method == 'POST':
        with open(button_signal_path,'r+') as button_signal:
            button_signal.seek(0,0)
            button_signal.truncate()
            button_signal.write("1")
            #获取按钮按下时间，也就是开始识别时间
            start_time = time.strftime("%H:%M:%S", time.localtime())
            start = datetime.datetime.now()
            print(start_time) 
            print("识别按钮触发")
            cmd = "ssh " +pi_addr + " 'play " + voice_path + "20.mp3'"
            os.system(cmd)

        #按钮按下，结果文件清零，为以后的存入数据准备
        with open(result_signal_path, 'r+') as result_signal:
            result_signal.seek(0,0)
            result_signal.truncate()
    #循环检测结果文件，当有结果的时候返回刷新了的网页
    while True:
        #避免第一次的网页进入死循环无法显示
        with open(button_signal_path, 'r+') as button_signal:
            flag =  button_signal.read().strip()
            #检测按钮文件，设置初始状态
            try:
                if int(flag) == '0':
                    break 
            except:
                button_signal.seek(0,0)
                button_signal.truncate()
                button_signal.write("0")
                continue 

        with open(result_signal_path, 'r+') as result_signal:
            result = result_signal.read().strip()
            if result != '':
                print(result)
                result_signal.seek(0,0)
                result_signal.truncate()
                break 
            else:
                continue 

    #获取结果返回的时间
    end_time = time.strftime("%H:%M:%S", time.localtime())
    end = datetime.datetime.now() 
    print(start)
    print(end)

    #计算时间差值
    try:
        sub = (end-start).seconds
    except:
        sub = 0
    print(sub)
    return render_template('Home.html', result=result, start_time=start_time,
            end_time=end_time,sub=sub)
if __name__ == '__main__':
    app.run()
