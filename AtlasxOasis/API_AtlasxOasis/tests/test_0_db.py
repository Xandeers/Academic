import os
import pytest
from core.databaseHandler import DatabaseManager
from sqlalchemy import text
from sqlalchemy.orm import Session

DB_USER = os.getenv("DB_USER_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
    
class Test_DB():
    
    def test_1_manager_created(self):
        manager = DatabaseManager()
        assert manager is not None
    
    def test_2_database_connection(self):
        manager = DatabaseManager()
        with manager.engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    
    def test_3_get_engine(self):
        manager = DatabaseManager()
        engine = manager.get_engine()
        assert engine is not None
    
    def test_4_get_session(self):
        db = DatabaseManager()
        with db.get_session() as session:
            assert isinstance(session, Session)
            assert session.is_active
    
    def test_5_get_session_rollback_on_error(self):
        db = DatabaseManager()
        with pytest.raises(ValueError):
            with db.get_session() as session:
                session.execute(text("SELECT 1"))
                raise ValueError("Erreur simulée")