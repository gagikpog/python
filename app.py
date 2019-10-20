from flask import Flask, render_template
from user import User
from bill import Bill

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', appName = 'Flask1')

@app.route('/user')
def user():
    user = User()
    print(user.get_by_pk(1))
    return render_template('userPage.html', user = user)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
