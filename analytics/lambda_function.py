import hashlib
import os
import urllib.parse

import orjson
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import sessionmaker

from db.models import Shelf, Book, ShelfSearch, LibrarySearch


def lambda_handler(event, context):
    # SQS event comes in the form of a list of records
    for record in event['Records']:
        # The body of the SQS message contains the SNS message
        sns_message = orjson.loads(record['body'])
        data = orjson.loads(sns_message['Message'])

        # Perform database insertion or other processing with the parsed data
        insert_into_database(data)

    return {
        'statusCode': 200,
        'body': orjson.dumps('Success')
    }


def generate_book_unique_hash(book):
    return hashlib.sha256(
        f"{book['title']}-{book['author']}-{book['goodreads_id']}-{book['isbn']}".encode()).hexdigest()


def insert_into_database(data):
    DATABASE_URL = f"postgresql+psycopg2://{os.environ.get("DB_USER", "postgres")}:{urllib.parse.quote_plus(os.environ.get("DB_PASS", "pass"))}@{os.environ.get("DB_HOST", "localhost")}:{os.environ.get("DB_PORT", "5432")}/{os.environ.get("DB_NAME", "demo")}"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        if data['msg_type'] == "SHELFSEARCH":
            # First, Add shelf to unique shelves, and track the shelf_id
            insert_stmt = pg_insert(Shelf).values(shelf_url=data['shelf_url']).on_conflict_do_nothing(
                index_elements=[Shelf.shelf_url]
            )

            result = session.execute(insert_stmt)
            shelf_id = result.scalar()

            if not shelf_id:
                existing_shelf = session.query(Shelf).filter_by(shelf_url=data['shelf_url']).first()
                shelf_id = existing_shelf.shelf_id

            # Second, Add all unique books, and track the book ids for the array
            new_book_ids = []
            for book_dict in data['books']:
                book_insert_stmt = pg_insert(Book).values(
                    unique_hash=generate_book_unique_hash(book_dict),
                    gr_id=book_dict['goodreads_id'],
                    title=book_dict['title'],
                    author=book_dict['author'],
                    isbn=book_dict['isbn']
                ).on_conflict_do_update(
                    index_elements=[Book.unique_hash],
                    set_={'unique_hash': Book.unique_hash}
                ).returning(Book.book_id)

                book_result = session.execute(book_insert_stmt)
                new_book_ids.append(book_result.scalar())

            # Finally, add the new shelf search using the shelf_id and new_book_ids array
            new_shelf_search = ShelfSearch(
                shelf_id=shelf_id,
                num_books=data['num_books'],
                time_start=data['time_start'],
                time_complete=data['time_end'],
                total_book_count=data['total_books'],
                books_returned=new_book_ids
            )

            session.add(new_shelf_search)
            session.commit()

        elif data['msg_type'] == "LIBRARYSEARCH":
            # First, Add Book to books if it doesn't exist, and return the book_id
            book_hash = generate_book_unique_hash(data['book'])
            book_insert_stmt = pg_insert(Book).values(
                unique_hash=book_hash,
                gr_id=data['book']['goodreads_id'],
                title=data['book']['title'],
                author=data['book']['author'],
                isbn=data['book']['isbn']
            ).on_conflict_do_nothing(
                index_elements=[Book.unique_hash],
            ).returning(Book.book_id)

            book_result = session.execute(book_insert_stmt)
            book_id = book_result.scalar()

            if not book_id:
                existing_book = session.query(Book).filter_by(unique_hash=book_hash).first()
                book_id = existing_book.book_id

            # Finally, add the new library search using the book_id
            new_library_search = LibrarySearch(
                library_id=data['library_id'],
                is_libby=data['is_libby'],
                time_start=data['time_start'],
                time_complete=data['time_end'],
                book_id=book_id,
                available=data['available'],
                availability_message=data['availability_message']
            )

            session.add(new_library_search)
            session.commit()

        else:
            pass
