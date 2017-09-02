#!env/bin/python

from flask import Flask, render_template , url_for , request
from handler import ldifCompareHandler
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/compare', methods = ['POST'])
def compare():
    aFile = request.files['aFile']
    bFile = request.files['bFile']
    #return ldifCompareHandler(aFile,bFile)
    return render_template("result.html",
                           items = ldifCompareHandler(aFile,bFile)
                           )