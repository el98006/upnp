'''
Created on Nov 11, 2016

@author: eric
'''
from flask import Flask,send_from_directory,request, render_template, url_for, Response
import os

#from flask import Response
from werkzeug.utils import secure_filename

app = Flask(__name__)
mime_map = {'.png':'image/png','.xpm':'image/xpm'}


@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename:
            fname = secure_filename(file.filename)
            my_dir = os.path.dirname(__file__)
            file_path = os.path.join(my_dir, 'media')
            file.save(os.path.join(file_path,fname))
            return render_template('index.html', filename=fname)
    return render_template('index.html')

@app.route('/media/<path:filename>')
def get_media(filename):
    my_dir = os.path.dirname(__file__)
    file_path = os.path.join(my_dir, 'media')
    return(send_from_directory(file_path, filename))

@app.route('/')
def browse_uploaded_files(): 
    
    my_dir = os.path.dirname(__file__)
    file_path = os.path.join(my_dir, 'media')
    file_list = [ item  for item in os.listdir(file_path) ]
    
    return(render_template('list.html', file_list=file_list))
    
if __name__ == '__main__':
    app.run(debug=True)
