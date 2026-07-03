"""Ponto de entrada unificado da aplicação Streamlit."""
import os
import sys
from pathlib import Path

# Força o Python a enxergar a pasta src/ onde o Render extrai o seu projeto
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Opcional: Garante o diretório de trabalho correto
os.chdir(str(current_dir))

# Agora sim, fazemos os imports normais
import streamlit as st
from datetime import date
from database.connection import init_db
from controllers.analysis_controller import AnalysisController
from components.camera_module import render_camera_component
from components.audio_module import render_audio_component
from components.dashboard_module import render_dashboard_component
from components.history_module import render_history_component

# Inicializa configurações da página web
st.set_page_config(page_title="Vision Pipeline Pro", layout="wide", initial_sidebar_state="expanded")

# Executa migrações automáticas de tabelas na base remota Neon.tech
init_db()

@st.cache_resource
def get_controller():
    return AnalysisController()

controller = get_controller()

# --- BARRA LATERAL (Sidebar) ---
st.sidebar.title("🛠️ Painel de Controle")
st.sidebar.markdown("### Status da Plataforma")
st.sidebar.success("⚡ Conectado ao Neon.tech (PostgreSQL)")

st.sidebar.markdown("### 🔍 Filtros de Consulta")
search_query = st.sidebar.text_input("Buscar por termos na descrição ou áudio:")
date_filter = st.sidebar.date_input("Filtrar por Data Específica:", value=None)

# --- CORPO PRINCIPAL ---
st.title("👁️ Enterprise Computer Vision & Speech Architecture")
st.markdown("Módulo unificado para monitoria visual, telemetria analítica e processamento acústico em tempo real.")

tab_captura, tab_historico = st.tabs(["📸 Nova Captura e Análise", "🗄️ Histórico e Dashboards"])

with tab_captura:
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        captured_image_bytes = render_camera_component()
        captured_audio_bytes = render_audio_component()
        
        st.markdown("### Ações de Execução")
        process_btn = st.button("🚀 Processar e Persistir Pipeline", use_container_width=True, type="primary")

    with col_right:
        st.subheader("📊 Resultados do Pipeline em Tempo Real")
        if process_btn:
            if not captured_image_bytes:
                st.error("Erro: É obrigatório capturar uma imagem pela webcam antes de disparar o pipeline.")
            else:
                with st.spinner("Orquestrando modelos de visão e transcrição acústica..."):
                    try:
                        saved_record = controller.process_and_save(
                            image_bytes=captured_image_bytes,
                            audio_bytes=captured_audio_bytes
                        )
                        st.success(f"Pipeline concluído! Registro #{saved_record.id} persistido com sucesso.")
                        
                        st.image(saved_record.image_path, caption="Imagem Armazenada no Servidor", use_container_width=True)
                        st.write(f"💬 **Transcrição Obtida:** {saved_record.transcricao}")
                        st.json(saved_record.json_resultado)
                    except Exception as e:
                        st.error(f"Ocorreu uma falha crítica no processamento: {e}")
        else:
            st.info("Aguardando ativação do gatilho de execução para exibir os resultados.")

with tab_historico:
    # Captura os dados aplicando os filtros de busca em tempo real da barra lateral
    current_data = controller.list_analyses(search=search_query, filter_date=date_filter)
    
    # Renderiza o Dashboard Executivo
    render_dashboard_component(current_data)
    st.markdown("---")
    
    # Renderiza a lista iterativa do histórico
    render_history_component(current_data, controller)
