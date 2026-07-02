"""Módulo Controlador Orquestrador seguindo o princípio da responsabilidade única."""
import uuid
from datetime import datetime
from database.connection import SessionLocal
from repositories.analysis_repository import AnalysisRepository
from services.vision_service import VisionService
from services.audio_service import AudioService
from models.analysis import AnalysisModel
from config.settings import UPLOAD_FOLDER
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

class AnalysisController:
    def __init__(self):
        self.vision_service = VisionService()
        self.audio_service = AudioService()

    def process_and_save(self, image_bytes: bytes, audio_bytes: Optional[bytes] = None) -> AnalysisModel:
        """Centraliza a captura, executa pipelines paralelos de visão e áudio e persiste na base Neon."""
        # 1. Executa pipeline de visão computacional
        vision_res = self.vision_service.analyze_image(image_bytes)
        
        # 2. Executa pipeline de áudio se fornecido
        transcription = "Nenhuma observação gravada."
        if audio_bytes:
            transcription = self.audio_service.transcribe(audio_bytes)

        # 3. Escrita física do arquivo de imagem em disco
        filename = f"capture_{uuid.uuid4().hex}.jpg"
        final_image_path = Path(UPLOAD_FOLDER) / filename
        with open(final_image_path, "wb") as f:
            f.write(image_bytes)

        # 4. Mapeamento para Entidade do Modelo ORM
        analysis_model = AnalysisModel(
            image_path=str(final_image_path),
            descricao=vision_res["descricao"],
            objetos=vision_res["objetos"],
            quantidade_pessoas=vision_res["quantidade_pessoas"],
            rostos=vision_res["rostos"],
            idade=vision_res["idade"],
            emocao=vision_res["emocao"],
            cores=vision_res["cores"],
            luminosidade=vision_res["luminosidade"],
            nitidez=vision_res["nitidez"],
            transcricao=transcription,
            json_resultado=vision_res
        )

        # 5. Persistência na base através do Repositório
        db = SessionLocal()
        try:
            repository = AnalysisRepository(db)
            saved_item = repository.save(analysis_model)
            return saved_item
        finally:
            db.close()

    def list_analyses(self, search: Optional[str] = None, filter_date: Optional[Any] = None) -> List[Dict[str, Any]]:
        """Busca registros transformando-os em tipos primitivos para consumo pela UI ou exportadores."""
        db = SessionLocal()
        try:
            repository = AnalysisRepository(db)
            models = repository.get_all(search, filter_date)
            
            result = []
            for m in models:
                result.append({
                    "id": m.id,
                    "created_at": m.created_at,
                    "image_path": m.image_path,
                    "descricao": m.descricao,
                    "objetos": m.objetos,
                    "quantidade_pessoas": m.quantidade_pessoas,
                    "rostos": m.rostos,
                    "idade": m.idade,
                    "emocao": m.emocao,
                    "cores": m.cores,
                    "luminosidade": m.luminosidade,
                    "nitidez": m.nitidez,
                    "transcricao": m.transcricao,
                    "json_resultado": m.json_resultado
                })
            return result
        finally:
            db.close()

    def delete_analysis(self, analysis_id: int) -> bool:
        """Remove o registro do banco de dados e tenta limpar o arquivo físico correspondente."""
        db = SessionLocal()
        try:
            repository = AnalysisRepository(db)
            item = repository.get_by_id(analysis_id)
            if item:
                # Remoção segura do arquivo em disco
                try:
                    p = Path(item.image_path)
                    if p.exists():
                        p.unlink()
                except Exception:
                    pass
                return repository.delete(analysis_id)
            return False
        finally:
            db.close()

    def update_transcription(self, analysis_id: int, text: str) -> bool:
        """Atualiza ou insere uma nova transcrição de áudio em um registro existente."""
        db = SessionLocal()
        try:
            repository = AnalysisRepository(db)
            item = repository.get_by_id(analysis_id)
            if item:
                item.transcricao = text
                repository.save(item)
                return True
            return False
        finally:
            db.close()