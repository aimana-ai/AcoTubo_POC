#uvicorn app.main:app --reload

from fastapi import FastAPI, UploadFile, File, Form, Request

from app.schemas import RegressorInput

from pydantic import ValidationError

import pandas as pd
import numpy as np
import json

import os
import joblib


#App 
app = FastAPI(
    title="🧠 AIMANA - AçoTubo ⚙",
    description="🎯 **API para previsão de Margem, Taxa de Conversão e sugestão de preço(s)** 🎯"
)


#home
@app.get("/", tags= ['Home 🏠'], description= 'Endpoint principal para verificar se a API está ativa.')
def read_root():
    return {"message": "🔑 API para previsão de Margem, Taxa de Conversão e sugestão de preço(s). Acesse /docs para testar."}


#endpoints
# @app.post("/upload_csv/",
#           tags= ["📨 Carregar arquivo .csv atualizado 📨"],
#           description= "Endpoint para *upload* do .csv contendo dados atualizados para consulta do Endpoint de predição")

# async def upload_csv(csv_file: UploadFile = File(...)):
#     contents = await csv_file.read()
#     with open("data/arquivo_base_acotubo.csv", "wb") as f:
#         f.write(contents)
#     return {"message": "Arquivo salvo com sucesso."}



@app.post("/predict", 
          tags=["📊 Realizar Previsões 📊"],
          description= '📈 Endpoint para prever Margem, Taxa de Conversão e sugestão de preço(s) 💰')

async def predict(input: RegressorInput, request: Request):
    #lendo .csv inputado no Endpoint acima
    df= pd.read_csv('data/poc_acotubo_17_06_2025.csv')
    #removendo aspas duplas e substituindo por aspas simples para tentar corrigir erro da API (json input no formato incorreto)
    df['ProdutoDescricao']= df['ProdutoDescricao'].str.replace('"', "'", regex= False)
    
    #load models
    conversion_model = joblib.load(os.path.join("app", "models", "2_poc_conversion_model_rf_df_16062025.pkl"))
    margem_model = joblib.load(os.path.join("app", "models", "2_poc_margem_model_xgb_df_16062025.pkl"))
    
    #descontos
    range_descontos = np.arange(-5, 20.5, 0.2)

    #inputs
    user_inputs = {
        'Year': input.Year,
        'day_of_year': input.day_of_year,
        'FaixaPeso': input.FaixaPeso,
        'ProdutoFamilia': input.ProdutoFamilia,
        'ProdutoDescricao': input.ProdutoDescricao,
        'ProdutoGrupoSOP': input.ProdutoGrupoSOP,
        'Canal': input.Canal,
        'EmpresaNome': input.EmpresaNome,
        'ClienteCNPJCPF': input.ClienteCNPJCPF, 
        'nuPrecoGerenciaTotal': input.nuPrecoGerenciaTotal
    }

    user_inputs2 = {
        'totalSold': df[df['ProdutoDescricao'] == user_inputs["ProdutoDescricao"]]['totalSold'].iloc[-1],
        'TotalQuoted': df[df['ProdutoDescricao'] == user_inputs["ProdutoDescricao"]]['TotalQuoted'].iloc[-1]  
    }


    df_inputs = pd.DataFrame([{
        **user_inputs,
        **user_inputs2,
        'Desconto': desconto
    } for desconto in range_descontos])


    conversion_predictions = conversion_model.predict(df_inputs)
    margem_predictions = margem_model.predict(df_inputs)


    #predictions dataframe
    df_results = pd.DataFrame({
    'Desconto' : range_descontos,
    'ConversionRate_Predicted': conversion_predictions,
    'Margem_Predicted': margem_predictions
    })

    #extraindo somente os registros que possuem um conversion rate acima do limite calculado em relação ao ultimo registro do produto
    limit = df[df['ProdutoDescricao'] == user_inputs["ProdutoDescricao"]].iloc[-1]['ConversionRate_%'] * input.limite

    #extraindo o valor de máximo de margem encontrado
    max_margem = df_results[df_results['ConversionRate_Predicted'] >= limit]['Margem_Predicted'].max()

    #descontos encontrados 
    desconto_encontrado = df_results[df_results['Margem_Predicted'] == max_margem]['Desconto'].tolist()

    #conversion rate encontrado (dentro da margem maxima)
    conversion_rate_encontrado = df_results[df_results['Margem_Predicted'] == max_margem]['ConversionRate_Predicted'].values[0]


    range_preco= []
    for desconto in desconto_encontrado:
        if desconto < 0:
            preco= input.nuPrecoGerenciaTotal - input.nuPrecoGerenciaTotal*(desconto/100)
            range_preco.append(preco)
        else:
            preco= input.nuPrecoGerenciaTotal - input.nuPrecoGerenciaTotal*(desconto/100)
            range_preco.append(preco)
    
    
    #resultados
    resultados = {
        "Margem Máxima encontrada": float(max_margem), 
        "Conversion Rate encontrado": float(conversion_rate_encontrado), 
        "Desconto(s) encontrado(s)": [float(d) for d in desconto_encontrado],
        "Preço original": float(input.nuPrecoGerenciaTotal),
        "Preço(s) encontrado(s)": [float(p) for p in range_preco]
    }
    
    
    #printando resultados
    return resultados