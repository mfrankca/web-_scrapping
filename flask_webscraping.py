from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from ebay_scrap_forweb import parse_arguments, read_listing_ids, scrape, write_to_excel, write_to_json

app = Flask(__name__)

# Get the current directory
current_dir = os.path.dirname(__file__)

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Set the template folder path
template_folder = os.path.join(parent_dir, 'template')

# Set the template folder for the Flask app
app.template_folder = template_folder



# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for('process_file', filename=filename))

@app.route('/process/<filename>', methods=['GET', 'POST'])
def process_file(filename):
    if request.method == 'POST':
        input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_format = request.form['output_format']
        output_excel_file = os.path.join(app.config['UPLOAD_FOLDER'], 'output.xlsx')
        output_json_file = os.path.join(app.config['UPLOAD_FOLDER'], 'output.json')
        args = parse_arguments([input_file, output_excel_file, output_json_file])
        listing_ids = read_listing_ids(args.input_file)
        scraped_data = []
        for item in listing_ids:
            data = scrape(item)
            if data:
                scraped_data.append(data)
        if 'excel' in output_format:
            write_to_excel(scraped_data, args.output_excel_file)
        if 'json' in output_format:
            write_to_json(scraped_data, args.output_json_file)
        return redirect(url_for('download_files', excel_file='output.xlsx', json_file='output.json'))

@app.route('/download/<excel_file>/<json_file>')
def download_files(excel_file, json_file):
    return render_template('download.html', excel_file=excel_file, json_file=json_file)

if __name__ == '__main__':
    app.run(debug=True)
