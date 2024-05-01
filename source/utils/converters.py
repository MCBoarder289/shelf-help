from dataclasses import asdict
from .models import Book
from dash import html, dcc
import dash_bootstrap_components as dbc


def book_to_cards(book: Book):
    return dbc.Card([
        dbc.CardBody([
            html.P(f"Title: {book.title}", className="card-text"),
            html.P(f"Author: {book.author}", className="card-text"),
            dbc.Row([
                dcc.Store(
                    id={"type": "library-store", "index": f'{book.goodreads_id}'},
                    data=asdict(book)
                ),
                dbc.Button("Goodreads Link", href=book.link, color="info", target="_blank"),
                dbc.Button(
                    "Check Library Status",
                    color="info",
                    id={"type": "library-button", "index": f'{book.goodreads_id}'},
                )
            ])
            ]
        ),
        dbc.CardImg(src=book.image_link, bottom=True),
    ], style={"width": "18rem"}, class_name="card"
    )
