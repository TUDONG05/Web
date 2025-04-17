
from flask import Flask, request, render_template, jsonify
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Tudong05@",
        database="laptrinhweb"
    )


@app.route('/')
def login_page():
    return render_template('login.html')


def __get_user_row(username: str) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT id,password FROM users WHERE username='{username}';")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = __get_user_row(username=username)
    if user and user['password'] == password:
        return jsonify({'success': True, 'message': 'Đăng nhập thành công!'})
    return jsonify({'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu.'})


@app.route('/dashboard')
def dashboard():
    return "Chao mung!"


if __name__ == '__main__':
    app.run(debug=True)
