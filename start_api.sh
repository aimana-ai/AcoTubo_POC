#!/bin/bash

echo "====================================="
echo "  🧠 AIMANA API - Instalador Linux/Mac"
echo "====================================="
echo

# URL correta
ZIP_URL="https://github.com/aimana-ai/AcoTubo_POC/archive/refs/heads/main.zip"
ZIP_FILE="aimana_api.zip"
EXTRACT_FOLDER="AcoTubo_POC-main"

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null
then
    echo "❌ Docker não está instalado ou não está no PATH."
    exit 1
fi

# Baixar o projeto
echo "⏬ Baixando a API do GitHub..."
curl -L -o "$ZIP_FILE" "$ZIP_URL"

if [ ! -f "$ZIP_FILE" ]; then
    echo "❌ Falha ao baixar o projeto. Verifique a URL ou sua conexão."
    exit 1
fi

# Descompactar
echo "📦 Extraindo arquivos..."
unzip -o "$ZIP_FILE" > /dev/null

# Entrar na pasta
cd "$EXTRACT_FOLDER" || { echo "❌ Erro ao acessar a pasta $EXTRACT_FOLDER."; exit 1; }

# Subir a API com Docker Compose (compatível com versões antigas e novas do Docker)
echo "🐳 Iniciando a API com Docker Compose..."

if command -v docker-compose &> /dev/null; then
    docker-compose up --build -d
else
    docker compose up --build -d
fi

if [ $? -eq 0 ]; then
    echo
    echo "✅ API AIMANA iniciada com sucesso!"
    echo "🌐 Acesse: http://localhost:8000/docs"
else
    echo "❌ Erro ao subir a API. Verifique se o Docker está rodando."
fi

echo
