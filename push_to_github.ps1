# Script para fazer push do PDF Converter para o GitHub
# Execute com: .\push_to_github.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  PDF Converter - Push to GitHub" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Verificar se é um repositório git
if (Test-Path .git) {
    Write-Host "[1/5] Repositorio Git encontrado!" -ForegroundColor Green
} else {
    Write-Host "[1/5] Inicializando repositorio Git..." -ForegroundColor Yellow
    git init
}

# Adicionar arquivos
Write-Host "`n[2/5] Adicionando arquivos..." -ForegroundColor Yellow
git add .

# Fazer commit
$commitMessage = Read-Host "`n[3/5] Digite a mensagem de commit (ou pressione Enter para usar padrao)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Update PDF Converter - Ready for production"
}
Write-Host "Fazendo commit com mensagem: $commitMessage" -ForegroundColor Yellow
git commit -m $commitMessage

# Verificar se o remote existe
Write-Host "`n[4/5] Verificando remote origin..." -ForegroundColor Yellow
$remoteExists = git remote get-url origin -q 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Remote origin nao encontrado. Adicionando..." -ForegroundColor Yellow
    git remote add origin https://github.com/IceeWolf/conversorpdf.git
} else {
    Write-Host "Remote origin ja configurado." -ForegroundColor Green
}

# Push para GitHub
Write-Host "`n[5/5] Fazendo push para GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Push concluido com sucesso!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green
Write-Host "Proximo passo: Deploy no Vercel" -ForegroundColor Cyan
Write-Host "Veja DEPLOY.md para instrucoes.`n" -ForegroundColor Cyan
