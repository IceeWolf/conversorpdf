// PDF Converter - JavaScript simplificado
// Gerencia apenas a conversão de PDF para Excel

// Global variables
let selectedFile = null;

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultsSection = document.getElementById('resultsSection');
const resultMessage = document.getElementById('resultMessage');
const downloadButtons = document.getElementById('downloadButtons');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');

// File input change handler
fileInput.addEventListener('change', handleFileSelect);

// Drag and drop handlers
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
uploadArea.addEventListener('click', () => fileInput.click());

// File handling functions
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'application/pdf') {
            processFile(file);
        } else {
            showError('Por favor, selecione apenas arquivos PDF.');
        }
    }
}

function processFile(file) {
    selectedFile = file;
    
    // Show file info
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Conversion function
function convertPDF() {
    if (!selectedFile) {
        showError('Nenhum arquivo selecionado.');
        return;
    }
    
    showProgress('Convertendo para Excel...');
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            return fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    filename: data.filename
                })
            });
        } else {
            throw new Error(data.message);
        }
    })
    .then(response => response.json())
    .then(data => {
        hideProgress();
        
        if (data.success) {
            showResults('PDF convertido para Excel com sucesso!', [
                {
                    text: '📊 Baixar Excel',
                    url: data.download_url,
                    class: 'download-btn-excel'
                }
            ]);
        } else {
            showError(data.message);
        }
    })
    .catch(error => {
        hideProgress();
        showError('Erro ao converter PDF: ' + error.message);
    });
}

// UI functions
function showProgress(message) {
    progressSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    progressText.textContent = message;
    
    // Animate progress bar
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        progressFill.style.width = progress + '%';
        
        if (progress >= 90) {
            clearInterval(interval);
        }
    }, 200);
}

function hideProgress() {
    progressSection.style.display = 'none';
    progressFill.style.width = '0%';
}

function showResults(message, buttons) {
    resultsSection.style.display = 'block';
    errorSection.style.display = 'none';
    
    resultMessage.textContent = message;
    
    // Clear previous buttons
    downloadButtons.innerHTML = '';
    
    // Add new buttons
    buttons.forEach(button => {
        const btn = document.createElement('a');
        
        if (button.url) {
            // Link button
            btn.href = button.url;
            btn.download = true;
        }
        
        btn.className = button.class;
        btn.textContent = button.text;
        downloadButtons.appendChild(btn);
    });
}

function showError(message) {
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorMessage.textContent = message;
}

function removeFile() {
    selectedFile = null;
    
    fileInfo.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    progressSection.style.display = 'none';
    
    fileInput.value = '';
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    console.log('PDF Converter carregado!');
});