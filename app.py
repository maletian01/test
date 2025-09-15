from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # 允许跨域，前端调试更方便

# 数据库配置（可根据实际情况修改）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'sunson',
    'port': 3306,  # 如有自定义端口请修改
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_conn():
    return pymysql.connect(**DB_CONFIG)

@app.route('/api1/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
        username = data.get('username')
        password_md5 = data.get('password_md5')
        if not username or not password_md5:
            return jsonify({'success': False, 'msg': '参数缺失'}), 400
        conn = get_db_conn()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id FROM users WHERE username=%s AND password_md5=%s"
                cursor.execute(sql, (username, password_md5))
                user = cursor.fetchone()
                if user:
                    return jsonify({'success': True, 'msg': '登录成功'})
                else:
                    return jsonify({'success': False, 'msg': '用户名或密码错误'})
        finally:
            conn.close()
    except Exception as e:
        logging.exception('登录接口异常:')
        return jsonify({'success': False, 'msg': '服务器异常'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)