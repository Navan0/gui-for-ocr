from __future__ import division, print_function
from flask import send_from_directory
import os
import glob
import random
import shutil
from pdf2jpg import pdf2jpg
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer

from pdf2image import convert_from_path

from pdf2image.exceptions import (
 PDFInfoNotInstalledError,
 PDFPageCountError,
 PDFSyntaxError
)


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


print('Server ready Boss http://127.0.0.1:5000/')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        app.config['UPLOAD_FOLDER'] = "uploads/"
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        files = glob.glob('uploads/*')
        # for f in files:
        #     os.remove(f)
        # Get the file from post request
        f = request.files['file']



        # Save the file to ./uploads
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        # import pdb; pdb.set_trace()
        path = app.config['UPLOAD_FOLDER']+f.filename
        images = convert_from_path(path)
        for i, image in enumerate(images):
            print(i)
            fname = "image" + str(i) + ".jpg"
            img_path = app.config['UPLOAD_FOLDER']+fname
            import pdb; pdb.set_trace()
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],fname), "JPEG")
            print(fname)
            os.chdir(os.path.join(app.root_path, 'darknet'))
            os.system("./darknet detector test /home/navaneeth/work/text-obj.data /home/navaneeth/work/text-yolov3.cfg /home/navaneeth/work/text-yolov3_2000.weights /home/navaneeth/work/ocr-ml-flask/"+str(img_path))


        # ims = glob.glob('uploads/*')
        #
        # for fi in ims:
        #     import pdb; pdb.set_trace()
        #     os.system("./darknet detector test /home/navaneeth/work/text-obj.data /home/navaneeth/work/text-yolov3.cfg /home/navaneeth/work/text-yolov3_2000.weights" + str(fi))
    return "o"


if __name__ == '__main__':
    #app.run(port=5002, debug=True)

    # Serve the app with gevent
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()
    app.run(host='0.0.0.0', port=5000)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='static/images/favicon.ico')
