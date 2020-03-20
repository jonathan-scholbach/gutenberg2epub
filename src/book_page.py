import re
import requests
import typing as tp

from bs4 import BeautifulSoup
from cached_property import cached_property


class BookPage:
    def __init__(self, url: str) -> None:
        self.url = url

    @cached_property
    def raw_html(self):
        html = requests.get(self.url)
        html.encoding = "utf8"

        return html.text

    @property
    def base_url(self):
        return "/".join(self.url.split("/")[:-1]) + "/"

    @cached_property
    def soup(self):
        return BeautifulSoup(self.raw_html, features="html.parser")

    @cached_property
    def next_page(self) -> tp.Optional["ChapterPage"]:
        next_page_url = ""
        for link in self.soup.findAll("a"):
            if "weiter" in link.text:
                return ChapterPage(self.base_url + link.get("href"))

    @cached_property
    def raw_content(self):
        hr_pattern = re.compile("<hr.*?</hr>(.*?)<hr.*?</hr>", re.DOTALL)
        a_pattern = re.compile("<a(.*?)/a>", re.DOTALL)
        content = re.findall(hr_pattern, self.raw_html)[0]
        content = re.sub(a_pattern, "", content).replace("\n", " ")

        return content

    @cached_property
    def content(self):
        space_p = (re.compile("\s+"), " ")

        h_ps = [
            (re.compile(f'<h\d*? class="{classname}">.*?</h\d>'), "")
            for classname in ["title", "author", "subtitle"]
        ]

        image_p = (
            re.compile('<img.*?src=".*?bilder/(.*?)"/>', re.DOTALL),
            '<img src="images/\g<1>"/>',
        )

        figure_p = (
            re.compile(
                '<div class="figure".*?>(.*?)<p class="figcaption">(.*?)</p>.*?</div>',
                re.DOTALL,
            ),
            "<figure>\g<1><figcaption>\g<2></figcaption></figure>",
        )

        motto_p = (
            re.compile('<[p|div] class="motto".*?>(.*?)</[p|div]>', re.DOTALL,),
            '<div class="motto" style="font-size: small; text-align: right;">\g<1></div>',
        )

        p_p = (
            re.compile("<p>(\s*?)</p>"),
            "",
        )
        content = self.raw_content.replace("&nbsp;", " ")

        for pattern in [*h_ps, image_p, figure_p, motto_p, p_p, space_p]:
            content = re.sub(pattern[0], pattern[1], content)

        return content

    @property
    def content_soup(self):
        return BeautifulSoup(self.raw_content, features="html.parser")

    @cached_property
    def images(self):
        images = {
            tag["src"].split("/")[-1]: requests.get(
                self.base_url + tag["src"], stream=True
            )
            for tag in self.content_soup.findAll("img")
        }

        return images


class TitlePage(BookPage):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    @cached_property
    def meta(self) -> dict:
        RELEVANT_FIELDS = [
            "type",
            "author",
            "title",
            "subtitle",
            "publisher",
            "year",
            "firstpub",
        ]

        meta = {}

        for meta_key in self.soup.findAll("meta"):
            try:
                if meta_key["name"] in RELEVANT_FIELDS:
                    meta[meta_key["name"]] = meta_key["content"]
            except KeyError:
                pass

        return meta


class ChapterPage(BookPage):
    def __init__(self, url: str) -> None:
        super().__init__(url)
