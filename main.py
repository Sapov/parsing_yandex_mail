from flask import Flask, render_template

from mail import Mail

app = Flask(__name__)


@app.route('/')
def index():
    mail = Mail()
    mail.run()
    return render_template('templates/index.html')


if __name__ == "__main__":
    app.run(debug=True)
