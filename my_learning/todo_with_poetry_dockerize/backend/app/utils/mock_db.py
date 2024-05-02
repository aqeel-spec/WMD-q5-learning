from collections.abc import Generator
from sqlmodel import Session, SQLModel, create_engine
from app import settings

connection_string = str(settings.TEST_DATABASE_URL).replace( 
    "postgresql", "postgresql+psycopg"
)
test_engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

def get_test_db_session() -> Generator[Session, None, None]:
    # print("--> TEST DB HERE <---")
    SQLModel.metadata.create_all(test_engine)
    
    with Session(test_engine) as session:
        yield session


def create_db_and_tables():
    print("Creating tables for testing..")
    SQLModel.metadata.create_all(test_engine)
    return ("Tables created..")

def drop_tables():
    print("Dropping tables..")
    SQLModel.metadata.drop_all(test_engine)
    return ("Tables dropped..")

