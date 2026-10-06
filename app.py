import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Limita a largura para simular uma proporção de folha A4 na vertical
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS avançados para criar cartões pequenos, bonitos e coloridos
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 1200px; }
    
    .cartao {
        border-radius: 6px;
        padding: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        border-left: 5px solid;
    }
    
    /* Cores de fundo e borda (Mapa Verde/Vermelho) */
    .cartao-op { border-left-color: #28a745; background-color: #f2fff5; }
    .cartao-man { border-left-color: #dc3545; background-color: #fff5f5; }
    
    .titulo { font-size: 13px; font-weight: 700; color: #2c3e50; text-align: center; margin-bottom: 4px; }
    .status-badge { font-size: 10px; font-weight: bold; text-align: center; margin-bottom: 4px; }
    .txt-op { color: #28a745; }
    .txt-man { color: #dc3545; }
    
    .linha { border-top: 1px solid #e0e0e0; margin: 4px 0; }
    
    .info { font-size: 11px; color: #444; margin: 2px 0; display: flex; justify-content: space-between; }
    .info-alerta { font-size: 11px; color: #dc3545; font-weight: 600; margin: 2px 0; }
    .info-aviso { font-size: 11px; color: #d35400; font-weight: 600; margin: 2px 0; }
    </style>
""", unsafe_allow_html=True)

# --- MEMÓRIA DO PAINEL ---
if "dados_maquinas" not in st.session_state:
    maquinas = [
        {"nome": "TB 05", "cap": "70 KG", "vol": "960 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 0},
        {"nome": "TB 06", "cap": "140 KG", "vol": "2240 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 0},
        {"nome": "TB 07", "cap": "140 KG", "vol": "2240 L", "status": "Manutenção", "horas_manutencao": 12, "horas_sem_prog": 0},
        {"nome": "TB 08", "cap": "140 KG", "vol": "2240 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 2},
        {"nome": "TB 09", "cap": "70 KG", "vol": "960 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 0},
        {"nome": "TB 10", "cap": "70 KG", "vol": "960 L", "status": "Manutenção", "horas_manutencao": 24, "horas_sem_prog": 0},
        {"nome": "CHINASA 19", "cap": "140 KG", "vol": "2240 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 0},
        {"nome": "CHINASA 20", "cap": "20 KG", "vol": "700 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 0},
        {"nome": "CHINASA 21", "cap": "21 KG", "vol": "700 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 5},
        {"nome": "CHINASA 22", "cap": "22 KG", "vol": "700 L", "status": "Manutenção", "horas_manutencao": 8, "horas_sem_prog": 0},
        {"nome": "CHINASA 23", "cap": "23 KG", "vol": "700 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 0},
        {"nome": "CHINASA 24", "cap": "70 KG", "vol": "960 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 0},
        {"nome": "ARMARIO 01", "cap": "300 KG", "vol": "6500 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 0},
        {"nome": "ARMARIO 02", "cap": "140 KG", "vol": "3250 L", "status": "Operacional", "horas_manutencao": 0, "horas_sem_prog": 0}
    ]
    st.session_state.dados_maquinas = pd.DataFrame(maquinas)

# --- MENU LATERAL ---
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Escolha a tela:", ["Painel Principal", "Lançamentos e Planilhas"])

# ==========================================
# TELA 1: PAINEL PRINCIPAL
# ==========================================
if pagina == "Painel Principal":
    st.title("Painel de Controlo: Tinturaria")

    col_filtro1, col_filtro2, col_vazia = st.columns([2, 2, 8])
    with col_filtro1:
        mes_escolhido = st.selectbox("Mês:", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
    with col_filtro2:
        ano_escolhido = st.selectbox("Ano:", ["2024", "2025", "2026", "2027"], index=2)

    st.divider()

    col_titulo, col_grafico = st.columns([4, 1])
    with col_titulo:
        st.markdown(f"### ⚙️ Situação em {mes_escolhido} de {ano_escolhido}")
        st.write("Resumo operacional compacto de todas as máquinas.")

    with col_grafico:
        resumo = st.session_state.dados_maquinas['status'].value_counts().reset_index()
        resumo.columns = ['Status', 'Quantidade']
        fig = px.pie(resumo, values='Quantidade', names='Status', hole=0.6, 
                     color='Status', color_discrete_map={'Operacional':'#28a745', 'Manutenção':'#dc3545'})
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=100, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Cria 7 colunas para os cartões super compactos
    colunas = st.columns(7)
    
    for i, row in st.session_state.dados_maquinas.iterrows():
        col = colunas[i % 7]
        
        # Define as classes CSS dependendo do status da máquina
        classe_cartao = "cartao-op" if row["status"] == "Operacional" else "cartao-man"
        classe_texto = "txt-op" if row["status"] == "Operacional" else "txt-man"
        icone = "🟢" if row["status"] == "Operacional" else "🔴"
        
        # Desenha o cartão em HTML diretamente no painel
        cartao_html = f"""
        <div class="cartao {classe_cartao}">
            <div class="titulo">{row['nome']}</div>
            <div class="status-badge {classe_texto}">{icone} {row['status']}</div>
            <div class="linha"></div>
            <div class="info"><span>📦 Cap:</span> <b>{row['cap']}</b></div>
            <div class="info"><span>💧 Vol:</span> <b>{row['vol']}</b></div>
            <div class="linha"></div>
            <div class="info-alerta">🔧 Manut: {row['horas_manutencao']}h</div>
            <div class="info-aviso">⏳ S/Prog: {row['horas_sem_prog']}h</div>
        </div>
        """
        col.markdown(cartao_html, unsafe_allow_html=True)

# ==========================================
# TELA 2: LANÇAMENTOS E PLANILHAS
# ==========================================
elif pagina == "Lançamentos e Planilhas":
    st.title("⏱️ Lançamentos de Horas e Backup")
    st.write("Dê dois cliques na tabela para editar as horas. Utilize os botões para exportar ou importar dados da folha de cálculo.")
    
    tabela_editada = st.data_editor(
        st.session_state.dados_maquinas, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "nome": "Máquina",
            "cap": "Capacidade",
            "vol": "Volume",
            "status": st.column_config.SelectboxColumn("Status Atual", options=["Operacional", "Manutenção"]),
            "horas_manutencao": st.column_config.NumberColumn("Horas Manutenção", min_value=0, step=1),
            "horas_sem_prog": st.column_config.NumberColumn("Horas Sem Programação", min_value=0, step=1)
        }
    )
    st.session_state.dados_maquinas = tabela_editada
    st.divider()

    col_export, col_import = st.columns(2)
    with col_export:
        st.subheader("⬇️ Exportar (Guardar)")
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.dados_maquinas.to_excel(writer, index=False, sheet_name="Lancamentos")
        st.download_button(
            label="Descarregar Folha de Cálculo",
            data=buffer,
            file_name="lancamentos_tinturaria.xlsx",
            mime="application/vnd.ms-excel"
        )

    with col_import:
        st.subheader("⬆️ Importar (Carregar)")
        arquivo_enviado = st.file_uploader("Arraste o ficheiro Excel", type=["xlsx"])
        if arquivo_enviado is not None:
            df_importado = pd.read_excel(arquivo_enviado)
            st.session_state.dados_maquinas = df_importado
            st.success("✅ Ficheiro lido! Os dados do Painel Principal foram atualizados.")
