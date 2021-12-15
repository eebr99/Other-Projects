from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def file():  # put application's code here
    return render_template('file.html')


if __name__ == '__main__':
    app.run()
