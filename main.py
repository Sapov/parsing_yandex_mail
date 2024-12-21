from flask import Flask, render_template

from mail import Mail

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/go')
def go():
    mail = Mail()
    mail.run()
    return render_template('templates/index1.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
