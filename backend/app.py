import os
import random

import boto3
import orjson
from datetime import datetime
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

ANALYTICS_ENABLED = os.environ.get('ENABLE_ANALYTICS', 'False').lower() == 'true'

if ANALYTICS_ENABLED:
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=os.environ.get("SNS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("SNS_SECRET_ACCESS_KEY"),
        region_name='us-east-2'
    )


@cache.memoize(timeout=1800)  # 30 minutes
def fetch_shelf_data_from_goodreads(url) -> List[Book]:
    return retrieve_goodreads_shelf_data(shelf_url=url)


@app.route("/alive", methods=['GET'])
def alive_check():
    return {"message": "API is alive"}


@app.route("/bookChoices", methods=['POST'])
def get_book_choices():
    if request.is_json:
        start_time = datetime.now()
        request_data = request.json

        try:
            get_books_request: GetBooksRequest = GetBooksRequest(**request_data)
        except ValidationError as e:
            return e.json(), 400

        shelf_data = fetch_shelf_data_from_goodreads(url=get_books_request.gr_url.strip())
        sample_number = get_books_request.num_books if len(shelf_data) >= get_books_request.num_books else len(shelf_data)
        book_list: List[Book] = random.sample(shelf_data, sample_number)

        publish_to_sns(
            {
                "msg_type": "SHELFSEARCH",
                "shelf_url": get_books_request.gr_url.strip(),
                "books": [book.model_dump() for book in book_list],
                "num_books": len(book_list),
                "time_start": start_time,
                "time_end": datetime.now(),
                "total_books": len(shelf_data)
            }
        )

        return BookList(books=book_list).model_dump_json(), 200

    else:
        return {"error": "Request must contain JSON data"}, 400


@app.route("/libraryCheck", methods=['POST'])
def get_library_status():
    if request.is_json:
        start_time = datetime.now()
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

        else:
            library_parser = parser_factory(library_status_request.library)
            available, message, link = library_parser.get_library_availability(
                library_links=library_parser.get_library_links(
                    isbn=library_status_request.book.isbn,
                    title=library_status_request.book.searchable_title,
                    author=library_status_request.book.author
                )
            )

        publish_to_sns(
            {
                "msg_type": "LIBRARYSEARCH",
                "library_id": library_status_request.library,
                "is_libby": library_status_request.is_libby,
                "time_start": start_time,
                "time_end": datetime.now(),
                "book": library_status_request.book.model_dump(),
                "available": available,
                "availability_message": message
            }
        )

        return LibraryStatusResponse(
            is_available=available,
            msg=message,
            link=link
        ).model_dump_json(), 200

    else:
        return {"error": "Request must contain JSON data"}, 400

def publish_to_sns(data):
    if ANALYTICS_ENABLED:
        topic_arn = os.environ.get("TOPIC_ARN")
        message = orjson.dumps(data).decode()
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageGroupId="default-group"
        )
        return response
    else:
        pass



if __name__ == '__main__':
    app.run(debug=True)
