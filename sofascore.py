import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import scrape


class Sofascore(scrape.Scraper):

    def __init__(self, url):
        super().__init__()
        self._update_url(url)
        self._change_window_size(1200, 400)

    def run(self):
        """mainプロセス"""

        self._screenshot('snap')

        self._close_driver()

if __name__ == '__main__':

    s = Sofascore('https://www.sofascore.com/brentford-liverpool/Usab')
    s.run()