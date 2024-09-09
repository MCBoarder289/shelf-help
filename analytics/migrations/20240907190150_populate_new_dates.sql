-- Set shelves date_added field for existing records

UPDATE shelves s
SET
    date_added = subquery.min_date
FROM
    (
        SELECT
            shelf_id,
            MIN(time_start) AS min_date

        FROM shelf_searches

        GROUP BY
            shelf_id
    ) AS subquery
WHERE
 s.shelf_id = subquery.shelf_id;

 -- Set shelves date_last_searched field for existing records

UPDATE shelves s
SET
    date_last_searched = subquery.max_date
FROM
    (
        SELECT
            shelf_id,
            MAX(time_start) AS max_date

        FROM shelf_searches

        GROUP BY
            shelf_id
    ) AS subquery
WHERE
 s.shelf_id = subquery.shelf_id;

-- Set book date_added field for existing records

UPDATE books b
SET
    date_added = subquery.earliest_date
FROM
    (
        SELECT
            UNNEST(books_returned) as book_id,
            MIN(time_start) as earliest_date

        FROM shelf_searches

        WHERE
            books_returned IS NOT NULL

        GROUP BY
            UNNEST(books_returned)
    ) AS subquery
WHERE
    b.book_id = subquery.book_id;

-- Set book date_last_displayed field for existing records

UPDATE books b
SET
    date_last_displayed = subquery.latest_date
FROM
    (
        SELECT
            UNNEST(books_returned) as book_id,
            MAX(time_start) as latest_date

        FROM shelf_searches

        WHERE
            books_returned IS NOT NULL

        GROUP BY
            UNNEST(books_returned)
    ) AS subquery
WHERE
    b.book_id = subquery.book_id;

