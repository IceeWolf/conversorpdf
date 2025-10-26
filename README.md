# PDF Converter

Uma aplicação web moderna que converte PDFs para Excel com extração inteligente de tabelas.

## 📊 Funcionalidades

- **Extração inteligente de tabelas** usando pdfplumber e tabula-py
- **Preservação da estrutura** de colunas e dados
- **Múltiplas planilhas** por página
- **Parsing inteligente** para formatos não estruturados
- **Interface simples e intuitiva**

## 🚀 Instalação

### Opção 1: Executar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/IceeWolf/conversorpdf.git
cd conversorpdf
```

2. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

4. Abra seu navegador e acesse `http://localhost:5000`

### Opção 2: Deploy no Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/IceeWolf/conversorpdf)

Ou siga os passos:

1. Faça o fork deste repositório
2. Conecte seu repositório no Vercel
3. Configure as variáveis de ambiente (se necessário)
4. Deploy automático!

## 📖 Como Usar

### Fluxo Básico:
1. **Faça o upload** do arquivo PDF (arraste e solte ou clique para selecionar)
2. **Clique em "Converter para Excel"**
3. **Aguarde o processamento**
4. **Baixe** o arquivo Excel gerado

### Tipos de PDF Suportados:
- ✅ Tabelas estruturadas com bordas claras
- ✅ Documentos com múltiplas tabelas
- ✅ Listas de dados não estruturadas
- ✅ Conteúdo misto com elementos gráficos

## 🛠️ Tecnologias

### Backend:
- **Python Flask** - Framework web
- **pdfplumber** - Extração primária de tabelas
- **tabula-py** - Fallback para PDFs complexos
- **openpyxl** - Geração de arquivos Excel
- **pandas** - Manipulação de dados

### Frontend:
- **HTML5, CSS3, JavaScript** - Interface moderna e responsiva
- **Design limpo e intuitivo**

## 📁 Estrutura do Projeto

```
conversorpdf/
├── app.py                      # Aplicação Flask principal
├── requirements.txt            # Dependências Python
├── vercel.json                 # Configuração Vercel
├── README.md                   # Esta documentação
├── .gitignore                  # Arquivos ignorados
├── static/
│   ├── css/
│   │   └── style.css          # Estilos
│   └── js/
│       └── main.js            # JavaScript
├── templates/
│   └── index.html             # Interface HTML
├── modules/
│   ├── __init__.py            # Inicialização do módulo
│   ├── pdf_utils.py           # Utilitários comuns
│   └── pdf_converter.py       # Módulo de conversão
├── uploads/                    # Arquivos temporários (gitignored)
└── output/
    └── excel/                  # Arquivos Excel (gitignored)
```

## 🔧 Funcionalidades Avançadas

### Parser Inteligente:
- Detecta automaticamente padrões estruturados
- Reconhece informações de empresa e dados relacionados
- Cria colunas estruturadas automaticamente

### Sistema de Fallbacks:
1. **Primeiro**: Tenta extrair tabelas estruturadas (`pdfplumber`)
2. **Segundo**: Se falhar, extrai texto e aplica parsing inteligente
3. **Terceiro**: Se `tabula-py` falhar, usa parsing de texto
4. **Último**: Parsing genérico para qualquer texto estruturado

### Estrutura Excel Otimizada:
- **Colunas**: ID, Descrição, Unidade, Valor, Data, Empresa, etc.
- **Formatação**: Headers em negrito, larguras ajustadas
- **Múltiplas páginas**: Cada página vira uma planilha separada

## 📝 API Endpoints

- `GET /` - Interface principal
- `POST /upload` - Upload de arquivo PDF
- `POST /convert` - Converte PDF para Excel
- `GET /download-excel/<filename>` - Download do arquivo Excel
- `GET /preview/<filename>` - Preview do PDF

## 🎯 Casos de Uso

### Caso 1: PDF com tabelas estruturadas
- Upload do PDF
- Conversão automática para Excel
- Download do arquivo Excel

### Caso 2: PDF com dados não estruturados
- Upload do PDF
- Parsing inteligente detecta padrões
- Extração automática para colunas

### Caso 3: PDF complexo com múltiplas páginas
- Upload do PDF
- Cada página vira uma planilha separada
- Estrutura preservada

## 🚀 Deploy

### Vercel
1. Conecte seu repositório ao Vercel
2. Configure Python como runtime
3. Deploy automático!

### Outros Plaftormas
- **Heroku**: Configure Procfile com `web: python app.py`
- **Railway**: Selecione Python e configure start command
- **Fly.io**: Use `fly deploy`

## 🛡️ Segurança

- Validação de arquivos PDF
- Limite de tamanho de arquivo (16MB)
- Upload seguro com nomes únicos
- Limpeza automática de arquivos temporários

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e distribuir.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📧 Contato

Para sugestões, bugs ou dúvidas, abra uma issue no GitHub.

---

**PDF Converter** - A solução inteligente para conversão de PDFs para Excel! 📊✨