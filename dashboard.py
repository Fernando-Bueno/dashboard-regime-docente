import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
        /* Estilo da Sidebar */
        [data-testid="stSidebar"] {
            background-color: #00ACA1;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: white !important;
        }
        [data-testid="stSidebar"] label {
            color: white !important;
        }
        [data-testid="stSidebar"] .stCheckbox label span p {
            color: white !important;
        }
        /* Forçar TODAS as fontes de texto da sidebar para branco */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] div, 
        [data-testid="stSidebar"] label {
            color: white !important;
        }

        /* Especificamente para o Toggle Switch */
        [data-testid="stSidebar"] .stToggle label p {
            color: white !important;
            background-color: transparent !important;
        }
        [data-testid="stSidebar"] .stToggle div[data-testid="stMarkdownContainer"] > p {
            color: white !important;
        }

        /* Cor do Toggle Switch quando ativo (checked) - Focado apenas no elemento switch */
        [data-testid="stSidebar"] .stToggle input:checked + div {
             background-color: white !important;
             border-color: white !important;
        }

        /* Bolinha (Thumb) quando ativo */
        [data-testid="stSidebar"] .stToggle input:checked + div::after {
            background-color: #A39161 !important;
        }
        
        /* Remover qualquer sombra ou outline vermelho */
        [data-testid="stSidebar"] .stToggle input:focus + div,
        [data-testid="stSidebar"] .stToggle input:active + div {
            box-shadow: none !important;
            outline: none !important;
        }
        /* Estilo das Tags do Multiselect */
        span[data-baseweb="tag"] {
            background-color: #9E9E9E !important; /* Cinza claro */
        }
        span[data-baseweb="tag"] span {
            color: white !important;
        }
        
        /* Fundo transparente para o File Uploader (Drag and drop) na Sidebar */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
            background-color: transparent !important;
            border: 1px dashed white !important; /* Opcional: borda branca para manter visibilidade */
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div {
             background-color: transparent !important;
        }
        /* Garantir que o ícone e texto de upload sejam brancos (Exceto botão) */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section span,
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section div,
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section small {
             color: white !important;
        }

        /* Tradução "Drag and drop file here" - Focado no primeiro span */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div > div > span:first-of-type {
            color: transparent !important;
            position: relative;
        }
        
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div > div > span:first-of-type::after {
            content: "Arraste e solte o arquivo aqui";
            color: white !important;
            position: absolute;
            left: 50%;
            top: 0;
            transform: translateX(-50%);
            white-space: nowrap;
            width: max-content;
        }

        /* Tradução "Limit 200MB per file" - Suporte para small e segundo span */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div > div > small,
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div > div > span:nth-of-type(2) {
            color: transparent !important;
            position: relative;
        }
        
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div > div > small::after,
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div > div > span:nth-of-type(2)::after {
            content: "Limite por arquivo 200MB";
            color: white !important;
            position: absolute;
            left: 50%;
            top: 0;
            transform: translateX(-50%);
            white-space: nowrap;
            width: max-content;
        }

        /* Botão Browse files com fundo Dourado e Texto Personalizado */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section button {
             background-color: #A39161 !important;
             color: transparent !important; /* Esconde 'Browse files' */
             border: none !important;
             position: relative;
        }
        
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section button::after {
             content: "Buscar arquivo";
             color: white !important;
             font-size: 1rem;
             position: absolute;
             left: 50%;
             top: 50%;
             transform: translate(-50%, -50%);
             white-space: nowrap;
        }

        /* Hover do Botão Browse files */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section button:hover {
             background-color: white !important;
             color: transparent !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploader"] section button:hover::after {
             color: #808080 !important;
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

def calcular_kpis(df):
    if df is None:
        return {}
    
    total_docentes = len(df)
    
    if 'Produção Científica' in df.columns:
        prod_cientifica = pd.to_numeric(df['Produção Científica'], errors='coerce').fillna(0)
    else:
        prod_cientifica = pd.Series([0] * total_docentes)
        
    prod_9_mais = len(prod_cientifica[prod_cientifica >= 9])
    prod_8 = len(prod_cientifica[prod_cientifica == 8])
    prod_6_7 = len(prod_cientifica[(prod_cientifica >= 6) & (prod_cientifica <= 7)])
    prod_5_menos = len(prod_cientifica[prod_cientifica <= 5])
    
    if 'Titulação' in df.columns:
        df_titulados = df[df['Titulação'].isin(['D', 'M', 'E'])]
        total_titulados_geral = len(df_titulados)
        qtd_qualificados = len(df[df['Titulação'].isin(['D', 'M'])])
    else:
        total_titulados_geral = 0
        qtd_qualificados = 0
    
    return {
        'total_docentes': total_docentes,
        'qtd_qualificados': qtd_qualificados,
        'prod_9_mais': prod_9_mais,
        'prod_8': prod_8,
        'prod_6_7': prod_6_7,
        'prod_5_menos': prod_5_menos,
        'total_titulados_geral': total_titulados_geral
    }

def render_individual_view(df_filtrado):
    kpis = calcular_kpis(df_filtrado)
    total_docentes = kpis['total_docentes']
    
    pct_qualificados = (kpis['qtd_qualificados'] / kpis['total_titulados_geral'] * 100) if kpis['total_titulados_geral'] > 0 else 0
    pct_9_mais = (kpis['prod_9_mais'] / total_docentes * 100) if total_docentes > 0 else 0
    pct_8 = (kpis['prod_8'] / total_docentes * 100) if total_docentes > 0 else 0
    pct_6_7 = (kpis['prod_6_7'] / total_docentes * 100) if total_docentes > 0 else 0
    pct_5_menos = (kpis['prod_5_menos'] / total_docentes * 100) if total_docentes > 0 else 0

    # Linha 1 de KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #666;">Total de Docentes</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                {total_docentes}
            </div>
            <div style="font-size: 1.2rem; color: black;">👤</div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #666;">Doutores e Mestres</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                {kpis['qtd_qualificados']} <span style="font-size: 1rem;">({pct_qualificados:.1f}%)</span>
            </div>
            <div style="font-size: 1.2rem;">🎓</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #666;">Produção ≥ 9</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                {kpis['prod_9_mais']} <span style="font-size: 1rem;">({pct_9_mais:.1f}%)</span>
            </div>
            <div style="font-size: 1.2rem;">5️⃣ <span style="color: #FFD700; text-shadow: 0 0 2px black;">★</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Linha 2 de KPIs
    kpi4, kpi5, kpi6 = st.columns(3)
    
    with kpi4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #666;">Produção = 8</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                {kpis['prod_8']} <span style="font-size: 1rem;">({pct_8:.1f}%)</span>
            </div>
            <div style="font-size: 1.2rem;"><span style="color: #C0C0C0; text-shadow: 0 0 1px black;">★</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi5:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #666;">Produção 6 ou 7</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                {kpis['prod_6_7']} <span style="font-size: 1rem;">({pct_6_7:.1f}%)</span>
            </div>
            <div style="font-size: 1.2rem;"><span style="color: #CD7F32; text-shadow: 0 0 1px black;">★</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi6:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #666;">Produção ≤ 5</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                {kpis['prod_5_menos']} <span style="font-size: 1rem;">({pct_5_menos:.1f}%)</span>
            </div>
            <div style="font-size: 1.2rem;"><span style="color: #808080;">★</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- GRÁFICOS DE REGIME ---
    st.subheader("📌 Regime Docente")
    col_reg1, col_reg2 = st.columns(2)
    
    regime_counts = df_filtrado['Regime'].value_counts().reset_index()
    regime_counts.columns = ['Regime', 'Quantidade']
    
    map_regime = {'H': 'Horista (H)', 'P': 'Parcial (P)', 'I': 'Integral (I)'}
    regime_counts['Legenda'] = regime_counts['Regime'].map(map_regime)
    ordem_regime = ['Horista (H)', 'Parcial (P)', 'Integral (I)']
    cores_regime = {'Horista (H)': '#A39161', 'Parcial (P)': '#00ACA1', 'Integral (I)': '#004D40'}

    with col_reg1:
        fig_reg_bar = px.bar(
            regime_counts, x='Legenda', y='Quantidade', text='Quantidade',
            color='Legenda', color_discrete_map=cores_regime,
            category_orders={'Legenda': ordem_regime}, title="Quantitativo por Regime"
        )
        fig_reg_bar.update_traces(textfont=dict(color='white', weight='bold'))
        st.plotly_chart(fig_reg_bar, use_container_width=True)
        
    with col_reg2:
        fig_reg_pie = px.pie(
            regime_counts, values='Quantidade', names='Legenda',
            color='Legenda', color_discrete_map=cores_regime,
            category_orders={'Legenda': ordem_regime}, hole=0.5, title="Percentual por Regime"
        )
        fig_reg_pie.update_traces(textfont=dict(color='white', weight='bold'))
        st.plotly_chart(fig_reg_pie, use_container_width=True)

    st.markdown("---")

    # --- GRÁFICOS DE TITULAÇÃO ---
    st.subheader("🎓 Titulação Docente")
    col_tit1, col_tit2 = st.columns(2)
    
    titulacao_counts = df_filtrado['Titulação'].value_counts().reset_index()
    titulacao_counts.columns = ['Titulação', 'Quantidade']
    
    map_titulacao = {'E': 'Especialista', 'M': 'Mestre', 'D': 'Doutor', 'G': 'Graduado'}
    titulacao_counts['Legenda'] = titulacao_counts['Titulação'].map(map_titulacao).fillna(titulacao_counts['Titulação'])
    
    with col_tit1:
        fig_tit_bar = px.bar(
            titulacao_counts, x='Legenda', y='Quantidade', text='Quantidade',
            color='Legenda', color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Quantitativo por Titulação"
        )
        fig_tit_bar.update_traces(textfont=dict(color='white', weight='bold'))
        st.plotly_chart(fig_tit_bar, use_container_width=True)
        
    with col_tit2:
        fig_tit_pie = px.pie(
            titulacao_counts, values='Quantidade', names='Legenda',
            color='Legenda', color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.5, title="Percentual por Titulação"
        )
        fig_tit_pie.update_traces(textfont=dict(color='white', weight='bold'))
        st.plotly_chart(fig_tit_pie, use_container_width=True)

    st.markdown("---")
    
    # --- GRÁFICOS DE LATTES ---
    if 'Atualização Lattes' in df_filtrado.columns:
        st.subheader("📅 Atualização Lattes")
        col_lat1, col_lat2 = st.columns(2)
        
        lattes_counts = df_filtrado['Atualização Lattes'].value_counts().reset_index()
        lattes_counts.columns = ['Status', 'Quantidade']
        
        cores_lattes = {
            'Atualizado': '#00ACA1', 'Desatualizado': '#E57373', 
            'Não Localizado': '#9E9E9E', 'Sem Data': '#9E9E9E'
        }
        
        with col_lat1:
            fig_lat_bar = px.bar(
                lattes_counts, x='Status', y='Quantidade', text='Quantidade',
                color='Status', color_discrete_map=cores_lattes,
                title="Quantitativo por Status Lattes"
            )
            fig_lat_bar.update_traces(textfont=dict(color='white', weight='bold'))
            st.plotly_chart(fig_lat_bar, use_container_width=True)
            
        with col_lat2:
            fig_lat_pie = px.pie(
                lattes_counts, values='Quantidade', names='Status',
                color='Status', color_discrete_map=cores_lattes,
                hole=0.5, title="Percentual de Atualização"
            )
            fig_lat_pie.update_traces(textfont=dict(color='white', weight='bold'))
            st.plotly_chart(fig_lat_pie, use_container_width=True)

    # --- TABELA DE DADOS ---
    with st.expander("Ver Dados Brutos"):
        st.dataframe(df_filtrado, use_container_width=True)

def render_comparative_view(df_a, df_b, nome_a="Atual", nome_b="Anterior"):
    kpis_a = calcular_kpis(df_a)
    kpis_b = calcular_kpis(df_b)
    
    st.subheader(f"📊 Comparativo: {nome_a} vs {nome_b}")
    
    # KPIs Comparativos
    k1, k2, k3 = st.columns(3)
    k4, k5, k6 = st.columns(3)
    
    with k1:
        st.metric("Total de Docentes", kpis_a.get('total_docentes', 0), kpis_a.get('total_docentes', 0) - kpis_b.get('total_docentes', 0))
    with k2:
        st.metric("Mestres e Doutores", kpis_a.get('qtd_qualificados', 0), kpis_a.get('qtd_qualificados', 0) - kpis_b.get('qtd_qualificados', 0))
    with k3:
        st.metric("Produção ≥ 9", kpis_a.get('prod_9_mais', 0), kpis_a.get('prod_9_mais', 0) - kpis_b.get('prod_9_mais', 0))
        
    with k4:
        st.metric("Produção = 8", kpis_a.get('prod_8', 0), kpis_a.get('prod_8', 0) - kpis_b.get('prod_8', 0))
    with k5:
        st.metric("Produção 6-7", kpis_a.get('prod_6_7', 0), kpis_a.get('prod_6_7', 0) - kpis_b.get('prod_6_7', 0))
    with k6:
        st.metric("Produção ≤ 5", kpis_a.get('prod_5_menos', 0), kpis_a.get('prod_5_menos', 0) - kpis_b.get('prod_5_menos', 0))
        
    st.markdown("---")
    
    # Gráficos Comparativos (Side-by-Side)
    col_g1, col_g2 = st.columns(2)
    
    def prepare_comparison_data(df1, df2, col, map_dict=None):
        if col not in df1.columns or col not in df2.columns:
            st.warning(f"Coluna '{col}' não encontrada em ambos os arquivos para comparação.")
            return pd.DataFrame(columns=['Categoria', 'Quantidade', 'Origem'])
        c1 = df1[col].value_counts().reset_index()
        c1.columns = ['Categoria', 'Quantidade']
        c1['Origem'] = nome_a
        c2 = df2[col].value_counts().reset_index()
        c2.columns = ['Categoria', 'Quantidade']
        c2['Origem'] = nome_b
        full = pd.concat([c1, c2])
        if map_dict:
            full['Categoria'] = full['Categoria'].map(map_dict).fillna(full['Categoria'])
        return full

    # Regime
    map_regime = {'H': 'Horista (H)', 'P': 'Parcial (P)', 'I': 'Integral (I)'}
    df_regime = prepare_comparison_data(df_a, df_b, 'Regime', map_regime)
    
    with col_g1:
        fig_reg = px.bar(
            df_regime, x='Categoria', y='Quantidade', color='Origem', barmode='group', text='Quantidade',
            title="Comparativo de Regimes",
            color_discrete_map={nome_a: '#00ACA1', nome_b: '#A39161'},
            category_orders={'Origem': [nome_a, nome_b]}
        )
        fig_reg.update_traces(textfont=dict(color='white', weight='bold'))
        st.plotly_chart(fig_reg, use_container_width=True)

    # Titulação
    map_titulacao = {'E': 'Especialista', 'M': 'Mestre', 'D': 'Doutor', 'G': 'Graduado'}
    df_tit = prepare_comparison_data(df_a, df_b, 'Titulação', map_titulacao)
    
    with col_g2:
        fig_tit = px.bar(
            df_tit, x='Categoria', y='Quantidade', color='Origem', barmode='group', text='Quantidade',
            title="Comparativo de Titulação",
            color_discrete_map={nome_a: '#00ACA1', nome_b: '#A39161'},
            category_orders={'Origem': [nome_a, nome_b]}
        )
        fig_tit.update_traces(textfont=dict(color='white', weight='bold'))
        st.plotly_chart(fig_tit, use_container_width=True)

    # Lattes
    if 'Atualização Lattes' in df_a.columns and 'Atualização Lattes' in df_b.columns:
        st.markdown("---")
        df_lattes = prepare_comparison_data(df_a, df_b, 'Atualização Lattes')
        fig_lat = px.bar(
            df_lattes, x='Categoria', y='Quantidade', color='Origem', barmode='group', text='Quantidade',
            title="Comparativo Lattes",
            color_discrete_map={nome_a: '#00ACA1', nome_b: '#A39161'},
            category_orders={'Origem': [nome_a, nome_b]}
        )
        fig_lat.update_traces(textfont=dict(color='white', weight='bold'))
        st.plotly_chart(fig_lat, use_container_width=True)


# Título e Header
col_logo, col_titulo = st.columns([0.15, 0.85])
with col_logo:
    try:
        if os.path.exists("CMMG_LogoFaculdade-Alta.png"):
            st.image("CMMG_LogoFaculdade-Alta.png", width=100)
        else:
            st.warning("Logo não encontrada")
    except Exception:
        pass

with col_titulo:
    st.markdown("""
        <div style="display: flex; flex-direction: column; justify-content: center; height: 100px;">
            <h1 style="margin: 0; font-size: 2.4rem; color: #333;">Dashboard de Análise de Regime Docente 2026-1</h1>
            <p style="margin: 0; font-size: 1.1rem; color: #A39161;">Faculdade de Ciências Médicas de Minas Gerais - FCM-MG</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Menu de Navegação na Sidebar
modo_visualizacao = st.sidebar.radio("Modo de Visualização", ["Análise Individual", "Comparativo"])

df_principal = None
df_secundario = None

if modo_visualizacao == "Análise Individual":
    arquivo_path = None
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        arquivo_path = sys.argv[1]
    
    if not arquivo_path:
        uploaded_file = st.sidebar.file_uploader("📂 Carregar Relatório (Excel)", type=['xlsx', 'xls'])
        if uploaded_file:
            arquivo_path = uploaded_file
            
    if arquivo_path:
        df_principal = carregar_dados(arquivo_path)

else: # Comparativo
    st.sidebar.markdown("### Seleção de Arquivos")
    file_a = st.sidebar.file_uploader("📂 Arquivo Principal (Atual)", type=['xlsx', 'xls'], key="file_a")
    file_b = st.sidebar.file_uploader("📂 Arquivo Secundário (Anterior)", type=['xlsx', 'xls'], key="file_b")
    
    if file_a and file_b:
        df_principal = carregar_dados(file_a)
        df_secundario = carregar_dados(file_b)
    elif file_a or file_b:
        st.warning("Por favor, carregue ambos os arquivos para comparar.")

# Processamento e Renderização
if df_principal is not None:
    # --- FILTROS GLOBAIS ---
    st.sidebar.header("🔍 Filtros Globais")
    
    # Unificar opções de filtros se houver dois DFs
    dfs_para_filtros = [df_principal]
    if df_secundario is not None:
        dfs_para_filtros.append(df_secundario)
        
    todos_cursos = set()
    todos_deptos = set()
    
    for df in dfs_para_filtros:
        cursos = df['Curso'].dropna().unique().astype(str)
        for c in cursos:
            for sub_c in c.split('\n'):
                if sub_c.strip(): todos_cursos.add(sub_c.strip())
                
    filtro_curso = st.sidebar.multiselect("Filtrar por Curso", options=sorted(list(todos_cursos)))
    
    # Deptos dependem da seleção de curso (simplificado: mostra todos se curso selecionado)
    for df in dfs_para_filtros:
        if filtro_curso:
             pattern = '|'.join(filtro_curso)
             df_temp = df[df['Curso'].astype(str).str.contains(pattern, na=False)]
        else:
             df_temp = df
        
        deptos = df_temp['Departamento'].dropna().unique().astype(str)
        for d in deptos:
             for sub_d in d.split('\n'):
                if sub_d.strip(): todos_deptos.add(sub_d.strip())
                
    filtro_depto = st.sidebar.multiselect("Filtrar por Departamento", options=sorted(list(todos_deptos)))
    filtro_ch_sala = st.sidebar.toggle("Apenas Docentes em aula (>0h)")
    
    # Função para aplicar filtros
    def aplicar_filtros(df):
        out = df.copy()
        if filtro_curso:
            pattern = '|'.join(filtro_curso)
            out = out[out['Curso'].astype(str).str.contains(pattern, na=False)]
        if filtro_depto:
            pattern = '|'.join(filtro_depto)
            out = out[out['Departamento'].astype(str).str.contains(pattern, na=False)]
        if filtro_ch_sala and 'CH Sala de aula' in out.columns:
            out = out[pd.to_numeric(out['CH Sala de aula'], errors='coerce') > 0]
        return out

    # Renderização Condicional
    if modo_visualizacao == "Análise Individual":
        df_filtrado = aplicar_filtros(df_principal)
        render_individual_view(df_filtrado)
        
    elif modo_visualizacao == "Comparativo" and df_secundario is not None:
        df_a_filtrado = aplicar_filtros(df_principal)
        df_b_filtrado = aplicar_filtros(df_secundario)
        
        render_comparative_view(df_a_filtrado, df_b_filtrado)
        
else:
    if modo_visualizacao == "Análise Individual" and not arquivo_path:
        st.info("👆 Por favor, carregue um arquivo Excel para começar.")
    elif modo_visualizacao == "Comparativo" and not (file_a and file_b):
        st.info("👆 Por favor, carregue os dois arquivos Excel para comparação.")
