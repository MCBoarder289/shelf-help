# Analytics Pipeline and Database

This is a separate python module meant to track usage of Shelf Help.

## General Architecture

The plan is to have fire-and-forget messages to an SNS topic, which will feed an SQS queue, which will invoke an AWS Lambda function.
This architecture is designed to provide minimal impact to the performance of the backend and keep the user experience fast,
while providing insight into the size/frequency of results and usage of the application.

### SNS Topic
* TBD

### SQS Queue
* TBD

### Lambda Function

This is designed to take all what is written in the queue, and depending on what event is fired, process the correct writes to the database.

* Perhaps we'll use an ENUM for the event type?


## Data Observations

The data that we will track will be as follows:

* **Get Data Event**
  * Fires when the `/bookChoices` endpoint is called
  * Will contain:
    * `num_books` - Number of books requested by user to be displayed.
    * `shelf_url` - URL of the shelf for the Goodreads shelf. Distinct URLs can be used to approximate number of unique users.
    * `time_start` - Timestamp when the processing starts. Used to calculate how long the processing takes.
    * `time_complete` - Timestamp when the processing is done. Used to calculate how long the processing takes.
    * `total_book_count` - Integer of how many books were on the shelf. More should correlate with more time.
    * `books_returned` - The small list of books that were chosen to be displayed to the user:
      * title: str
      * author: str
      * isbn: str
      * avg_rating: float
      * date_added: str
      * link: str
      * searchable_title: str
      * image_link: str
      * goodreads_id: str
* **Library Search Event**
  * Fires when the `/libraryCheck` endpoint is called
  * Will contain:
    * `libary_name` - Name of the library.
    * `library_id` -  Unique identifier of the library.
    * `is_libby` - Whether this was a libby search, or physical library search.
    * `time_start` - Timestamp when the processing starts. Used to calculate how long the processing takes.
    * `time_complete` - Timestamp when the processing is done. Used to calculate how long the processing takes.
    * `available` - Boolean for whether the requested library had the book or not.
    * `availability_message` - Message presented to the user about availability.
* **TBD Goodreads Review**
  * Would be nice to track events on how many times we drive traffic to Goodreads.
  * Right now this is a FE link only, would need to add a FE event, or a BE endpoint to send this info.

## Database model

The database is planned to be a Postgres database hosted by Supabase.
Here are some general ides related to the design of the database:

### Schema
This is the basic idea of the relational schema. Each parent bullet is a table:

* `books`
  * Keeps a distinct record of every book that has been displayed to users
  * Columns:
    * `id` - Auto-incrementing integer ID as the primary key
    * `gr_id` - String (maybe int? might be riskier) of the goodreads id for the book. Unique constraint?
    * `title` - String of the book title
    * `author` - String of the book's author
    * `isbn` - String of the ISBN provided. Unique Constraint

* `book_searches`
  * Table to track the frequency/duration of book searches from shelves
  * Columns:
    * `id` - Auto-incrementing integer ID as the Primary Key
    * `shelf_url` - URL of the shelf for the Goodreads shelf. Distinct URLs can be used to approximate number of unique users.
    * `num_books` - Number of books requested by user to be displayed.
    * `time_start` - Timestamp when the processing starts. Used to calculate how long the processing takes.
    * `time_complete` - Timestamp when the processing is done. Used to calculate how long the processing takes.
    * `total_book_count` - Integer of how many books were on the shelf. More should correlate with more time.
    * `books_returned` - The small list of books that were chosen to be displayed to the user
      * Make this a list of the `id` field from the `books` table

* `library_searches`
  * Table to track the frequency/duration/results of library checks
  * Columns:
    * `id` - Auto-incrementing integer ID as the Primary Key
    * `libary_name` - Name of the library. (Maybe exclude this so that you join on the `libraries` table)
    * `library_id` -  Unique identifier of the library. (Maybe make this a foreign key to `libraries` table)
    * `is_libby` - Whether this was a libby search, or physical library search.
    * `time_start` - Timestamp when the processing starts. Used to calculate how long the processing takes.
    * `time_complete` - Timestamp when the processing is done. Used to calculate how long the processing takes.
    * `available` - Boolean for whether the requested library had the book or not.
    * `availability_message` - Message presented to the user about availability.

* `libraries`
  * Reference table that holds the distinct libraries
  * Columns:
    * `id` - Primary Key - String that is the short string used to identify the library (enum in libraryEnum and value LibraryConstants.ts)
    * `name` - String that is the display name in LibraryConstants.ts

### Migrations
Will try to leverage [Atlas](https://atlasgo.io/) for tracking database migrations
