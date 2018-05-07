from court_parce import app
from flask import send_from_directory, render_template


@app.route('/', methods=['GET', 'POST'])
def index_page():
    return render_template('index_page.html')


@app.route('/dbcase/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['dbcase'],
                               filename)


@app.route('/download/<filename>', methods=['GET', 'POST'])
def download_exapmles(filename):
    return send_from_directory(app.config['DOWNLOAD'],
                               filename)
