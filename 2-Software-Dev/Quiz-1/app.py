from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def change_image():  # put application's code here
    return render_template('change_image.html')


if __name__ == '__main__':
    app.run()