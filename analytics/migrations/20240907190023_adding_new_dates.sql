-- Modify "books" table
ALTER TABLE "books" ADD COLUMN "date_added" timestamp NULL, ADD COLUMN "date_last_displayed" timestamp NULL;
-- Modify "shelves" table
ALTER TABLE "shelves" ADD COLUMN "date_added" timestamp NULL, ADD COLUMN "date_last_searched" timestamp NULL;
