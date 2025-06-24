import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="AIMANA - AçoTubo Preditor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .info-box {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 AIMANA - AçoTubo Preditor</h1>
    <p>Sistema Inteligente de Previsão de Margem, Taxa de Conversão e Preços</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation and info
with st.sidebar:
    st.markdown("### 📊 Informações do Dashboard")
    st.markdown("**Data Atual:** " + datetime.now().strftime("%d de %B de %Y"))
    st.markdown("**Status da API:** 🟢 Online")
    
    st.markdown("---")
    st.markdown("### ℹ️ Como Usar")
    st.markdown("""
    1. **Preencha os campos obrigatórios** abaixo
    2. **Selecione os detalhes do produto** nos menus suspensos
    3. **Clique em 'Gerar Previsão'** para obter resultados
    4. **Revise as previsões** na seção de resultados
    """)
    
    st.markdown("---")
    st.markdown("### 📈 O Que Você Receberá")
    st.markdown("""
    - **Margem Prevista** encontrada
    - **Taxa de Conversão Prevista**
    - **Descontos Ótimos** sugeridos
    - **Preços Recomendados** para máximo lucro
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Sobre os Descontos")
    st.markdown("""
    **Desconto Negativo (-):** Aumento no preço
    **Desconto Positivo (+):** Redução no preço
    
    Exemplo: -5% = aumento de 5% no preço
    Exemplo: +10% = redução de 10% no preço
    """)

# Load data with better error handling
@st.cache_data
def load_data():
    try:
        with st.spinner("🔄 Carregando dataset..."):
            df = pd.read_csv('data/poc_acotubo_17_06_2025.csv')
            st.success("✅ Dataset carregado com sucesso!")
            return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dataset: {e}")
        return None

# Main content area
st.markdown("### 🎯 Parâmetros de Previsão")

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["📋 Configurações Básicas", "🏭 Detalhes do Produto", "💰 Precificação"])

with tab1:
    st.markdown("#### Configuração Básica")
    col1_1, col1_2 = st.columns(2)
    
    with col1_1:
        limite = st.slider(
            "Limite da Taxa de Conversão",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            step=0.05,
            help="Taxa de conversão mínima aceitável (0.0 a 1.0)"
        )
        Year = st.number_input(
            "Ano",
            min_value=2020,
            max_value=2030,
            value=2025,
            help="Ano alvo para a previsão"
        )
    
    with col1_2:
        day_of_year = st.number_input(
            "Dia do Ano",
            min_value=1,
            max_value=366,
            value=datetime.now().timetuple().tm_yday,
            help="Dia do ano (1-366)"
        )

with tab2:
    st.markdown("#### Informações do Produto")
    
    # Load data
    df = load_data()
    
    if df is not None:
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            FaixaPeso = st.selectbox(
                "Faixa de Peso",
                sorted(df['FaixaPeso'].unique()),
                help="Selecione a faixa de peso do produto"
            )
            ProdutoFamilia = st.selectbox(
                "Família do Produto",
                sorted(df['ProdutoFamilia'].unique()),
                help="Selecione a família do produto"
            )
            ProdutoGrupoSOP = st.selectbox(
                "Grupo SOP do Produto",
                sorted(df['ProdutoGrupoSOP'].unique()),
                help="Selecione o grupo SOP do produto"
            )
        
        with col2_2:
            Canal = st.selectbox(
                "Canal de Vendas",
                sorted(df['Canal'].unique()),
                help="Selecione o canal de vendas"
            )
            EmpresaNome = st.selectbox(
                "Nome da Empresa",
                sorted(df['EmpresaNome'].unique()),
                help="Selecione a empresa"
            )
            ClienteCNPJCPF = st.selectbox(
                "CNPJ/CPF do Cliente",
                sorted(df['ClienteCNPJCPF'].unique()),
                help="Selecione o cliente"
            )
        
        # Product description with search functionality
        st.markdown("#### Descrição do Produto")
        produto_options = sorted(df['ProdutoDescricao'].unique())
        ProdutoDescricao = st.selectbox(
            "Selecionar Produto",
            produto_options,
            help="Escolha a descrição específica do produto",
            index=0 if len(produto_options) > 0 else None
        )

with tab3:
    st.markdown("#### Informações de Preço")
    nuPrecoGerenciaTotal = st.number_input(
        "Preço Total de Gerência (R$)",
        min_value=0.0,
        value=1000.0,
        step=10.0,
        help="Digite o preço total de gerência"
    )

# Prediction button and results
st.markdown("---")
st.markdown("### 🚀 Gerar Previsão")

# Create a centered button
col_button1, col_button2, col_button3 = st.columns([1, 2, 1])
with col_button2:
    predict_button = st.button(
        "🎯 Gerar Previsão",
        type="primary",
        use_container_width=True
    )

if predict_button:
    if df is None:
        st.error("❌ Não é possível gerar previsão: Dataset não carregado")
    else:
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("🔄 Preparando dados...")
            elif i < 60:
                status_text.text("🧠 Executando modelos de previsão...")
            elif i < 90:
                status_text.text("📊 Analisando resultados...")
            else:
                status_text.text("✅ Finalizando previsão...")
        
        # Replace double quotes with single quotes
        ProdutoDescricao_processed = ProdutoDescricao.replace('"', "'")
        
        payload = {
            "limite": limite,
            "Year": int(Year),
            "day_of_year": int(day_of_year),
            "FaixaPeso": FaixaPeso,
            "ProdutoFamilia": ProdutoFamilia,
            "ProdutoDescricao": ProdutoDescricao_processed,
            "ProdutoGrupoSOP": ProdutoGrupoSOP,
            "Canal": Canal,
            "EmpresaNome": EmpresaNome,
            "ClienteCNPJCPF": ClienteCNPJCPF,
            "nuPrecoGerenciaTotal": nuPrecoGerenciaTotal
        }
        
        try:
            with st.spinner("🔄 Enviando requisição para a API..."):
                response = requests.post("http://localhost:8000/predict", json=payload, timeout=30)
            
            progress_bar.progress(100)
            status_text.text("✅ Previsão concluída!")
            
            if response.status_code == 200:
                result = response.json()
                
                # Display results in a beautiful format
                st.markdown("### 📈 Resultados da Previsão")
                
                # Create metric cards
                col_result1, col_result2, col_result3, col_result4 = st.columns(4)
                
                with col_result1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>💰 Margem Prevista</h4>
                        <h2>{result['Margem Máxima encontrada']:.2f}%</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_result2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>📊 Taxa de Conversão Prevista</h4>
                        <h2>{result['Conversion Rate encontrado']:.2f}%</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_result3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>🎯 Desconto Ótimo</h4>
                        <h2>{result['Desconto(s) encontrado(s)'][0]:.1f}%</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_result4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>💵 Preço Recomendado</h4>
                        <h2>R$ {result['Preço(s) encontrado(s)'][0]:.2f}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detailed results
                st.markdown("### 📋 Análise Detalhada")
                
                col_detail1, col_detail2 = st.columns(2)
                
                with col_detail1:
                    st.markdown("#### Original vs Recomendado")
                    st.write(f"**Preço Original:** R$ {result['Preço original']:,.2f}")
                    st.write(f"**Preço Recomendado:** R$ {result['Preço(s) encontrado(s)'][0]:,.2f}")
                    st.write(f"**Diferença de Preço:** R$ {result['Preço(s) encontrado(s)'][0] - result['Preço original']:,.2f}")
                
                with col_detail2:
                    st.markdown("#### Todas as Opções de Desconto")
                    for i, discount in enumerate(result['Desconto(s) encontrado(s)']):
                        if discount < 0:
                            st.write(f"**Opção {i+1}:** Aumento de {abs(discount):.1f}% no preço")
                        else:
                            st.write(f"**Opção {i+1}:** Redução de {discount:.1f}% no preço")
                
                # Success message
                st.markdown("""
                <div class="success-message">
                    <strong>✅ Previsão concluída com sucesso!</strong><br>
                    O sistema analisou seus parâmetros e forneceu recomendações de preços ótimos.
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div class="error-message">
                    <strong>❌ Erro na API {response.status_code}</strong><br>
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
        except requests.exceptions.Timeout:
            st.markdown("""
            <div class="error-message">
                <strong>⏰ Timeout da Requisição</strong><br>
                A requisição para a API demorou muito. Tente novamente.
            </div>
            """, unsafe_allow_html=True)
        except requests.exceptions.ConnectionError:
            st.markdown("""
            <div class="error-message">
                <strong>🔌 Erro de Conexão</strong><br>
                Não é possível conectar à API. Verifique se o backend está rodando.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="error-message">
                <strong>❌ Erro Inesperado</strong><br>
                {str(e)}
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🧠 AIMANA - AçoTubo Preditor | Alimentado por Machine Learning</p>
    <p>Para suporte, entre em contato com a equipe de desenvolvimento</p>
</div>
""", unsafe_allow_html=True)
