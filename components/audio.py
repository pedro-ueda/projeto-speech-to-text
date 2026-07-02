"""Componente visual de gravação e gerenciamento de áudio."""
import streamlit as st

def render_audio_component():
    """Exibe o controle de upload ou instrução de áudio estruturado na UI do Streamlit."""
    st.subheader("🎙️ Observações via Áudio (Speech to Text)")
    
    # Utilizando o gravador nativo do Streamlit/HTML5 ou Input de arquivo de voz para ampla compatibilidade Cloud/Local
    audio_file = st.file_uploader("Grave ou envie um arquivo de áudio (WAV/MP3) com suas observações:", type=["wav", "mp3"])
    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")
        return audio_file.read()
    return None