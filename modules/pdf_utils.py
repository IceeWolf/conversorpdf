"""
PDF Studio - Utilitários Comuns
Módulo com funções compartilhadas entre limpeza e conversão de PDF
"""

import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

def generate_unique_filename(original_filename):
    """Gera um nome de arquivo único"""
    file_id = str(uuid.uuid4())
    filename = secure_filename(original_filename)
    file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'pdf'
    return f"{file_id}.{file_extension}", file_id

def cleanup_file(file_path):
    """Remove arquivo temporário"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Erro ao remover arquivo {file_path}: {e}")

def validate_pdf_file(file):
    """Valida se o arquivo é um PDF válido"""
    if not file or file.filename == '':
        return False, "Nenhum arquivo selecionado"
    
    if not file.filename.lower().endswith('.pdf'):
        return False, "Apenas arquivos PDF são permitidos"
    
    return True, "Arquivo válido"

def get_file_size_mb(file_path):
    """Retorna o tamanho do arquivo em MB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / (1024 * 1024), 2)
    except:
        return 0

def format_file_size(bytes_size):
    """Formata o tamanho do arquivo para exibição"""
    if bytes_size == 0:
        return '0 Bytes'
    k = 1024
    sizes = ['Bytes', 'KB', 'MB', 'GB']
    i = 0
    while bytes_size >= k and i < len(sizes) - 1:
        bytes_size /= k
        i += 1
    return f"{bytes_size:.2f} {sizes[i]}"

def create_response(success=True, message="", data=None, error_code=None):
    """Cria resposta padronizada para API"""
    response = {
        'success': success,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if data:
        response.update(data)
    
    if error_code:
        response['error_code'] = error_code
    
    return response

