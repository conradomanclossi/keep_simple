from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)


class Database:
    def __init__(self):
        self.engine = None
        self.Session = None

    def get_engine(self):
        if self.engine is None:
            if os.getenv('ENV') == 'production':
                DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"
            else:
                DATABASE_URL = "sqlite:///./test.db"
            self.engine = create_engine(DATABASE_URL, echo=True, future=True)
            Base.metadata.create_all(self.engine)
        return self.engine

    def get_session(self):
        if self.Session is None:
            engine = self.get_engine()
            self.Session = sessionmaker(bind=engine)
        return self.Session()

    def create_user(self, id, first_name, last_name, username):
        session = self.get_session()
        new_user = User(id=id, first_name=first_name,
                        last_name=last_name, username=username)
        session.add(new_user)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def get_user(self, user_id):
        session = self.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        return user

    def update_user(self, user_id, **kwargs):
        session = self.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.commit()

    def delete_user(self, user_id):
        session = self.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()


database = Database()
