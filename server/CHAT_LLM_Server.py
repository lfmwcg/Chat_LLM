from flask import Flask, render_template, Response
import os
from flask import jsonify

from flask import request

from CHAT_LLM_db import *

from CHAT_LLM_log import LOG



app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/get_session_data', methods=['GET'])
def get_session_data():
    data = query_recent_session_data_by_uid(get_uid())
    LOG(data)
    return jsonify(data)

@app.route('/get_conversion_data', methods=['GET'])
def get_conversion_data():
    session_id = request.args.get('sessionId')
    conversation_data = query_recent_conversion_data_by_uid_and_session_id(get_uid(), session_id)
    return jsonify(conversation_data)

@app.route('/usr_submit_data', methods=['POST'])
def usr_submit_data():
    data = request.json
    # 在这里处理接收到的数据
    input_content = data.get('input')
    LOG(input_content)
    # 进行处理并返回响应
    #return jsonify({'message': 'Data received and processed successfully'})
    #text = chat_with_LLM(input_content,model)
    #return jsonify({'message': text})
    #return text


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

def get_uid():
    return "uid1"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
