import os
import io
import zipfile
from flask import Flask, render_template, request, jsonify, send_file
import src.core.processing_logic as processing_logic
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CACHE_DIR = os.path.join(app.root_path, 'data', 'cache')

@app.route('/')
def index():
    return render_template('dashboard.html')

# Solo ricerca Scopus 
@app.route('/search_scopus', methods=['POST'])
def search_scopus():
    try:
        data = request.json
        full_name = f"{data['nome']} {data['cognome']}"
        scholar_id = data['id']
        candidates = processing_logic.search_scopus_candidates(full_name)
        return jsonify({'status': 'success', 'candidates': candidates, 'scholar_id': scholar_id})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Solo elaborazione (Download + Merge)
@app.route('/process_author', methods=['POST'])
def process_author():
    try:
        data = request.json
        folder_name = processing_logic.process_chosen_author(
            data['scopus_id'], data['scopus_name'], data['scholar_id']
        )
        if folder_name:
            return jsonify({'status': 'success', 'folder': folder_name})
        else:
            return jsonify({'status': 'error', 'message': 'Errore elaborazione'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Download Zip
@app.route('/download/zip/<author_folder>')
def download_zip(author_folder):
    author_path = os.path.join(CACHE_DIR, author_folder)
    if not os.path.isdir(author_path): return "Non trovato", 404
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(author_path):
            for file in files:
                zf.write(os.path.join(root, file), file)
    data.seek(0)
    return send_file(data, mimetype='application/zip', as_attachment=True, download_name=f'{author_folder}.zip')



if __name__ == '__main__':
    app.run(debug=True)