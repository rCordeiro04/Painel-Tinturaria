import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS para deixar os cartões pequenos e o número de eficiência em destaque
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .nome-maquina { font-size: 15px; font-weight: bold; text-align: center; color: #1f77b4; margin-bottom: 0px; }
    .eficiencia { font-size: 24px; font-weight: 900; text-align: center; margin-top: 5px; margin-bottom: 10px; }
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
    st.title("Painel de Controle: Tinturaria")

    col_filtro1, col_filtro2, col_vazia = st.columns([2, 2, 8])
    with col_filtro1:
        mes_escolhido = st.selectbox("Mês:", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
    with col_filtro2:
        ano_escolhido = st.selectbox("Ano:", ["2024", "2025", "2026", "2027"], index=2)

    st.divider()

    col_titulo, col_grafico = st.columns([4, 1])
    with col_titulo:
        st.markdown(f"### ⚙️ Eficiência em {mes_escolhido} de {ano_escolhido}")
        st.write("Clique no botão de detalhes de cada máquina para ver as especificações e o histórico de paradas.")

    with col_grafico:
        resumo = st.session_state.dados_maquinas['status'].value_counts().reset_index()
        resumo.columns = ['Status', 'Quantidade']
        fig = px.pie(resumo, values='Quantidade', names='Status', hole=0.6, 
                     color='Status', color_discrete_map={'Operacional':'#28a745', 'Manutenção':'#dc3545'})
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=100, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Cria 7 colunas para distribuir os cartões na tela
    colunas = st.columns(7)
    
    for i, row in st.session_state.dados_maquinas.iterrows():
        col = colunas[i % 7]
        
        # --- CÁLCULO DE EFICIÊNCIA ---
        horas_totais_mes = 720
        horas_paradas = row["horas_manutencao"] + row["horas_sem_prog"]
        # Garante que a eficiência não passe de 100% nem caia abaixo de 0%
        eficiencia = max(0, 100 - ((horas_paradas / horas_totais_mes) * 100))
        
        # Define a cor do número baseado no resultado
        if eficiencia >= 90:
            cor_efi = "#28a745" # Verde
        elif eficiencia >= 75:
            cor_efi = "#f39c12" # Amarelo/Laranja
        else:
            cor_efi = "#dc3545" # Vermelho
            
        with col.container(border=True):
            # Mostra apenas o nome e a porcentagem gigante no balão principal
            st.markdown(f"<p class='nome-maquina'>{row['nome']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='eficiencia' style='color: {cor_efi};'>{eficiencia:.1f}%</p>", unsafe_allow_html=True)
            
            # Botão interativo: ao clicar, abre uma pequena janela de informações
            with st.popover("🔎 Ver Detalhes", use_container_width=True):
                cor_status = "🟢" if row["status"] == "Operacional" else "🔴"
                st.markdown(f"**Status atual:** {cor_status} {row['status']}")
                st.markdown("---")
                st.markdown(f"📦 **Capacidade:** {row['cap']}")
                st.markdown(f"💧 **Volume:** {row['vol']}")
                st.markdown("---")
                st.markdown(f"🔧 **Manutenção:** {row['horas_manutencao']}h")
                st.markdown(f"⏳ **Sem Prog.:** {row['horas_sem_prog']}h")

# ==========================================
# TELA 2: LANÇAMENTOS E PLANILHAS
# ==========================================
elif pagina == "Lançamentos e Planilhas":
    st.title("⏱️ Lançamentos de Horas e Backup")
    st.write("Dê dois cliques na tabela para editar as horas. A Eficiência na tela principal será calculada automaticamente com base nesses lançamentos.")
    
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
