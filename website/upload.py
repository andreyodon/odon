from website import create_app
from flask import render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/alexis/PycharmProjects/pythonProject/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = create_app()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'
    return render_template('upload.html')
