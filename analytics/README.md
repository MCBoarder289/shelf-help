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
#### Testing Lambda
Add the following to the lambda_function to test it locally:
```python
if __name__ == '__main__':
    example_shelf_search_body = r"""
    {
      "Type" : "Notification",
      "MessageId" : "bd0ff884-73c8-5106-bf98-a7cba1ea884c",
      "SequenceNumber" : "10000000000000027000",
      "TopicArn" : "arn:aws:sns:us-east-2:692859946229:shelfhelp-event-pipeline.fifo",
      "Message" : "{\"msg_type\":\"SHELFSEARCH\",\"shelf_url\":\"https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=to-read\",\"books\":[{\"title\":\"Into Thin Air: A Personal Account of the Mt. Everest Disaster\",\"author\":\"Jon Krakauer\",\"isbn\":\"\",\"avg_rating\":4.23,\"date_added\":\"Fri, 25 Nov 2022 14:52:40 -0800\",\"link\":\"https://www.goodreads.com/book/show/1898\",\"searchable_title\":\"Into Thin Air: A Personal Account of the Mt. Everest Disaster\",\"image_link\":\"https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1631501298l/1898._SY475_.jpg\",\"goodreads_id\":\"1898\"},{\"title\":\"The Stranger\",\"author\":\"Albert Camus\",\"isbn\":\"\",\"avg_rating\":4.04,\"date_added\":\"Wed, 12 Jun 2024 18:14:43 -0700\",\"link\":\"https://www.goodreads.com/book/show/49552\",\"searchable_title\":\"The Stranger\",\"image_link\":\"https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1590930002l/49552._SY475_.jpg\",\"goodreads_id\":\"49552\"},{\"title\":\"Narrative of the Life of Frederick Douglass\",\"author\":\"Frederick Douglass\",\"isbn\":\"1580495761\",\"avg_rating\":4.08,\"date_added\":\"Sat, 13 Jan 2024 18:52:35 -0800\",\"link\":\"https://www.goodreads.com/book/show/36529\",\"searchable_title\":\"Narrative of the Life of Frederick Douglass\",\"image_link\":\"https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1388234247l/36529.jpg\",\"goodreads_id\":\"36529\"},{\"title\":\"Skin in the Game: The Hidden Asymmetries in Daily Life\",\"author\":\"Nassim Nicholas Taleb\",\"isbn\":\"0241300657\",\"avg_rating\":3.87,\"date_added\":\"Fri, 14 Jun 2024 07:07:57 -0700\",\"link\":\"https://www.goodreads.com/book/show/36064445\",\"searchable_title\":\"Skin in the Game: The Hidden Asymmetries in Daily Life\",\"image_link\":\"https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1510319798l/36064445.jpg\",\"goodreads_id\":\"36064445\"}],\"num_books\":4,\"time_start\":\"2024-09-02T09:46:54.835456\",\"time_end\":\"2024-09-02T09:46:58.513410\",\"total_books\":127,\"search_type\":\"Shuffle\"}",
      "Timestamp" : "2024-09-02T14:46:58.708Z",
      "UnsubscribeURL" : "https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:692859946229:shelfhelp-event-pipeline.fifo:bb37548a-fa4a-4343-8cd4-ce9bb9760157"
    }
    """

    example_library_search_body = r"""
    {
      "Type" : "Notification",
      "MessageId" : "40cfe23d-96c0-5096-b23f-bd7244e649dc",
      "SequenceNumber" : "10000000000000028000",
      "TopicArn" : "arn:aws:sns:us-east-2:692859946229:shelfhelp-event-pipeline.fifo",
      "Message" : "{\"msg_type\":\"LIBRARYSEARCH\",\"library_id\":\"nashville\",\"is_libby\":true,\"time_start\":\"2024-09-02T09:47:02.582256\",\"time_end\":\"2024-09-02T09:47:02.878562\",\"book\":{\"title\":\"Into Thin Air: A Personal Account of the Mt. Everest Disaster\",\"author\":\"Jon Krakauer\",\"isbn\":\"\",\"avg_rating\":4.23,\"date_added\":\"Fri, 25 Nov 2022 14:52:40 -0800\",\"link\":\"https://www.goodreads.com/book/show/1898\",\"searchable_title\":\"Into Thin Air: A Personal Account of the Mt. Everest Disaster\",\"image_link\":\"https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1631501298l/1898._SY475_.jpg\",\"goodreads_id\":\"1898\"},\"available\":true,\"availability_message\":\"AVAILABLE: Check link for more\"}",
      "Timestamp" : "2024-09-02T14:47:02.908Z",
      "UnsubscribeURL" : "https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:692859946229:shelfhelp-event-pipeline.fifo:bb37548a-fa4a-4343-8cd4-ce9bb9760157"
    }
    """

    test_event = {
        'Records': [
            {'body': example_shelf_search_body},
            {'body': example_library_search_body}
        ]
    }


    test = lambda_handler(test_event, None)

    print(test)
```

#### Containerizing Lambda with Docker
Assuming all commands that follow are in the `analytics` directory.

[Helpful link](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions)

**Build Command**:
```commandline
docker build --platform linux/arm64 -t shelf-help-analytics .
```

**Run Command (to test locally)**:
```commandline
docker run --platform linux/arm64 -p 9001:8080 --env-file .env shelf-help-analytics
```

**Test Curl Command**:
```commandline
curl "http://localhost:9001/2015-03-31/functions/function/invocations" -d @test-payload.json
```

**Kill Container Commands**:
```commandline
docker ps
```
* Find container id, then...
```commandline
docker kill <container id>
```

**Cost Management**:
* Realized that Amazon ECR (Container Registry) costs money after a year in the "Private" repo.
* Can't have a Lambda run from a "Public" repo even though that storage is free.
* Therefore, I decided to build the docker image, and then pull out what I needed to create the `.zip` file instead.
* Steps to recreate this:
  * Run docker container with `docker run --platform linux/arm64 -p 9001:8080 --env-file .env shelf-help-analytics`
  * In a separate terminal, copy the main to a new directory like so: `docker cp <running-container-name>:/var/task ./lambda_package`
  * Next, copy all the installed python packages like so: `docker cp <running-container-name>:/var/lang/lib/python3.12/site-packages ./lambda_package`
  * Manually move all the items out of the `site-packages` directory in `./lambda_package` to that top level with everything else
  * Zip it all together from the lambda_package directory with `zip -r ../lambda_function.zip ./*`
  * Then upload that directly to the Lambda

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

* [This walkthrough](https://atlasgo.io/guides/postgres/automatic-migrations) is how I got started.

* Using a `schema.sql` file to be the actual schema
* Using a `migrations` directory to hold the migrations
* Using `atlas.hcl` to hold config/environment definitions
  * the `local` env uses the atlas-demo docker container. Need to have it running via the following command:
  * `docker run --rm -d --name atlas-demo -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=demo -p 5432:5432 postgres`
* CORRECT Steps I did to setup the schema/migrations:
  * Created initial schema.sql
  * Made sure local db was completely blank, since we want to start from scratch.
  * ` atlas migrate diff initial_schema --env local`
    * Created initial_schema migration file
  * Add new migration with:
    * `atlas migrate new seed_libraries`
    * Then manually update the SQL in the generated .sql file in `migrations`
    * Update the hash with `atalas migrate hash`
  * Double-checked SQLAlchemy was synced with:
    * ` atlas migrate diff --env sqlalchemy` didn't return a new generated schema

* WRONG Steps I did to set up the schema/migrations:
  * Created initial schema.sql
  * `atlas schema apply --env prod`
  * Created baseline with following command:
    * `atlas migrate diff my_baseline --env local`
  * Add new migration with:
    * `atlas migrate new seed_libraries`
    * Then manually update the SQL in the generated .sql file in `migrations`
  * Applied the new migration with:
    * `atlas migrate apply --env local --baseline "20240901143242"`
    * In order to make this work for prod, I had do run the `20240901143242` migration manually. *Then* all of the other migrations will follow the pattern below.
  * Net new migrations need to go as follows:
    * Changes to `schema.sql`:
      * `atlas migrate diff <migration_name> --env local`
      * `atlas migrate apply --env local`

### Transfer/Backup the database
I went through the following steps to move my Supabase project over to another region.
These steps should also work if I ever want to back up or relocate the database in the future.

1. Disable the Lambda trigger. This way it will prevent data loss since the SQS queue should hold the data for some time.
2. Followed [these instructions](https://supabase.com/docs/guides/platform/migrating-and-upgrading-projects#migrate-your-project) mostly which are outlined as follows:
3. Run supabase backup commands:
```commandline
supabase db dump --db-url "$OLD_DB_URL" -f roles.sql --role-only
supabase db dump --db-url "$OLD_DB_URL" -f schema.sql
supabase db dump --db-url "$OLD_DB_URL" -f data.sql --use-copy --data-only
```
4. I only cared about the `data.sql` beacuse `atlas` commands will do my migrations for me.
5. Edited the SQL file to remove the following references:
   * Any tables or sequences for tables not in the atlas migration code
   * Take out the INSERT commands related to seeding the databse (taken care of in atlas migrations)
   * Take out anything related to the `atlas_schema_revisions` table
6. Run the following `psql` command to load the data into the new database:
```commandline
psql \
  --single-transaction \
  --variable ON_ERROR_STOP=1 \
  --command 'SET session_replication_role = replica' \
  --file data.sql \
  --dbname "$NEW_DB_URL"
```
7. Turn back on the lambda so that the queue can process

### Set up Local Database for migration testing

The following steps are what you can take to recreate a database with some initial seed data:
1. Spin up the local `atlas-demo` postgres table:
```commandline
docker run --rm -d --name atlas-demo -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=demo -p 5432:5432 postgres
```
2. Run the atlas migrations:
```commandline
atlas migrate apply --env local
```
3. Load the data with psql:
```commandline
psql \
  --single-transaction \
  --variable=ON_ERROR_STOP=1 \
  --command='SET session_replication_role = replica' \
  --file=db_state/data_raw_local_load.sql \
  --dbname="postgresql://postgres:pass@localhost:5432/demo"
```

4. Once you have finished adding migrations and testing everything manually, replace `data_raw_local_load.sql` with what you have locally at the end.
```commandline
docker exec atlas-demo pg_dump --column-inserts --data-only -U postgres demo > db_state/data_raw_local_load.sql
```

5. Make sure you delete all resulting inserts to `atlas_schema_revisions` and `libraries` before commiting.

### Helpful DB maintenance tips:
* running `cluster <table_name> using <index_name>` will reorder the rows physically (helps after weird migrations might update various rows)
* Maintenance commands:
```
REINDEX: This command is used to rebuild an index. It can be used to rebuild all indexes in a specific table or all indexes in the entire database.
VACUUM: This command is used to reclaim space from deleted or updated rows. It can be used to vacuum all tables in the current database or a specific table.
ANALYZE: This command is used to update statistics about the distribution of data in tables and indexes. This can help the query planner make better decisions about how to execute queries.
CLUSTER: This command is used to physically reorder the rows of a table based on the values in one or more of its indexes. This can improve query performance for certain types of queries.
```
## Sequencing
Need a FIFO queue because order will matter given the foreign key constraints, etc.

### DB Order of events:

**ShelfSearch Event:**
1. Insert shelf_url into `shelves` tables (and return id)
2. Insert the books returned data into `books` table (and return ids)
3. Insert into `shelf_searches` using the shelf_id and book_ids

**LibrarySearch Event:**:
1. Retrieve the `book_id` using the ISBN to search the `books` table
2. Insert into `library_searches` using the retrieved book_id
3. Handle if book_id is not present in `books` (Edge Case)
