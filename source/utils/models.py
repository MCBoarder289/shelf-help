from dataclasses import dataclass


@dataclass
class Book:
    """DataClass for holding book information"""
    title: str
    author: str
    isbn: str
    isbn13: str
    avg_rating: float
    date_added: str
    link: str

