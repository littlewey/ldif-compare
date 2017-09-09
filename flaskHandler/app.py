#!env/bin/python

from flask import Flask, render_template , url_for , request , make_response
from werkzeug.utils import secure_filename
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
    if len(request.form.getlist('ifCSV_Format')) == 1 :
        response = make_response(ldifCompareHandler(aFile,bFile)["csv"])
        response.headers['Content-type'] = 'text/txt' 
        response.headers['Content-Disposition'] = "attachment;filename=LDIF_compare_result.csv" 
    else:
        response = render_template("result.html",data = ldifCompareHandler(aFile,bFile)["data"])
    return response