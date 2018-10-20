from flask import *

# initialise
app = Flask(__name__)
app.secret_key = 'Be5tp@sswrdever1sHeRe'
app.debug = True

page = {}
session = {}

# main page
@app.route("/")
def welcome_page():
    return render_template("index.html", session=session, page=page)

# run the application on 0.0.0.0, port 10000
app.run(debug= True, host="0.0.0.0", port="10000")
