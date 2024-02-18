from functools import wraps
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from vulzap.settings import VLogger
from vulzap.utils import is_same_origin

logger = VLogger(name="analyzer", level="INFO")


class Analyzer:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    @staticmethod
    def hostonly(func):
        is_same_origin()

        @wraps(func)
        def wrapper(*args, **kwargs):
            _ = func(*args, **kwargs)
            return _

        return wrapper

    @staticmethod
    def element(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _ = func(*args, **kwargs)
            return _

        return wrapper

    def _href(self) -> None:
        for _ in self.soup.find_all(name="a", href=True):
            parsed_url = urlparse(url=_.get("href"))

        return

    def main(self):
        print(self._href())

    # def find_soup(self, tag: str, attrs: dict):
    #     return self.soup.find_all(name=tag, attrs=attrs)

    pass


if __name__ == "__main__":
    a = Analyzer(soup=BeautifulSoup("<html><a href='/test?a=1'></a></html>", "lxml"))
    a.main()
