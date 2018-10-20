from flask import *

app = Flask(__name__)
app.secret_key = 'Be5tp@sswrdever1sHeRe'
app.debug = True

@app.route("/")
def hello():
    return "Hello world"

app.run(debug= True, host="0.0.0.0", port="10000")
