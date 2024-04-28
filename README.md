# Shelf Help 
![Shelf Help](assets/images/ios/144.png) 

I'm making this super basic app to help me randomly pick multiple books out of my Goodreads `to-read` shelf.
Because there is no direct API anymore, I'm resorting to scraping/crawling the public pages for my profile.

## High Level Plan
* Input: Goodreads Shelf URL
* Process the resulting page to get the title's data.
* Return the random title with information/navigate to the page in goodreads
* Do this all in some simple Dash app?

## Requirements:
* Python `3.8.12`
* See `requirements.txt`

## Other cool resources I found

* [Open Library](https://openlibrary.org/developers)
  * Has an API and their mission resonates with me
  * Might want to look into porting goodreads things here?
* [OverReader](http://overreader.com/)
  * Uses a GoodReads Shelf to find your local libraries' audio/eBook/Kindle Unlimited availability