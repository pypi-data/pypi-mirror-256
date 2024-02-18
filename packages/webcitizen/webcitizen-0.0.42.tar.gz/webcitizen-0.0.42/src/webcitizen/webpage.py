from urllib.parse import urlparse
from newspaper import Article
import bs4
from w3lib.html import replace_escape_chars
from typing import Optional
import pyap
import re
import requests


class Webpage:

    def __init__(
        self, url: str, html: Optional[str] = None, title: Optional[str] = None
    ) -> None:
        self.url = url
        self.html = html
        self.title = title
        if self.html is not None:
            article = Article(url)
            html = self.html.replace("<br>", " ").replace("<br/>", " ")
            self.soup = bs4.BeautifulSoup(self.html, "html.parser")
            # self.html = requests.get(url).text
            article.set_html(self.html)
            article.parse()
            article.nlp()
            self.article = article
            text = self.extract_text()
            self.text = text.replace("  ", " ")

    def __str__(self):
        return f"url: {self.url}, text: toddo"

    def filter_links(self):
        # x = filter_links(all_links, urlparse(response.url).netloc)
        import re

        all_links = self.soup.find_all("a", href=True)
        all_links = [x.get("href") for x in all_links]
        netloc = urlparse(self.url).netloc
        data = [
            f"https://{netloc}{x}" if x.startswith("//") else x
            for x in list(set(all_links))
        ]

        return {
            "external": [
                x
                for x in data
                if (bool(re.match(r"https?://", x)) or bool(re.match(r"//", x)))
                and (netloc not in x)
            ],
            "internal": [
                x
                for x in data
                if (not bool(re.match(r"https?://", x)))
                and (not bool(re.match(r"#", x)))
            ],
            "internal_same_domain": [
                x
                for x in data
                if (not bool(re.match(r"https?://", x)))
                and (not bool(re.match(r"#", x)))
                and (netloc in x)
            ],
            "external-domains": [
                urlparse(x).scheme + "://" + urlparse(x).netloc + "/"
                for x in data
                if (bool(re.match(r"https?://", x)) or bool(re.match(r"//", x)))
                and (netloc not in x)
            ],
        }

    def unpack_url(self, *args, **kwargs):

        _ = urlparse(self.url)
        dict_ = {
            "domain": _.netloc,
            "root_path": _.path.split("/")[1] if len(_.path.split("/")) > 1 else None,
            "full_path": _.path,
            "scheme": _.scheme,
            "scheme_domain": _.scheme,
            "base_url": f"{_.scheme}://{_.netloc}",
        }
        if kwargs.get("return_only"):
            v = kwargs.get("return_only")
            return dict_[v]
        else:
            return dict_

    def extract_text(self) -> str:

        new = self.soup
        new = replace_escape_chars(new.text, replace_by=" ")
        return " ".join(new.split())

    def extract_article_text(self) -> str:
        return self.article.text

    def json_nltk_article(self) -> dict:

        article = self.article

        _ = {
            "keywords": article.keywords,
            "summary": article.summary,
            "text": article.text,
            "title": article.title,
            "authors": article.authors,
            "publish_date": str(article.publish_date),
            "top_image": article.top_image,
            "meta_keywords": article.meta_keywords,
            "meta_description": article.meta_description,
            "meta_lang": article.meta_lang,
            "meta_favicon": article.meta_favicon,
            "canonical_link": article.canonical_link,
            "tags": list(article.tags),
            "movies": article.movies,
            "imgs": list(article.imgs),
        }
        return _

    def json_html(self) -> dict:
        base_url = self.unpack_url(return_only="base_url")
        images = self.soup.find_all("img")
        img_sizes = {}
        for _ in [x.get("src") for x in images]:
            x = base_url + _ if _.startswith("/") else _
            import requests

            r = requests.head(x)
            img_sizes.__setitem__(x, int(r.headers.get("content-length")) / 1000000)

        addresses = (
            pyap.parse(self.text, country="US")
            + pyap.parse(self.text, country="GB")
            + pyap.parse(self.text, country="CA")
        )
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.text)

        # get all h1, h2, h3, h4, h5, h6, p, img, a, meta, link, script, style, title, keywords, description
        soup = self.soup
        phones = re.findall(
            re.findall(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", self.text)
        )
        json_html = (
            {
                "phone_numbers": str(phones) if len(phones) > 0 else None,
                "addresses": str(addresses[0]) if len(addresses) > 0 else None,
                "emails": str(emails[0]) if len(emails) > 0 else None,
                "h1": [
                    replace_escape_chars(i.text.strip()) for i in soup.find_all("h1")
                ],
                "h2": [
                    replace_escape_chars(i.text.strip()) for i in soup.find_all("h2")
                ],
                "h3": [
                    replace_escape_chars(i.text.strip()) for i in soup.find_all("h3")
                ],
                "h4": [
                    replace_escape_chars(i.text.strip()) for i in soup.find_all("h4")
                ],
                "h5": [
                    replace_escape_chars(i.text.strip()) for i in soup.find_all("h5")
                ],
                "h6": [
                    replace_escape_chars(i.text.strip()) for i in soup.find_all("h6")
                ],
                "title": replace_escape_chars(soup.title.text.strip()),
                "keywords": (
                    replace_escape_chars(
                        soup.find("meta", {"name": "keywords"}).get("content")
                    )
                    if soup.find("meta", {"name": "keywords"})
                    else None
                ),
                "description": (
                    replace_escape_chars(
                        soup.find("meta", {"name": "description"}).get("content")
                    )
                    if soup.find("meta", {"name": "description"})
                    else None
                ),
                "robots": (
                    replace_escape_chars(
                        soup.find("meta", {"name": "robots"}).get("content")
                    )
                    if soup.find("meta", {"name": "robots"})
                    else None
                ),
                "text_size": len(replace_escape_chars(soup.text.strip())),
                "img_sizes": img_sizes,
            },
        )

        return json_html

    def analyze_meta_description(self) -> str:
        """
        Analyze the meta description of the website
        Args:
        url (str): url of the website
        html (str): html content of the website
        Returns:
        str: meta description of the website
        """
        if self.meta_description is None:
            self.meta_description = ""
        if self.meta_description:
            if len(self.meta_description) == 0:
                return "empty"
            elif len(self.meta_description) > 0 or len(self.meta_description) <= 129:
                return "short"
            elif len(self.meta_description) >= 130 or len(self.meta_description) <= 160:
                return "correct length"
            else:
                return "long"

    def analyze_H1(self) -> str:
        """
        Analyze the H1 of the website
        Args:
        url (str): url of the website
        html (str): html content of the website
        Returns:
        str: H1 of the website
        """
        if self.h1 is None:
            self.h1 = ""
        if self.h1:
            if len(self.h1) == 0:
                return "empty"
            elif len(self.h1) > 0 or len(self.h1) < 20:
                return "short"
            elif len(self.h1) >= 20 or len(self.h1) <= 70:
                return "correct length"
            else:
                return "long"

    def responsive_check(self, html: str):
        """
        Check if the website is responsive
        Args:
        html (str): html content of the website
        Returns:
        int: score
        list: message
        """
        x = bs4.BeautifulSoup(html, "html.parser")
        # get meta viewport tag value
        message = []
        score = 0
        if (
            str(x.find("meta", {"name": "viewport"}).get("content"))
            == "width=device-width, initial-scale=1.0"
        ):
            score += 10
            message.append("Meta viewport tag is set correctly")
        # check if there are media queries in the html
        if "@media" in html:

            score += 10
            message.append("Media queries are present")
        if "max-width" in html:
            score += 10
            message.append("Max-width is present")

        return score, message

    def searchengine_check(self, html: str):
        """
        Check if the website is search engine friendly
        Args:
        html (str): html content of the website
        Returns:
        int: score
        list: message
        """
        x = bs4.BeautifulSoup(html, "html.parser")
        # get meta viewport tag value
        message = []
        score = 0
        # check if there are meta description tag
        if x.find("meta", {"name": "description"}):
            score += 10
            message.append("Meta description tag is present")
        # check if page has H1 tag
        if x.find("h1"):
            score += 10
            message.append("H1 tag is present")

        return score, message

    def analyze_title(self):
        """
        Analyze the title of the website
        Args:
        url (str): url of the website
        html (str): html content of the website
        Returns:
        str: title of the website
        """
        if self.title is None:
            self.title = ""
        if self.title:

            if len(self.title) == 0:
                return "empty"
            elif len(self.title) > 0 or len(self.title) <= 29:
                return "short"
            elif len(self.title) >= 30 or len(self.title) <= 60:
                return "correct length"
            else:
                return "long"
