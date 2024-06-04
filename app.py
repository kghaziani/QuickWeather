import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    print("Index route accessed")
    current_working_directory = os.getcwd()
    print("Current working directory:", current_working_directory)
    
    templates_path = os.path.join(current_working_directory, 'templates')
    print("Templates directory exists:", os.path.exists(templates_path))
    
    index_path = os.path.join(templates_path, 'index.html')
    print("index.html exists:", os.path.exists(index_path))
    
    return render_template('index.html')

if __name__ == '__main__':
    print("Running the Flask app...")
    app.run(debug=True)