# Instruções de Deploy

Este documento contém instruções para fazer push para o GitHub e deploy no Vercel.

## 📋 Pré-requisitos

- Git instalado
- Conta no GitHub
- Conta no Vercel (ou GitHub login)

## 🚀 Push para GitHub

### 1. Inicializar Git (se ainda não foi feito)

```bash
git init
```

### 2. Adicionar todos os arquivos

```bash
git add .
```

### 3. Fazer commit inicial

```bash
git commit -m "Initial commit - PDF Converter application"
```

### 4. Adicionar remote do GitHub

```bash
git remote add origin https://github.com/IceeWolf/conversorpdf.git
```

### 5. Push para o GitHub

```bash
git branch -M main
git push -u origin main
```

## 🚀 Deploy no Vercel

### Opção 1: Via Dashboard do Vercel

1. Acesse [vercel.com](https://vercel.com)
2. Faça login com GitHub
3. Clique em "Add New Project"
4. Selecione o repositório `IceeWolf/conversorpdf`
5. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Install Command**: `pip install -r requirements.txt`
6. Clique em "Deploy"

### Opção 2: Via Vercel CLI

1. Instale o Vercel CLI:
```bash
npm i -g vercel
```

2. Faça login:
```bash
vercel login
```

3. Deploy:
```bash
vercel
```

4. Para produção:
```bash
vercel --prod
```

## 📦 Arquivos de Configuração

Os seguintes arquivos foram configurados para o deploy:

- **vercel.json**: Configuração do Vercel para Python/Flask
- **requirements.txt**: Dependências Python
- **runtime.txt**: Versão do Python (3.11)
- **.gitignore**: Arquivos ignorados pelo Git

## 🔍 Verificações Pós-Deploy

Após o deploy, verifique:

1. **API funcionando**: `https://seu-projeto.vercel.app/`
2. **Upload de arquivos**: Teste fazer upload de um PDF
3. **Conversão**: Verifique se o arquivo Excel é gerado
4. **Download**: Teste fazer download do arquivo

## 🐛 Troubleshooting

### Erro: ModuleNotFoundError

Se houver erro de módulo não encontrado:
1. Verifique se todas as dependências estão em `requirements.txt`
2. Certifique-se de que o Python 3.11 está configurado

### Erro: Internal Server Error

1. Verifique os logs no dashboard do Vercel
2. Certifique-se de que os diretórios estão sendo criados
3. Verifique se o tamanho do arquivo está dentro do limite (16MB)

### Erro: File too large

Por padrão, o Vercel limita uploads a 4.5MB para planos gratuitos.
Para aumentar, considere:
1. Upgrade para plano Pro
2. Ou use APIs de storage como AWS S3

## 🔗 URLs Importantes

- **GitHub Repository**: https://github.com/IceeWolf/conversorpdf
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Documentação Vercel**: https://vercel.com/docs

## 📝 Próximos Passos

1. ✅ Configurar domínio customizado (opcional)
2. ✅ Adicionar variáveis de ambiente (se necessário)
3. ✅ Configurar CI/CD para deploys automáticos
4. ✅ Adicionar monitoramento e analytics

---

**Pronto!** Seu aplicativo está configurado para deploy! 🎉
