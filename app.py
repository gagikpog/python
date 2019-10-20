from flask import Flask, render_template, url_for, request, abort, send_from_directory, jsonify
from user import User
from bill import Bill
from utility.utility import generate_token, get_hash_password, check_hash_password

app = Flask(__name__)

@app.route('/src/<path:path>')
def src(path):
    return send_from_directory('src', path)

@app.route('/')
def index():
    return render_template('index.html', appName = 'Flask1')

@app.route('/user')
def user():
    user = User()
    user.get_by_pk(1)
    return render_template('userPage.html', user = user)

@app.route('/auth', methods=['GET'])
@app.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


@app.route('/signin', methods=['POST'])
def signin():
    if not request.json or not 'login' in request.json or not 'password' in request.json:
        abort(400)

    login = request.json['login']
    password = request.json['password']

    if not login or not password:
        return '{"status": "error", "messagge": "login or password is empty"}'

    hash_pass = get_hash_password(password)

    token = generate_token()
    res = {"status": "auth"}
    res['token'] = token
    return jsonify(res)

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
