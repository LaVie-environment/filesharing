from flask import Flask, render_template, request, send_file
import os

class FileSharingApp:
    def __init__(self, upload_folder='uploads'):
        self.app = Flask(__name__)
        self.upload_folder = upload_folder
        self.app.config['UPLOAD_FOLDER'] = upload_folder

        # Route to the main page
        @self.app.route('/')
        def index():
            return render_template('index.html')

        # Route to handle file uploads
        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            if 'file' not in request.files:
                return 'No file part'
            
            file = request.files['file']
            
            if file.filename == '':
                return 'No selected file'
            
            if file:
                file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], file.filename))
                return 'File uploaded successfully'

        # Route to serve uploaded files
        @self.app.route('/uploads/<filename>')
        def download_file(filename):
            return send_file(os.path.join(self.app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

        # Ensure the 'uploads' folder exists
        os.makedirs(upload_folder, exist_ok=True)

    def run(self, debug=True):
        # Run the app
        self.app.run(debug=debug)

if __name__ == '__main__':
    file_sharing_app = FileSharingApp()
    file_sharing_app.run()
