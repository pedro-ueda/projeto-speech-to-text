"""Componente visual para captura de fluxos da Câmera."""
import streamlit as st

def render_camera_component():
    """Renderiza o input nativo de câmera e captura os bytes da foto."""
    st.subheader("📸 Captura de Vídeo em Tempo Real")
    picture = st.camera_input("Alinhe o alvo na câmera e clique em capturar:")
    if picture is not None:
        return picture.getvalue()
    return None