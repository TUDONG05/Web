from flask import Flask, request, render_template, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

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
    cursor.execute(f"SELECT id, password FROM users WHERE username=%s;", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = __get_user_row(username=username)
    
    if user and check_password_hash(user['password'], password):
        return jsonify({'success': True, 'message': 'Đăng nhập thành công!'})
    
    return jsonify({'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu.'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('register.html', message="Mật khẩu không khớp.")

        if __get_user_row(username=username):
            return render_template('register.html', message="Tên đăng nhập đã tồn tại.")

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('login.html', message="Đăng ký thành công. Vui lòng đăng nhập.")

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    return "Chúc mừng sếp đã đăng nhập thành công!"


if __name__ == '__main__':
    app.run(debug=True)
