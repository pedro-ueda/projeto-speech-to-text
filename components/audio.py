"""Componente visual de gravação de áudio em tempo real usando o microfone."""
import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_audio_component():
    """Exibe o gravador de microfone em tempo real na interface do Streamlit."""
    st.subheader("🎙️ Observações via Áudio (Gravar na Hora)")
    st.write("Clique no botão abaixo para usar o microfone do seu computador:")
    
    audio_captured = mic_recorder(
        start_prompt="🔴 Iniciar Gravação",
        stop_prompt="⏹️ Parar Gravação",
        just_once=False,
        use_container_width=True,
        format="wav"
    )
    
    # Tratamento seguro do retorno do dicionário nativo da versão 0.0.8
    if isinstance(audio_captured, dict) and 'bytes' in audio_captured:
        audio_bytes = audio_captured['bytes']
        if audio_bytes and len(audio_bytes) > 0:
            st.audio(audio_bytes, format="audio/wav")
            return audio_bytes

    return None
