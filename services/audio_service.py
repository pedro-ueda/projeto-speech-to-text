"""Pipeline de processamento acústico e Speech-to-Text integrado usando faster-whisper."""
import tempfile
import os
from faster_whisper import WhisperModel
from utils.logger import get_logger

logger = get_logger(__name__)

class AudioService:
    def __init__(self):
        # Modelo 'tiny' otimizado para CPU/Ambientes de Cloud leves, garantindo inferência rápida localmente ou no Render.
        self.model_size = "tiny"
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info("Carregando modelo do Faster-Whisper...")
            # Configurado para rodar em CPU usando float32 de forma nativa e estável
            self._model = WhisperModel(self.model_size, device="cpu", compute_type="float32")
        return self._model

    def transcribe(self, audio_bytes: bytes) -> str:
        """Converte um fluxo de bytes de áudio para texto síncrono."""
        if not audio_bytes or len(audio_bytes) < 100:
            return "Nenhuma observação por áudio gravada."
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_bytes)
                temp_path = temp_audio.name

            segments, info = self.model.transcribe(temp_path, beam_size=5, language="pt")
            text_result = " ".join([segment.text for segment in segments])
            
            try:
                os.remove(temp_path)
            except OSError:
                pass

            return text_result.strip() if text_result.strip() else "Áudio processado, porém nenhum texto inteligível foi detectado."
        except Exception as e:
            logger.error(f"Falha técnica durante o procedimento de transcrição de áudio: {e}", exc_info=True)
            return f"Falha ao transcrever áudio: {str(e)}"