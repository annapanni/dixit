from flask import Flask, escape, request, jsonify, render_template
import config

app = Flask(__name__)

#-------------------- minta1 ------------------
@app.route('/test')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

#-------------------- minta2 ------------------
@app.route('/jsontest')
def jsontest():
    mydata = {'a': [1,2,3], 'b': 43}
    return jsonify( mydata )

#-------------------- minta3 ------------------
@app.route('/fromtemplate')
def fromtemplate():
    mydata = 'petike'
    return render_template('template.html', mydata=mydata)

app.run(host=config.host, port=config.port)
