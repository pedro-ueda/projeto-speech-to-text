"""Pipeline de processamento digital de imagens e visão computacional usando OpenCV."""
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
from typing import Dict, Any, List
from utils.logger import get_logger

logger = get_logger(__name__)

class VisionService:
    def __init__(self):
        # Inicializa os classificadores Haar Cascade nativos do OpenCV para detecção
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.upper_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """Executa análises heurísticas e estatísticas completas sobre os bytes da imagem."""
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Incapaz de decodificar os bytes da imagem.")

            height, width, _ = img.shape
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 1. Detecção de Rostos e Pessoas via Haar Cascades
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            bodies = self.upper_body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 50))
            
            num_faces = len(faces)
            num_people = max(num_faces, len(bodies))

            # 2. Avaliação de Luminosidade (Média dos pixels em escala de cinza)
            avg_brightness = np.mean(gray)
            if avg_brightness < 50:
                luminosity = "Baixa / Escuro"
            elif avg_brightness > 200:
                luminosity = "Alta / Superexposto"
            else:
                luminosity = "Normal / Balanceada"

            # 3. Avaliação de Nitidez (Variância do operador Laplaciano)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            if laplacian_var < 100:
                sharpness = "Desfocada / Baixa Nitidez"
            elif laplacian_var > 300:
                sharpness = "Excelente Nitidez"
            else:
                sharpness = "Nitidez Aceitável"

            # 4. Extração de Cores Predominantes (Utilizando K-Means simplificado via histograma/quantização)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pixels = img_rgb.reshape(-1, 3)
            # Amostragem para agilizar cálculo
            pixels_sample = pixels[np.random.choice(pixels.shape[0], 1000, replace=False)] if pixels.shape[0] > 1000 else pixels
            
            # Mapeamento simples de paleta aproximada por canais médios dominantes
            avg_color = np.mean(pixels_sample, axis=0).astype(int).tolist()

            now = datetime.now()
            
            # Prontidão estrutural para integrações com LLMs / Modelos Avançados externos
            detected_objects = ["Pessoa"] * num_people if num_people > 0 else ["Ambiente de captura"]
            
            analysis_result = {
                "descricao": f"Captura em ambiente com iluminação {luminosity.lower()} e {sharpness.lower()}.",
                "objetos": detected_objects,
                "quantidade_pessoas": num_people,
                "rostos": num_faces,
                "idade": "Não disponível (Requer API externa)",
                "emocao": "Não disponível (Requer API externa)",
                "cores": {"RGB_Medio": avg_color},
                "luminosidade": luminosity,
                "nitidez": f"{sharpness} (Métrica: {laplacian_var:.1f})",
                "resolucao": f"{width}x{height}",
                "data": now.strftime("%Y-%m-%d"),
                "horario": now.strftime("%H:%M:%S")
            }
            return analysis_result
        except Exception as e:
            logger.error(f"Erro durante processamento analítico de visão: {e}", exc_info=True)
            raise e