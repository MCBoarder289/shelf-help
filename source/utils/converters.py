import requests

from .models import Book
from dash import html, dcc
import dash_bootstrap_components as dbc


def book_to_cards(book: Book):
    cover_response = requests.get(f"https://covers.openlibrary.org/b/isbn/{book.isbn}.json")
    cover_url: str
    if not cover_response.ok:
        cover_url = "https://drive.google.com/thumbnail?id=1i727hdYfgqoliWkxTxHyaT7b5jE3QISY"
    else:
        cover_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg"
    return dbc.Card([
        dbc.CardBody([
            html.P(f"Title: {book.title}", className="card-text"),
            html.P(f"Author: {book.author}", className="card-text"),
            dbc.Row([
                dcc.Store(id={"type": "library-store", "index": book.isbn}, data=book.library_links),
                dbc.Button("Goodreads Link", href=book.link, color="info", target="_blank"),
                dbc.Button(
                    "Check Library Status",
                    color="info",
                    id={"type": "library-button", "index": book.isbn},
                )
            ])
            ]
        ),
        dbc.CardImg(src=cover_url, bottom=True),
    ], style={"width": "18rem"}, class_name="card"
    )
