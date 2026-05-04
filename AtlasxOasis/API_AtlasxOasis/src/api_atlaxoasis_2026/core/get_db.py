from core.databaseHandler import DatabaseManager

db_manager = DatabaseManager()

def get_db():
    with db_manager.get_session() as session:
        yield session