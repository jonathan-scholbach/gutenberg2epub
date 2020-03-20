import os
import typing as tp

from cached_property import cached_property
import yaml

from src.book_page import BookPage, TitlePage, ChapterPage


class Book:
    def __init__(self, titlepage_url: str) -> None:
        self.titlepage_url = titlepage_url

    @cached_property
    def titlepage(self) -> "TitlePage":
        return TitlePage(self.titlepage_url)

    @cached_property
    def pages(self) -> tp.List["BookPage"]:
        pages = []
        current_page = self.titlepage
        while current_page:
            pages.append(current_page)
            current_page = current_page.next_page

        return pages

    @cached_property
    def meta(self):
        return self.titlepage.meta

    @cached_property
    def content(self):
        return "".join(page.content for page in self.pages)

    @property
    def images(self):
        images = {}
        for page in self.pages:
            images = {
                **images,
                **page.images,
            }

        return images

    @property
    def directory(self):
        return f"books/{self.meta['author']}/{self.meta['title']}".replace(" ", "_")

    @property
    def image_directory(self):
        return f"{self.directory}/images"

    def store(self):
        os.makedirs(self.directory, exist_ok=True)

        with open(self.directory + "/content.html", "w+") as f:
            f.write(self.content)

        with open(self.directory + "/metadata.txt", "w+") as f:
            f.write("---\n")
            f.write(yaml.dump(self.meta))
            f.write("---")

        if self.images:
            os.makedirs(self.image_directory, exist_ok=True)

            for image_file_name, image_file in self.images.items():
                with open(
                    self.image_directory + f"/{image_file_name}", "wb"
                ) as f:
                    for data in image_file.iter_content():
                        f.write(data)
