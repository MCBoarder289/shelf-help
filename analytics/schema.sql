CREATE TABLE libraries (
    library_id VARCHAR PRIMARY KEY,
    library_name VARCHAR NOT NULL
);

CREATE TABLE books (
    book_id BIGINT GENERATED ALWAYS AS IDENTITY,
    unique_hash VARCHAR NOT NULL UNIQUE,
    gr_id BIGINT,
    title VARCHAR,
    author VARCHAR,
    isbn VARCHAR,
    date_added TIMESTAMP,
    date_last_displayed TIMESTAMP,
    PRIMARY KEY (book_id)
);

CREATE TABLE shelves (
    shelf_id BIGINT GENERATED ALWAYS AS IDENTITY,
    shelf_url VARCHAR NOT NULL UNIQUE,
    date_added TIMESTAMP,
    date_last_searched TIMESTAMP,
    PRIMARY KEY (shelf_id)
);


CREATE TABLE shelf_searches (
    shelf_search_id BIGINT GENERATED ALWAYS AS IDENTITY,
    shelf_id BIGINT,
    num_books INT,
    time_start TIMESTAMP,
    time_complete TIMESTAMP,
    total_book_count INT,
    books_returned BIGINT[],
    search_type VARCHAR,
    PRIMARY KEY (shelf_search_id),
    CONSTRAINT shelf_searches_shelf_id_fkey
      FOREIGN KEY(shelf_id)
        REFERENCES shelves(shelf_id)
);

CREATE INDEX idx_shelf_searches_books_returned ON shelf_searches USING GIN (books_returned);

CREATE TABLE library_searches (
    library_search_id BIGINT GENERATED ALWAYS AS IDENTITY,
    library_id VARCHAR NOT NULL,
    is_libby BOOLEAN,
    time_start TIMESTAMP,
    time_complete TIMESTAMP,
    book_id BIGINT,
    available BOOLEAN,
    availability_message VARCHAR,
    PRIMARY KEY (library_search_id),
    CONSTRAINT library_searches_library_id_fkey
      FOREIGN KEY(library_id)
        REFERENCES libraries(library_id),
    CONSTRAINT library_searches_book_id_fkey
      FOREIGN KEY(book_id)
        REFERENCES books(book_id)
);

CREATE INDEX idx_library_searches_library_id ON library_searches(library_id);
CREATE INDEX idx_library_searches_book_id ON library_searches(book_id);
CREATE INDEX idx_library_searches_is_libby ON library_searches(is_libby);
CREATE INDEX idx_library_searches_available ON library_searches(available);

