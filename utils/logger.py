"""Módulo gerenciador de logs estruturados."""
import logging
from logging.handlers import RotatingFileHandler
from config.settings import LOG_FOLDER

def get_logger(name: str) -> logging.Logger:
    """Retorna uma instância configurada de Logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        file_handler = RotatingFileHandler(
            LOG_FOLDER / "app.log", maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    return logger