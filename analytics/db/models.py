from sqlalchemy import (
    Column, String, BigInteger, Boolean, Integer, TIMESTAMP, ARRAY, ForeignKey, Index, Identity
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Library(Base):
    __tablename__ = 'libraries'

    library_id = Column(String, primary_key=True)
    library_name = Column(String, nullable=False)

    # Relationship to link to library_searches
    library_searches = relationship('LibrarySearch', back_populates='library')


class Book(Base):
    __tablename__ = 'books'

    book_id = Column(BigInteger, Identity(always=True), primary_key=True)
    unique_hash = Column(String, unique=True, nullable=False)
    gr_id = Column(BigInteger)
    title = Column(String)
    author = Column(String)
    isbn = Column(String)
    date_added = Column(TIMESTAMP)
    date_last_displayed = Column(TIMESTAMP)


class Shelf(Base):
    __tablename__ = 'shelves'

    shelf_id = Column(BigInteger, Identity(always=True), primary_key=True)
    shelf_url = Column(String, unique=True, nullable=False)
    date_added = Column(TIMESTAMP)
    date_last_searched = Column(TIMESTAMP)

    # Relationship to link to shelf_searches
    shelf_searches = relationship('ShelfSearch', back_populates='shelf')


class ShelfSearch(Base):
    __tablename__ = 'shelf_searches'

    shelf_search_id = Column(BigInteger, Identity(always=True), primary_key=True)
    shelf_id = Column(BigInteger, ForeignKey('shelves.shelf_id'))
    num_books = Column(Integer)
    time_start = Column(TIMESTAMP)
    time_complete = Column(TIMESTAMP)
    total_book_count = Column(Integer)
    books_returned = Column(ARRAY(BigInteger))

    __table_args__ = (
        Index('idx_shelf_searches_books_returned', 'books_returned', postgresql_using='gin'),
    )

    # Relationship
    shelf = relationship('Shelf', back_populates='shelf_searches')


class LibrarySearch(Base):
    __tablename__ = 'library_searches'

    library_search_id = Column(BigInteger, Identity(always=True), primary_key=True)
    library_id = Column(String, ForeignKey('libraries.library_id'), nullable=False)
    is_libby = Column(Boolean)
    time_start = Column(TIMESTAMP)
    time_complete = Column(TIMESTAMP)
    book_id = Column(BigInteger, ForeignKey('books.book_id'))
    available = Column(Boolean)
    availability_message = Column(String)

    __table_args__ = (
        Index('idx_library_searches_library_id', 'library_id'),
        Index('idx_library_searches_book_id', 'book_id'),
        Index('idx_library_searches_is_libby', 'is_libby'),
        Index('idx_library_searches_available', 'available'),
    )

    # Relationship
    library = relationship('Library', back_populates='library_searches')
