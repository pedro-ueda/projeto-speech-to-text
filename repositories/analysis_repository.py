"""Camada de abstração de dados (Repository Pattern) para operações em Análises."""
from sqlalchemy.orm import Session
from models.analysis import AnalysisModel
from typing import List, Optional
from datetime import date
from utils.logger import get_logger

logger = get_logger(__name__)

class AnalysisRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, model: AnalysisModel) -> AnalysisModel:
        """Persiste ou atualiza uma instância de análise na base de dados."""
        try:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model
        except Exception as e:
            self.db.rollback()
            logger.error(f"Falha ao persistir registro de análise: {e}", exc_info=True)
            raise e

    def get_all(self, search: Optional[str] = None, filter_date: Optional[date] = None) -> List[AnalysisModel]:
        """Recupera registros aplicando filtros dinâmicos de busca textual e por data."""
        try:
            query = self.db.query(AnalysisModel)
            if filter_date:
                query = query.filter(AnalysisModel.created_at >= f"{filter_date} 00:00:00").filter(AnalysisModel.created_at <= f"{filter_date} 23:59:59")
            if search:
                search_expr = f"%{search}%"
                query = query.filter(
                    (AnalysisModel.descricao.ilike(search_expr)) | 
                    (AnalysisModel.transcricao.ilike(search_expr))
                )
            return query.order_by(AnalysisModel.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Erro ao buscar registros no repositório: {e}", exc_info=True)
            return []

    def get_by_id(self, analysis_id: int) -> Optional[AnalysisModel]:
        """Busca um registro específico por ID primário."""
        return self.db.query(AnalysisModel).filter(AnalysisModel.id == analysis_id).first()

    def delete(self, analysis_id: int) -> bool:
        """Deleta fisicamente um registro da base de dados."""
        try:
            item = self.get_by_id(analysis_id)
            if item:
                self.db.delete(item)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao remover registro {analysis_id}: {e}", exc_info=True)
            raise e