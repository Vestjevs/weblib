from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    pw_hash = Column(String(100))

    def __init__(self, username=None, password=None):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.username


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    description = Column(Text, unique=True)

    def __init__(self, title=None, description=None):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<Title %r>' % self.title


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    books = relationship("Book", secondary="association", backref="authors")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name


association_table = Table('association', Base.metadata, Column('books_id', Integer, ForeignKey('books.id')),
                          Column('authors_id', Integer, ForeignKey('authors.id')))
