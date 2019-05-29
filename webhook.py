from flask import Flask,request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hook():
    fo = open('/tmp/hook.log','a+')
    fo.write(request.json)
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
