@echo off
title AIMANA - Setup Automático
color 0A

echo =====================================
echo   🧠 AIMANA API - Instalador Windows
echo =====================================
echo.

REM URL correta (sem espaço depois do igual)
set ZIP_URL=https://github.com/aimana-ai/AcoTubo_POC/archive/refs/heads/main.zip

REM Nome do arquivo zip e pasta correta
set ZIP_FILE=aimana_api.zip
set EXTRACT_FOLDER=AcoTubo_POC-main

REM Verificar Docker
docker --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker não está instalado ou não está no PATH.
    pause
    exit /b
)

REM Baixar
echo ⏬ Baixando a API do GitHub...
curl -L -o %ZIP_FILE% %ZIP_URL%

IF NOT EXIST %ZIP_FILE% (
    echo ❌ Falha ao baixar o projeto. Verifique a URL ou sua conexão.
    pause
    exit /b
)

REM Descompactar
echo 📦 Extraindo arquivos...
powershell -Command "Expand-Archive -Force '%ZIP_FILE%' ."

REM Entrar na pasta
cd %EXTRACT_FOLDER%

REM Subir API
echo 🐳 Iniciando a API com Docker Compose...
docker-compose up --build -d

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ API AIMANA iniciada com sucesso!
    echo 🌐 Acesse: http://localhost:8000/docs
) ELSE (
    echo ❌ Erro ao subir a API. Verifique se o Docker está rodando.
)

echo.
pause
