from app.database.database import Base, engine

# Importa os modelos para que o SQLAlchemy os conheça
from app.database.models import Trip


def create_database():
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados criado com sucesso!")


if __name__ == "__main__":
    create_database()