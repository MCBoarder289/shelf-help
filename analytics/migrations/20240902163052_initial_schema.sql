-- Create "books" table
CREATE TABLE "books" (
  "book_id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
  "unique_hash" character varying NOT NULL,
  "gr_id" bigint NULL,
  "title" character varying NULL,
  "author" character varying NULL,
  "isbn" character varying NULL,
  PRIMARY KEY ("book_id"),
  CONSTRAINT "books_unique_hash_key" UNIQUE ("unique_hash")
);
-- Create "libraries" table
CREATE TABLE "libraries" (
  "library_id" character varying NOT NULL,
  "library_name" character varying NOT NULL,
  PRIMARY KEY ("library_id")
);
-- Create "library_searches" table
CREATE TABLE "library_searches" (
  "library_search_id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
  "library_id" character varying NOT NULL,
  "is_libby" boolean NULL,
  "time_start" timestamp NULL,
  "time_complete" timestamp NULL,
  "book_id" bigint NULL,
  "available" boolean NULL,
  "availability_message" character varying NULL,
  PRIMARY KEY ("library_search_id"),
  CONSTRAINT "library_searches_book_id_fkey" FOREIGN KEY ("book_id") REFERENCES "books" ("book_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "library_searches_library_id_fkey" FOREIGN KEY ("library_id") REFERENCES "libraries" ("library_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
-- Create index "idx_library_searches_available" to table: "library_searches"
CREATE INDEX "idx_library_searches_available" ON "library_searches" ("available");
-- Create index "idx_library_searches_book_id" to table: "library_searches"
CREATE INDEX "idx_library_searches_book_id" ON "library_searches" ("book_id");
-- Create index "idx_library_searches_is_libby" to table: "library_searches"
CREATE INDEX "idx_library_searches_is_libby" ON "library_searches" ("is_libby");
-- Create index "idx_library_searches_library_id" to table: "library_searches"
CREATE INDEX "idx_library_searches_library_id" ON "library_searches" ("library_id");
-- Create "shelves" table
CREATE TABLE "shelves" (
  "shelf_id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
  "shelf_url" character varying NOT NULL,
  PRIMARY KEY ("shelf_id"),
  CONSTRAINT "shelves_shelf_url_key" UNIQUE ("shelf_url")
);
-- Create "shelf_searches" table
CREATE TABLE "shelf_searches" (
  "shelf_search_id" bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
  "shelf_id" bigint NULL,
  "num_books" integer NULL,
  "time_start" timestamp NULL,
  "time_complete" timestamp NULL,
  "total_book_count" integer NULL,
  "books_returned" bigint[] NULL,
  PRIMARY KEY ("shelf_search_id"),
  CONSTRAINT "shelf_searches_shelf_id_fkey" FOREIGN KEY ("shelf_id") REFERENCES "shelves" ("shelf_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
-- Create index "idx_shelf_searches_books_returned" to table: "shelf_searches"
CREATE INDEX "idx_shelf_searches_books_returned" ON "shelf_searches" USING gin ("books_returned");
