from .models import Book
from dash import html
import dash_bootstrap_components as dbc


def book_to_cards(book: Book):
    # TODO: Add Google Books API for better image results?
    return dbc.CardLink([
        dbc.CardBody([
            html.P(f"Title: {book.title}", className="card-text"),
            html.P(f"Author: {book.author}", className="card-text")
            ]
        ),
        dbc.CardImg(src=f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg", bottom=True),
    ], href=book.link, style={"width": "18rem"}, target="_blank", class_name="card"
    )
