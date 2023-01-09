from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date

from conect_to_db import Base


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(30), nullable=False, unique=True)
    date_of_birth = Column(Date)
    lint_to_info = Column(String(250), nullable=False)
    quotes_auth = relationship('Quote', back_populates='author')


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    text = Column(String(1200), nullable=False, unique=True)
    quotes = relationship('Quote', secondary='tags_to_quotes', back_populates = 'tags')


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    text = Column(String(50), nullable=False, unique=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship('Author', cascade='all, delete', back_populates='quotes_auth')
    tags = relationship('Tag', secondary='tags_to_quotes', back_populates = 'quotes')


class TagToQuote(Base):
    __tablename__ = 'tags_to_quotes'
    id = Column(Integer, primary_key=True)
    tag_id = Column('tag_id', ForeignKey('tags.id', ondelete='CASCADE'))
    quote_id = Column('quotes_id', ForeignKey('quotes.id', ondelete='CASCADE'))

