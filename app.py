from flask import Flask, request, render_template, jsonify, send_file, flash
import os
from modules import PDFConverter, generate_unique_filename, cleanup_file, validate_pdf_file, create_response

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
EXCEL_FOLDER = os.path.join(OUTPUT_FOLDER, 'excel')
TEMP_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['EXCEL_FOLDER'] = EXCEL_FOLDER
app.config['TEMP_FOLDER'] = TEMP_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize modules
pdf_converter = PDFConverter(UPLOAD_FOLDER, EXCEL_FOLDER)

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload file for processing"""
    if 'file' not in request.files:
        return jsonify(create_response(False, "Nenhum arquivo enviado")), 400
    
    file = request.files['file']
    is_valid, message = validate_pdf_file(file)
    
    if not is_valid:
        return jsonify(create_response(False, message)), 400
    
    try:
        # Generate unique filename
        unique_filename, file_id = generate_unique_filename(file.filename)
        
        # Save uploaded file
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(upload_path)
        
        return jsonify(create_response(True, "Arquivo carregado com sucesso", {
            'file_id': file_id,
            'filename': unique_filename
        }))
        
    except Exception as e:
        cleanup_file(upload_path)
        return jsonify(create_response(False, f"Erro ao processar arquivo: {str(e)}")), 500


@app.route('/convert', methods=['POST'])
def convert_pdf():
    """Convert PDF to Excel"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify(create_response(False, "Nome do arquivo não fornecido")), 400
        
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(upload_path):
            return jsonify(create_response(False, "Arquivo não encontrado")), 404
        
        # Convert PDF
        success, excel_path, error = pdf_converter.convert_pdf_to_excel(upload_path)
        
        if success:
            excel_filename = os.path.basename(excel_path)
            return jsonify(create_response(True, "PDF convertido para Excel com sucesso", {
                'excel_filename': excel_filename,
                'download_url': f'/download-excel/{excel_filename}'
            }))
        else:
            return jsonify(create_response(False, error)), 500
            
    except Exception as e:
        return jsonify(create_response(False, f"Erro ao converter PDF: {str(e)}")), 500

@app.route('/preview/<filename>')
def preview_file(filename):
    """Preview PDF file"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify(create_response(False, "Arquivo não encontrado")), 404
    except Exception as e:
        return jsonify(create_response(False, f"Erro ao pré-visualizar arquivo: {str(e)}")), 500

@app.route('/download-excel/<filename>')
def download_excel(filename):
    """Download Excel file"""
    try:
        file_path = os.path.join(app.config['EXCEL_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=f"convertido_{filename}")
        else:
            return jsonify(create_response(False, "Arquivo Excel não encontrado")), 404
    except Exception as e:
        return jsonify(create_response(False, f"Erro ao baixar Excel: {str(e)}")), 500

# Ensure directories exist (both for local and Vercel)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(EXCEL_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

if __name__ == '__main__':
    print("PDF Converter iniciado!")
    print("Funcionalidade:")
    print("   - Conversão de PDF para Excel")
    print("Acesse: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# For Vercel deployment
if 'vercel' in os.environ:
    app = app
