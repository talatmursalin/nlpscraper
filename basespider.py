import abc
import scrapy
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(threadName)s %(name)-18s %(levelname)-8s %(message)s'
)


class BaseSpider(scrapy.Spider):

    __metaclass__ = abc.ABCMeta
    name = "crawler"

    def __init__(self, conf='', *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.visited_url_file_name = "visited"
        self.visited_url = self.load_visited_url()
        self.url_writer = self.init_url_saver()

    def init_url_saver(self):
        url_writer = logging.getLogger('url_writer')
        url_writer.setLevel(logging.INFO)
        ch = logging.FileHandler(self.visited_url_file_name)
        ch.setFormatter(logging.Formatter('%(message)s'))
        url_writer.addHandler(ch)
        return url_writer


    def load_visited_url(self):
        logging.debug("load load_visited_url")
        f = open(self.visited_url_file_name, "r")
        ret = f.read().split('\n')
        f.close()
        return ret

    def mark_url_as_visited(self, url):
        logging.debug("mark url as visited [%s]", url)
        self.visited_url.append(url)
        if not self.is_base_url(url):
            self.save_visited_url_to_file(url)

    def save_visited_url_to_file(self, url):
        logging.debug("save_visited_url_to_file")
        self.url_writer.info(url)

    def extract_links(self, response):
        logging.debug("extract links [%s]", response.url)
        hxs = scrapy.Selector(response)
        all_urls_in_page = hxs.xpath('*//a/@href').extract()
        return all_urls_in_page

    def extract_article(self, response):
        logging.debug("extract article [%s]", response.url)
        selector = self.get_article_selector()
        text = None
        html = BeautifulSoup(response.text, "html.parser")
        article = html.select(selector)
        if article:
            article = article[0]
            text = article.get_text()
            if text:
                self.save_article(text)

    def extract_article_and_mark_url(self, response):
        logging.debug("extract article and mark [%s]", response.url)
        self.extract_article(response)
        self.mark_url_as_visited(response.url)

    def match_url_prefix(self, url):
        logging.debug("match url prefix [%s]", url)
        if url.startswith(self.get_url_prefix_patt()):
            return True
        return False

    def extract_links_and_article(self, response):
        logging.debug("extract links and article [%s]", response.url)
        self.extract_article_and_mark_url(response)
        urls_in_page = self.extract_links(response)
        for url in urls_in_page:
            url = response.urljoin(url)
            if self.match_url_prefix(url):
                if url not in self.visited_url:
                    request = scrapy.Request(url,
                                             self.extract_links_and_article)
                    yield request

    def start_requests(self):
        url = self.get_base_url()
        try:
            logging.debug("starting crawler : %s", url)
            request = scrapy.Request(url, self.extract_links_and_article)
            yield request
        except KeyboardInterrupt:
            pass
        except Exception:
            logging.error(e)

    @abc.abstractmethod
    def get_base_url(self):
        raise NotImplementedError(
            'subclass must override get_base_url()')

    @abc.abstractmethod
    def is_base_url(self, url):
        raise NotImplementedError(
            'subclass must override is_base_url()')


    @abc.abstractmethod
    def get_url_prefix_patt(self):
        raise NotImplementedError(
            'subclass must override get_url_prefix_patt')

    @abc.abstractmethod
    def get_article_selector(self):
        raise NotImplementedError(
            'subclass must override get_article_selector()')

    @abc.abstractmethod
    def save_article(self, text):
        raise NotImplementedError(
            'subclass must override save_article()')
