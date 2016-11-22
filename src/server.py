'''
Created on Nov 11, 2016

@author: eric
'''
from flask import Flask,send_from_directory,request, render_template, url_for
import os

#from flask import Response
from werkzeug.utils import secure_filename

app = Flask(__name__)
mime_map = {'.png':'image/png','.xpm':'image/xpm'}

@app.route('/')
def index():
    my_dir = os.path.dirname(__file__)
    file_path = os.path.join(my_dir, 'pics')
    return(send_from_directory(file_path, 'firefox.png'))
 
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename:
            fname = secure_filename(file.filename)
            my_dir = os.path.dirname(__file__)
            file_path = os.path.join(my_dir, 'pics')
            file.save(os.path.join(file_path,fname))
            return render_template('index.html', filename=fname)
    return render_template('index.html')

@app.route('/list')
def browse_stored_file(): 
    
    my_dir = os.path.dirname(__file__)
    file_path = os.path.join(my_dir, 'pics')
    #file_list = [ os.path.join(my_dir, item)  for item in os.listdir(file_path) ]
    file_list = [ url_for('static', filename=item)  for item in os.listdir(file_path) ]
    
    return(render_template('list.html', file_list=file_list))
    
if __name__ == '__main__':
    app.run(debug=True)
