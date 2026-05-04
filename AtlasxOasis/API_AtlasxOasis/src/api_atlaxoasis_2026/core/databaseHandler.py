import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from contextlib import contextmanager
import logging

logger = logging.getLogger("uvicorn.error")

load_dotenv(".env")

class DatabaseManager:

    def __init__(self):
        # recuperation des variable d' environnement
        self.host = os.getenv("DB_HOST", "localhost")
        self.port= os.getenv("DB_PORT", 5432)
        self.user= os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "")
        self.dbname = os.getenv("DB_NAME", "postgres")
        
        # creation de l'url de connection a la db
        self.connect_url = (f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}")

        self.engine = create_engine(
            self.connect_url,
            pool_size=20,           # Nombre maximal de connexions dans le pool
            max_overflow=10,        # Nombre de connexions supplémentaires autorisées
            pool_timeout=30,        # Temps d'attente max pour une connexion (secondes)
            pool_recycle=3600,      # Recycle les connexions après 1h (évite les timeouts)
            pool_pre_ping=True,     # Vérifie la validité des connexions avant de les utiliser
            echo=False,             # Affiche les requêtes SQL dans la console (utile pour le debug)
            future=True,            
        )

        # Crée une factory de sessions
        self.sessionlocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=False,  # Évite que les objets soient invalidés après un commit
        )

    def get_engine(self):
        return self.engine

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session = self.sessionlocal()
        try:
            yield session
        except Exception as e:
            logger.info("rolleback DB")
            session.rollback()  # Annule la transaction en cas d'erreur
            raise e
        finally:
            session.close()  # Ferme la session pour libérer la connexion

    def close_engine(self):
        if hasattr(self, "engine"):
            self.engine.dispose()
