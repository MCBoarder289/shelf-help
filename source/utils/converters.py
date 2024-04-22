from .models import Book
from dash import html
import dash_bootstrap_components as dbc


def book_to_cards(book: Book):
    # TODO: Add Google Books API for better image results?
    return dbc.Card([
        dbc.CardBody([
            html.P(f"Title: {book.title}", className="card-text"),
            html.P(f"Author: {book.author}", className="card-text"),
            dbc.Row([
                dbc.Button("Goodreads Link", href=book.link, color="info", target="_blank"),
                dbc.Button("Check Nashville Library",
                           color="info",
                           id={"type": "library-button", "index": book.isbn},
                           value=f"https://catalog.library.nashville.org/Search/Results?join=AND&lookfor0%5B%5D={book.isbn}&type0%5B%5D=ISN")
            ])
            ]
        ),
        dbc.CardImg(src=f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg", bottom=True),
    ], style={"width": "18rem"}, class_name="card"
    )
