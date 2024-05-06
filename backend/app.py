import random
from typing import List

from flask import Flask, request
from flask_caching import Cache
from pydantic import ValidationError

from models import GetBooksRequest, Book, BookList, LibraryStatusRequest, LibraryStatusResponse
from parsers.gr import retrieve_goodreads_shelf_data
from parsers.libby import search_libby
from parsers.library import parser_factory

cache = Cache(config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache',
    'CACHE_THRESHOLD': 100
})

app = Flask(__name__)
cache.init_app(app)


dummy_books = [
    Book(
        title="Book 1",
        author="Author 1",
        isbn="1234567890",
        avg_rating=4.5,
        date_added="2023-01-01",
        link="https://example.com/book1",
        searchable_title="book_1",
        image_link="https://example.com/image1",
        goodreads_id="1"
    ),
    Book(
        title="Book 2",
        author="Author 2",
        isbn="0987654321",
        avg_rating=4.0,
        date_added="2023-01-02",
        link="https://example.com/book2",
        searchable_title="book_2",
        image_link="https://example.com/image2",
        goodreads_id="2"
    ),
    Book(
        title="Book 3",
        author="Author 3",
        isbn="5432167890",
        avg_rating=4.2,
        date_added="2023-01-03",
        link="https://example.com/book3",
        searchable_title="book_3",
        image_link="https://example.com/image3",
        goodreads_id="3"
    )
]


@cache.memoize(timeout=1800)  # 30 minutes
def fetch_shelf_data_from_goodreads(url) -> List[Book]:
    return retrieve_goodreads_shelf_data(shelf_url=url)


@app.route("/bookChoices", methods=['POST'])
def get_book_choices():
    if request.is_json:
        request_data = request.json

        try:
            get_books_request: GetBooksRequest = GetBooksRequest(**request_data)
        except ValidationError as e:
            return e.json(), 400

        shelf_data = fetch_shelf_data_from_goodreads(url=get_books_request.gr_url.strip())
        sample_number = get_books_request.num_books if len(shelf_data) >= get_books_request.num_books else len(shelf_data)
        book_list: List[Book] = random.sample(shelf_data, sample_number)
        return BookList(books=book_list).json(), 200

    else:
        return {"error": "Request must contain JSON data"}, 400


@app.route("/libraryCheck", methods=['POST'])
def get_library_status():
    if request.is_json:
        request_data = request.json

        try:
            library_status_request: LibraryStatusRequest = LibraryStatusRequest(**request_data)
        except ValidationError as e:
            return e.json(), 400

        if library_status_request.is_libby:
            available, message, link = search_libby(
                library_id=library_status_request.library,
                title=library_status_request.book.searchable_title,
                author=library_status_request.book.author
            )
            return LibraryStatusResponse(
                is_available=available,
                msg=message,
                link=link
            ).json(), 200
        else:
            library_parser = parser_factory(library_status_request.library)
            available, message, link = library_parser.get_library_availability(
                library_links=library_parser.get_library_links(
                    isbn=library_status_request.book.isbn,
                    title=library_status_request.book.searchable_title,
                    author=library_status_request.book.author
                )
            )

            return LibraryStatusResponse(
                is_available=available,
                msg=message,
                link=link
            ).json(), 200

    else:
        return {"error": "Request must contain JSON data"}, 400


if __name__ == '__main__':
    app.run(debug=True)
