import json
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommendations', methods=['POST'])
def recommendations():
    url1 = request.form['url1']
    url2 = request.form['url2']
    url3 = request.form['url3']
    print(url1, url2, url3)
    return json.dumps([{'url': 'http://yandex.ru/', 'title': 'Yandex'}])

if __name__ == '__main__':
    app.run()
