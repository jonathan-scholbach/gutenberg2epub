import unittest as ut

from src import BookPage


class TestBookPage(ut.TestCase):
    def setUp(self):
        self.page = BookPage(
            "https://www.projekt-gutenberg.org/zweig/weltgest/chap001.html"
        )

    def test_next_page(self):
        self.assertEqual(
            self.page.next_page.url,
            "https://www.projekt-gutenberg.org/zweig/weltgest/chap002.html",
        )
