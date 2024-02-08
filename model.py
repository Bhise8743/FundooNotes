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


collaborator = Table('collaborator', Base.metadata, Column('user_id', BigInteger, ForeignKey('user.id')),
                     Column('note_id', BigInteger, ForeignKey('notes.id')))


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
    notes = relationship('Notes', back_populates='user')
    label = relationship('Labels', back_populates='user')
    notes_m2m = relationship('Notes', secondary=collaborator, overlaps='user')

    def __repr__(self):  # this method used to define string representation of object
        return self.user_name


class Notes(Base):
    __tablename__ = 'notes'
    id = Column(Integer, index=True, primary_key=True, nullable=False)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    color = Column(String(20), nullable=False)
    reminder = Column(DateTime, default=None)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='notes')
    user_m2m = relationship('User', secondary=collaborator, overlaps='notes')

    def __repr__(self):
        return self.title


class Labels(Base):
    __tablename__ = 'label'
    id = Column(Integer, index=True, primary_key=True, nullable=False)
    label_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='label')

    def __repr__(self):
        return self.label_name


class RequestLog(Base):
    __tablename__ = 'request_logs'
    id = Column(BigInteger, index=True, primary_key=True)
    request_method = Column(String)
    request_path = Column(String)
    count = Column(BigInteger, default=1)
    # user = Column(String,nullable=True)
