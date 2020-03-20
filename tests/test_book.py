import unittest as ut

from src import Book


class TestBook(ut.TestCase):
    def setUp(self):
        self.book = Book(
            "https://www.projekt-gutenberg.org/zweig/weltgest/titlepage.html"
        )

    def test_author(self):
        self.assertEqual(self.book.meta["author"], "Stefan Zweig")

    def test_title(self):
        self.assertEqual(self.book.meta["title"], "Die Welt von Gestern")

    def test_subtitle(self):
        self.assertEqual(
            self.book.meta["subtitle"], "Erinnerungen eines Europäers"
        )

    def test_chapters(self):
        self.assertEqual(len(self.book.pages), 18)
