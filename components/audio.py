"""Componente visual de gravação de áudio em tempo real usando o microfone."""
import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_audio_component():
    """Exibe o gravador de microfone em tempo real na interface do Streamlit."""
    st.subheader("🎙️ Observações via Áudio (Gravar na Hora)")
    st.write("Clique no botão abaixo para usar o microfone do seu computador:")
    
    # Renderiza o gravador nativo do navegador
    audio_captured = mic_recorder(
        start_prompt="🔴 Iniciar Gravação",
        stop_prompt="⏹️ Parar Gravação",
        just_once=True,
        use_container_width=True,
        format="wav"
    )
    
    if audio_captured is not None:
        # Recupera os bytes brutos do áudio gravado do dicionário retornado
        audio_bytes = audio_captured['bytes']
        st.audio(audio_bytes, format="audio/wav")
        st.success("✅ Áudio gravado com sucesso e pronto para o pipeline!")
        return audio_bytes
        
    return None
