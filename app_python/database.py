from sqlmodel import create_engine, SQLModel, Session


class Database:
    def __init__(self):
        sqlite_file_name = "database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        connect_args = {"check_same_thread": False}
        self._engine = create_engine(sqlite_url, connect_args=connect_args)

    def create(self):
        SQLModel.metadata.create_all(self._engine)

    def session(self):
        with Session(self._engine) as session:
            yield session