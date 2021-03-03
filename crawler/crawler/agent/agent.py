
#
# 1. parse html
# 2. select urls ( image, javascript, css, ...)
# 3. normalize url
# 4. send new url to Frontier
# 5. write data to Database
#

import re
import requests
import xml.etree.ElementTree as xmlEt


def parse_html(document: requests.models.Response) -> list:
    pass


def recursive_xml(element: xmlEt.Element) -> list:
    if not list(element):
        reg_str = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b' \
                  r'([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        # print(element, type(element))
        # print(element.text)
        if element.text and re.search(reg_str, element.text):
            # print(element.text)
            return [element.text.strip()]
        else:
            return []
    else:
        new_urls = []
        for e in element:
            new_urls += recursive_xml(e)
        return new_urls


def parse_xml(document: str) -> list:
    root = xmlEt.fromstring(document)
    new_urls = []
    for element in root:
        new_urls += recursive_xml(element)
    return new_urls


def parse_image(document: requests.models.Response) -> list:
    pass


def parse_others(document: requests.models.Response) -> list:
    pass


def _normalize_url(url: str) -> str:
    """normalize url
    example
        www.google.com
        www.google.com/
        www.google.com/index.html

    :param url: str
    :return normalized_url: str
    """
    normalized_url = url
    return normalized_url


def _check_is_article(html) -> bool:
    return False


class Agent(object):

    def __init__(self):
        self.distinct_new_urls = []
        self.document_format_func = {
            0: parse_html,
            1: parse_xml,
            2: parse_image,
            3: parse_others,
        }

    def get_new_urls(self) -> list:
        # return new distinct urls
        return self.distinct_new_urls

    def _write_data_to_db(self):
        pass

    def _parse_new_urls(self, url):
        """ parse new url in document
        1. request to get document
        2. parsing link tags (a, img, javascripts, ...)
        3. check that is article
        4.   if article -> write data to db
        5. return new url list

        :param url:
        :return new_urls:
        """
        document = requests.get(url)
        if next(document.iter_lines()).decode() == '<?xml version="1.0" encoding="UTF-8"?>':
            new_urls = parse_xml(document.text)
        else:
            new_urls = parse_others(document)
        # print(new_urls)

        for new_url_ in new_urls:
            if new_url_ not in self.distinct_new_urls:
                self.distinct_new_urls.append(new_url_)

    def _send_new_urls_to_queue(self):
        """send new url list to queue

        :return:
        """
        pass

    def run(self, url):
        url = _normalize_url(url)
        self._parse_new_urls(url)
        self._send_new_urls_to_queue()


if __name__ == '__main__':
    agent = Agent()
    agent.run('https://www.donga.com/sitemap/donga-newsmap.xml')
    for i in agent.get_new_urls():
        print(i)
