import os
import sys

from src.book import Book


if __name__ == "__main__":
    url = sys.argv[1]
    book = Book(url)
    print(f"Scraping `{book.meta['title']}` by `{book.meta['author']}`...")
    book.store()
    print("Creating epub with pandoc...")
    os.system(f"cd {book.directory} && pandoc --toc -o {book.meta['title'].replace(' ', '_')}.epub metadata.txt content.html +RTS -Ksize -RTS")
    print(f"Finished. Find your book at `{book.directory}`.")
