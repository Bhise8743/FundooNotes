from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from main import app
from model import get_db, Base
from Core.settings import postgresSQL_password,test_database_name
engine = create_engine(f'postgresql+psycopg2://postgres:{postgresSQL_password}@localhost:5432/{test_database_name}')
session = Session(engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# pytest mark.abc

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)


@pytest.fixture
def user_data():
    return {
        "user_name": "Omkar@123",
        "first_name": "Omkar",
        "last_name": "Bhise",
        "email": "omkarbhise8635@gmail.com",
        "password": "Omkar@123",
        "phone": 9960401728,
        "city": "latur",
        "state": "Maha",
        "is_verified":True
    }


@pytest.fixture
def login_data():
    return {
        "user_name": "Omkar@123",
        "password": "Omkar@123"
    }


@pytest.fixture
def notes_data():
    return {
        "title": "Pytest",
        "description": "using TestClient test the apis",
        "color": "red"
    }


@pytest.fixture
def new_notes_data():
    return {
        "title": "Override the get_db",
        "description": "for the api testing we are override the get_db function with override_get_db function",
        "color": "red"
    }

@pytest.fixture
def update_notes_data():
    return {
        "title": "Pytest",
        "description": "using TestClient test the apis",
        "color": "pink"
    }

@pytest.fixture
def label_data():
    return {
        'label_name': "python "
    }

@pytest.fixture
def update_label_data():
    return {
        'label_name': "python FastAPI "
    }