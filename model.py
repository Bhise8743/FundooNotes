from sqlalchemy.orm import declarative_base, Session, sessionmaker, relationship
from sqlalchemy import Integer, String, Column, create_engine, ForeignKey, BigInteger, Boolean, Text, DateTime, Table
from Core.settings import database_name, postgresSQL_password

engine = create_engine(f'postgresql+psycopg2://postgres:{postgresSQL_password}@localhost:5432/{database_name}')
session = Session(engine)
Base = declarative_base()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_name = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    phone = Column(BigInteger)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):  # this method used to define string representation of object
        return self.user_name
