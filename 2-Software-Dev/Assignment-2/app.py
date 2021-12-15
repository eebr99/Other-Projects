from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/education')
def education():
    return render_template('education.html')


@app.route('/work')
def work():
    return render_template('work.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
