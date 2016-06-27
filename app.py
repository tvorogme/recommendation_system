import json
from flask import Flask, render_template, request
from data.data_utils import TvrainData
app = Flask(__name__)
data = TvrainData()

@app.route('/')
def index():
    topics = data.get_random_articles(10)
    return render_template('index.html', topics = topics)


@app.route('/recommendations', methods=['POST'])
def recommendations():
    url1 = request.form['url1']
    url2 = request.form['url2']
    url3 = request.form['url3']
    print(url1, url2, url3)
    return json.dumps([{'url': 'http://yandex.ru/', 'title': 'Yandex'}])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
