import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Configuração da Página
st.set_page_config(
    page_title="Dashboard Regime Docente FCM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS Personalizado
st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .st-emotion-cache-16txtl3 {
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #00ACA1;
        }
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
    </style>
""", unsafe_allow_html=True)

# Função de Carregamento de Dados
@st.cache_data
def carregar_dados(caminho_arquivo):
    try:
        # Tenta ler a aba 'regime_geral', se falhar tenta a primeira aba
        try:
            df = pd.read_excel(caminho_arquivo, sheet_name='regime_geral', engine='openpyxl')
        except:
            df = pd.read_excel(caminho_arquivo, sheet_name=0, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return None

# Título e Header
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    try:
        if os.path.exists("CMMG_LogoFaculdade-Alta.png"):
            st.image("CMMG_LogoFaculdade-Alta.png", width=100)
        else:
            st.warning("Logo não encontrada")
    except Exception:
        pass

with col_titulo:
    st.title("Dashboard de Análise de Regime Docente 2025-2")
    st.markdown("Faculdade de Ciências Médicas de Minas Gerais - FCM-MG")

st.markdown("---")

# Lógica de Seleção de Arquivo
arquivo_path = None

# 1. Tentar pegar argumento da linha de comando
if len(sys.argv) > 1:
    potential_path = sys.argv[1]
    if os.path.exists(potential_path) and potential_path.endswith(('.xlsx', '.xls')):
        arquivo_path = potential_path

# 2. Se não houver argumento válido, mostrar uploader
if not arquivo_path:
    uploaded_file = st.sidebar.file_uploader("📂 Carregar Relatório (Excel)", type=['xlsx', 'xls'])
    if uploaded_file:
        arquivo_path = uploaded_file

# Se temos um arquivo, processamos
if arquivo_path:
    df = carregar_dados(arquivo_path)
    
    if df is not None:
        # --- FILTROS ---
        st.sidebar.header("🔍 Filtros")
        
        # Filtro de Curso
        cursos_unicos = sorted(df['Curso'].dropna().unique().astype(str))
        # Tratamento para separar cursos se estiverem na mesma célula (quebra de linha)
        todos_cursos = set()
        for c in cursos_unicos:
            for sub_c in c.split('\n'):
                if sub_c.strip():
                    todos_cursos.add(sub_c.strip())
        
        filtro_curso = st.sidebar.multiselect(
            "Filtrar por Curso",
            options=sorted(list(todos_cursos)),
            default=[]
        )
        
        # Filtro de Departamento
        deptos_unicos = sorted(df['Departamento'].dropna().unique().astype(str))
        todos_deptos = set()
        for d in deptos_unicos:
            for sub_d in d.split('\n'):
                if sub_d.strip():
                    todos_deptos.add(sub_d.strip())
                    
        filtro_depto = st.sidebar.multiselect(
            "Filtrar por Departamento",
            options=sorted(list(todos_deptos)),
            default=[]
        )
        
        # Aplicar Filtros
        df_filtrado = df.copy()
        
        if filtro_curso:
            # Filtra se a string da coluna contém ALGUM dos cursos selecionados
            pattern = '|'.join(filtro_curso)
            df_filtrado = df_filtrado[df_filtrado['Curso'].astype(str).str.contains(pattern, na=False)]
            
        if filtro_depto:
            pattern_depto = '|'.join(filtro_depto)
            df_filtrado = df_filtrado[df_filtrado['Departamento'].astype(str).str.contains(pattern_depto, na=False)]
            
        # --- KPIs ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total de Docentes", len(df_filtrado))
            
        with col2:
            # Contagem Doutores (D) + Mestres (M)
            # Percentual sobre Total de Titulados (D + M + E)
            
            df_titulados = df_filtrado[df_filtrado['Titulação'].isin(['D', 'M', 'E'])]
            total_titulados = len(df_titulados)
            
            qtd_qualificados = len(df_filtrado[df_filtrado['Titulação'].isin(['D', 'M'])])
            
            pct_qualificados = (qtd_qualificados / total_titulados * 100) if total_titulados > 0 else 0
            
            st.metric("Doutores e Mestres", f"{qtd_qualificados} ({pct_qualificados:.1f}%)", help="Percentual em relação ao total de Doutores, Mestres e Especialistas")

        st.markdown("---")

        # --- GRÁFICOS DE REGIME ---
        st.subheader("📌 Regime Docente")
        col_reg1, col_reg2 = st.columns(2)
        
        regime_counts = df_filtrado['Regime'].value_counts().reset_index()
        regime_counts.columns = ['Regime', 'Quantidade']
        
        # Mapa de nomes legíveis
        map_regime = {'H': 'Horista (H)', 'P': 'Parcial (P)', 'I': 'Integral (I)'}
        regime_counts['Legenda'] = regime_counts['Regime'].map(map_regime)
        
        # Forçar ordem específica
        ordem_regime = ['Horista (H)', 'Parcial (P)', 'Integral (I)']
                
        cores_regime = {
            'Horista (H)': '#A39161', # Dourado
            'Parcial (P)': '#00ACA1', # Verde FCM
            'Integral (I)': '#87CEEB' # Azul Claro
        }

        with col_reg1:
            # Gráfico de Coluna (Barra)
            fig_reg_bar = px.bar(
                regime_counts,
                x='Legenda',
                y='Quantidade',
                text='Quantidade',
                color='Legenda',
                color_discrete_map=cores_regime,
                category_orders={'Legenda': ordem_regime},
                title="Quantitativo por Regime"
            )
            fig_reg_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_reg_bar, use_container_width=True)
            
        with col_reg2:
            # Gráfico de Rosca
            fig_reg_pie = px.pie(
                regime_counts, 
                values='Quantidade', 
                names='Legenda',
                color='Legenda',
                color_discrete_map=cores_regime,
                category_orders={'Legenda': ordem_regime},
                hole=0.5,
                title="Percentual por Regime"
            )
            st.plotly_chart(fig_reg_pie, use_container_width=True)

        st.markdown("---")

        # --- GRÁFICOS DE TITULAÇÃO ---
        st.subheader("🎓 Titulação Docente")
        col_tit1, col_tit2 = st.columns(2)
        
        titulacao_counts = df_filtrado['Titulação'].value_counts().reset_index()
        titulacao_counts.columns = ['Titulação', 'Quantidade']
        
        map_titulacao = {'E': 'Especialista', 'M': 'Mestre', 'D': 'Doutor', 'G': 'Graduado'}
        titulacao_counts['Legenda'] = titulacao_counts['Titulação'].map(map_titulacao).fillna(titulacao_counts['Titulação'])
        
        # Definir cores consistentes se desejar, ou usar sequência
        
        with col_tit1:
            # Gráfico de Coluna (Barra)
            fig_tit_bar = px.bar(
                titulacao_counts,
                x='Legenda',
                y='Quantidade',
                text='Quantidade',
                color='Legenda',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                title="Quantitativo por Titulação"
            )
            fig_tit_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_tit_bar, use_container_width=True)
            
        with col_tit2:
            # Gráfico de Rosca
            fig_tit_pie = px.pie(
                titulacao_counts,
                values='Quantidade',
                names='Legenda',
                color='Legenda',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.5,
                title="Percentual por Titulação"
            )
            st.plotly_chart(fig_tit_pie, use_container_width=True)

        # --- TABELA DE DADOS ---
        with st.expander("Ver Dados Brutos"):
            st.dataframe(df_filtrado, use_container_width=True)

else:
    # Tela inicial sem arquivo
    st.info("👆 Por favor, carregue um arquivo Excel gerado pelo sistema ou execute através da aplicação principal.")
    
    # Exemplo de como usar
    st.markdown("""
    ### Como usar:
    1. Gere o relatório no sistema Desktop.
    2. Arraste o arquivo `Regime_Data...xlsx` para a barra lateral.
    3. Explore os dados!
    """)










