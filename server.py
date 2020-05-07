from flask import Flask, escape, request, jsonify
import config

app = Flask(__name__)

@app.route('/test')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/jsontest')
def jsontest():
    mydata = {'a': [1,2,3], 'b': 43}
    return jsonify( mydata )

app.run(host=config.host, port=config.port)
