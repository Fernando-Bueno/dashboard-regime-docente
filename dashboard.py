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
            default=[],
            placeholder="Selecionar..."
        )
        
        # Filtro de Departamento (Dependente do Curso)
        if filtro_curso:
            # Se houver curso selecionado, filtrar departamentos apenas desse(s) curso(s)
            pattern_curso = '|'.join(filtro_curso)
            df_curso_filtrado = df[df['Curso'].astype(str).str.contains(pattern_curso, na=False)]
            deptos_unicos = sorted(df_curso_filtrado['Departamento'].dropna().unique().astype(str))
        else:
            # Se não houver curso selecionado, mostrar todos
            deptos_unicos = sorted(df['Departamento'].dropna().unique().astype(str))
            
        todos_deptos = set()
        for d in deptos_unicos:
            for sub_d in d.split('\n'):
                if sub_d.strip():
                    todos_deptos.add(sub_d.strip())
                    
        filtro_depto = st.sidebar.multiselect(
            "Filtrar por Departamento",
            options=sorted(list(todos_deptos)),
            default=[],
            placeholder="Selecionar..."
        )
        
        # Filtro de CH Sala de aula > 0
        filtro_ch_sala = st.sidebar.toggle("Docentes em aula")
        
        # Aplicar Filtros
        df_filtrado = df.copy()
        
        if filtro_curso:
            # Filtra se a string da coluna contém ALGUM dos cursos selecionados
            pattern = '|'.join(filtro_curso)
            df_filtrado = df_filtrado[df_filtrado['Curso'].astype(str).str.contains(pattern, na=False)]
            
        if filtro_depto:
            pattern_depto = '|'.join(filtro_depto)
            df_filtrado = df_filtrado[df_filtrado['Departamento'].astype(str).str.contains(pattern_depto, na=False)]
            
        if filtro_ch_sala:
            if 'CH Sala de aula' in df_filtrado.columns:
                 df_filtrado = df_filtrado[pd.to_numeric(df_filtrado['CH Sala de aula'], errors='coerce') > 0]
            
        # --- KPIs ---
        # Definir colunas para os KPIs (2 linhas de 3 colunas)
        # Linha 1: Docentes, Titulados, Prod >= 9
        # Linha 2: Prod 8, Prod 6-7, Prod <= 5
        
        # Calcular métricas de Produção Científica
        if 'Produção Científica' in df_filtrado.columns:
            # Garantir que é numérico
            prod_cientifica = pd.to_numeric(df_filtrado['Produção Científica'], errors='coerce').fillna(0)
        else:
            prod_cientifica = pd.Series([0] * len(df_filtrado))

        total_docentes = len(df_filtrado)
        
        # Cálculos de Produção
        prod_9_mais = len(prod_cientifica[prod_cientifica >= 9])
        pct_9_mais = (prod_9_mais / total_docentes * 100) if total_docentes > 0 else 0
        
        prod_8 = len(prod_cientifica[prod_cientifica == 8])
        pct_8 = (prod_8 / total_docentes * 100) if total_docentes > 0 else 0
        
        prod_6_7 = len(prod_cientifica[(prod_cientifica >= 6) & (prod_cientifica <= 7)])
        pct_6_7 = (prod_6_7 / total_docentes * 100) if total_docentes > 0 else 0
        
        prod_5_menos = len(prod_cientifica[prod_cientifica <= 5])
        pct_5_menos = (prod_5_menos / total_docentes * 100) if total_docentes > 0 else 0

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
            # Contagem Doutores (D) + Mestres (M)
            df_titulados = df_filtrado[df_filtrado['Titulação'].isin(['D', 'M', 'E'])]
            total_titulados_geral = len(df_titulados)
            qtd_qualificados = len(df_filtrado[df_filtrado['Titulação'].isin(['D', 'M'])])
            pct_qualificados = (qtd_qualificados / total_titulados_geral * 100) if total_titulados_geral > 0 else 0
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.8rem; color: #666;">Doutores e Mestres</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                    {qtd_qualificados} <span style="font-size: 1rem;">({pct_qualificados:.1f}%)</span>
                </div>
                <div style="font-size: 1.2rem;">🎓</div>
            </div>
            """, unsafe_allow_html=True)

        with kpi3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.8rem; color: #666;">Produção ≥ 9</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                    {prod_9_mais} <span style="font-size: 1rem;">({pct_9_mais:.1f}%)</span>
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
                    {prod_8} <span style="font-size: 1rem;">({pct_8:.1f}%)</span>
                </div>
                <div style="font-size: 1.2rem;"><span style="color: #C0C0C0; text-shadow: 0 0 1px black;">★</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi5:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.8rem; color: #666;">Produção 6 ou 7</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                    {prod_6_7} <span style="font-size: 1rem;">({pct_6_7:.1f}%)</span>
                </div>
                <div style="font-size: 1.2rem;"><span style="color: #CD7F32; text-shadow: 0 0 1px black;">★</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi6:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.8rem; color: #666;">Produção ≤ 5</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #00ACA1;">
                    {prod_5_menos} <span style="font-size: 1rem;">({pct_5_menos:.1f}%)</span>
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
        
        # Mapa de nomes legíveis
        map_regime = {'H': 'Horista (H)', 'P': 'Parcial (P)', 'I': 'Integral (I)'}
        regime_counts['Legenda'] = regime_counts['Regime'].map(map_regime)

        # Forçar ordem específica
        ordem_regime = ['Horista (H)', 'Parcial (P)', 'Integral (I)']
        
        cores_regime = {
            'Horista (H)': '#A39161', # Dourado
            'Parcial (P)': '#00ACA1', # Verde FCM
            'Integral (I)': '#004D40' # Verde Escuro
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
            fig_reg_bar.update_traces(textfont=dict(color='white', weight='bold'))
            
            # Ajuste do eixo Y para ter margem superior
            max_y = regime_counts['Quantidade'].max()
            margem_y = max_y * 1.15  # 15% de margem
            fig_reg_bar.update_layout(
                showlegend=False,
                yaxis=dict(range=[0, margem_y])
            )
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
            fig_tit_bar.update_traces(textfont=dict(color='white', weight='bold'))
            
            # Ajuste do eixo Y para ter margem superior
            max_y_tit = titulacao_counts['Quantidade'].max()
            margem_y_tit = max_y_tit * 1.15
            fig_tit_bar.update_layout(
                showlegend=False,
                yaxis=dict(range=[0, margem_y_tit])
            )
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
            fig_tit_pie.update_traces(textfont=dict(color='white', weight='bold'))
            st.plotly_chart(fig_tit_pie, use_container_width=True)

        st.markdown("---")

        # --- GRÁFICOS DE LATTES ---
        if 'Atualização Lattes' in df_filtrado.columns:
            st.subheader("📅 Atualização Lattes")
            col_lat1, col_lat2 = st.columns(2)
            
            lattes_counts = df_filtrado['Atualização Lattes'].value_counts().reset_index()
            lattes_counts.columns = ['Status', 'Quantidade']
            
            # Cores personalizadas
            cores_lattes = {
                'Atualizado': '#00ACA1',     # Verde
                'Desatualizado': '#E57373',  # Vermelho claro/suave para alerta
                'Não Localizado': '#9E9E9E', # Cinza
                'Sem Data': '#9E9E9E'        # Fallback
            }
            
            with col_lat1:
                # Gráfico de Coluna
                fig_lat_bar = px.bar(
                    lattes_counts,
                    x='Status',
                    y='Quantidade',
                    text='Quantidade',
                    color='Status',
                    color_discrete_map=cores_lattes,
                    title="Quantitativo por Status Lattes"
                )
                fig_lat_bar.update_traces(textfont=dict(color='white', weight='bold'))
                
                # Ajuste eixo Y
                max_y_lat = lattes_counts['Quantidade'].max() if not lattes_counts.empty else 0
                margem_y_lat = max_y_lat * 1.15
                fig_lat_bar.update_layout(
                    showlegend=False,
                    yaxis=dict(range=[0, margem_y_lat])
                )
                st.plotly_chart(fig_lat_bar, use_container_width=True)
                
            with col_lat2:
                # Gráfico de Rosca
                fig_lat_pie = px.pie(
                    lattes_counts,
                    values='Quantidade',
                    names='Status',
                    color='Status',
                    color_discrete_map=cores_lattes,
                    hole=0.5,
                    title="Percentual de Atualização"
                )
                fig_lat_pie.update_traces(textfont=dict(color='white', weight='bold'))
                st.plotly_chart(fig_lat_pie, use_container_width=True)

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
