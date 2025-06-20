#!/bin/bash

echo "📦 Baixando a API AIMANA..."

# Baixar um zip do GitHub (ou outra URL pública com o projeto completo)
curl -L -o aimana_api.zip https://github.com/aimana-ai/AcoTubo_POC.git/archive/refs/heads/main.zip

# Descompactar
unzip aimana_api.zip
cd aimana-api-main  # ou o nome da pasta descompactada

echo "🐳 Subindo a API com Docker..."
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo "✅ API AIMANA iniciada com sucesso!"
    echo "🌐 Acesse: http://localhost:8000/docs"
else
    echo "❌ Erro ao iniciar a API. Verifique se o Docker está em execução."
fi
