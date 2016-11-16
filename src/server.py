'''
Created on Nov 11, 2016

@author: eric
'''
from flask import Flask,send_from_directory,request
import os
from flask import Response
from werkzeug.utils import secure_filename

app = Flask(__name__)
mime_map = {'.png':'image/png','.xpm':'image/xpm'}

@app.route('/')
def index():
    my_dir = os.path.dirname(__file__)
    file_path = os.path.join(my_dir, 'pics')
    #mimetype = mime_map['.png']
    #res = Response(mimetype = mimetype)
    #return(res)
    return(send_from_directory(file_path, 'firefox.png'))
 
@app.route('/upload', method='POST')
def upload():
    file = request.files['file']
    if file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.dirname(__file__),filename))
        #return (render_template('index.html'),filename=filename)
    

if __name__ == '__main__':
    app.run(debug=True)