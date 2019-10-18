import basespider
import hashlib
import os


class ProthomAlo(basespider.BaseSpider):
    def __init__(self, conf='', *args, **kwargs):
        super(ProthomAlo, self).__init__(*args, **kwargs)
        self.prefix_patt = "https://www.prothomalo.com"
        self.base_url = "https://www.prothomalo.com"
        self.article_file_path = "/home/talat/Desktop/article"

    def get_base_url(self):
        return self.base_url

    def get_url_prefix_patt(self):
        return self.prefix_patt

    def get_article_selector(self):
        return "div > article > div"

    def save_article(self, text):
        hash_object = hashlib.sha256(text.encode())
        file_name = hash_object.hexdigest()
        f = open(os.path.join(self.article_file_path, file_name), "w+")
        f.write(text)
        f.close()
