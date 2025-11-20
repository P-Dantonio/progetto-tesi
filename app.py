import os
import io
import zipfile
from flask import Flask, render_template, request, jsonify, send_file
import src.core.processing as processing

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
        candidates = processing.search_scopus_candidates(full_name)
        return jsonify({'status': 'success', 'candidates': candidates, 'scholar_id': scholar_id})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Solo elaborazione (Download + Merge)
@app.route('/process_author', methods=['POST'])
def process_author():
    try:
        data = request.json
      
        result = processing.process_chosen_author(
            data['scopus_id'], data['scopus_name'], data['scholar_id']
        )
        
      
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Download Zip
@app.route('/download/zip/<author_folder>')
def download_zip(author_folder):
    # Controlla se la cartella esiste
    author_path = os.path.join(CACHE_DIR, author_folder)
    if not os.path.isdir(author_path): return "Non trovato", 404
    # Crea un file zip in memoria RAM
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Aggiungi tutti i file della cartella al file zip
        for root, dirs, files in os.walk(author_path):
            for file in files:
                zf.write(os.path.join(root, file), file)
    data.seek(0)
    return send_file(data, mimetype='application/zip', as_attachment=True, download_name=f'{author_folder}.zip')

if __name__ == '__main__':
    app.run(debug=True)