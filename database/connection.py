"""Módulo de conexão com o banco de dados Neon.tech/PostgreSQL."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import DATABASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    logger.error(f"Erro ao inicializar conexão com banco de dados: {e}", exc_info=True)
    raise e

def init_db():
    """Cria de forma síncrona e automática as tabelas se não existirem."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas do banco de dados verificadas/criadas com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao sincronizar tabelas: {e}", exc_info=True)