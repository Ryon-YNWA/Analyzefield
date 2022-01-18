import yaml
from logging import config, getLogger

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import scrape


class Sofascore(scrape.Scraper):

    def __init__(self, url):
        super().__init__()
        self._update_url(url)
        self._change_window_size(1200, 400)
        self.__parser = 'html.parser'
        self.__logger = getLogger('sofascore')

    def __get_df_player_statistics(self):

        soup = BeautifulSoup(self._driver.page_source.encode('utf-8'),  self.__parser)
        table = soup.find('table', {'class': 'styles__Table-sc-17k0iju-6 eApptp'})
        return pd.read_html(str(table))

    def __scrape_player_statistics(self):

        # Player Statisticsを選択
        self._driver.find_element(by=By.XPATH, value='//a[text()="Player statistics"]').click()

        # Player Statisticsを順にdataframeで取得
        self._driver.find_element(by=By.XPATH, value='//a[text()="Summary"]').click()
        df_summary = self.__get_df_player_statistics()
        self.__logger.debug(df_summary)

        self._driver.find_element(by=By.XPATH, value='//a[text()="Attack"]').click()
        df_attack= self.__get_df_player_statistics()
        self.__logger.debug(df_attack)

        self._driver.find_element(by=By.XPATH, value='//a[text()="Defence"]').click()
        df_defence = self.__get_df_player_statistics()
        self.__logger.debug(df_defence)

        self._driver.find_element(by=By.XPATH, value='//a[text()="Passing"]').click()
        df_passing = self.__get_df_player_statistics()
        self.__logger.debug(df_passing)

        self._driver.find_element(by=By.XPATH, value='//a[text()="Duels"]').click()
        df_duels = self.__get_df_player_statistics()
        self.__logger.debug(df_duels)

        self._driver.find_element(by=By.XPATH, value='//a[text()="Goalkeeper"]').click()
        df_goalkeeper = self.__get_df_player_statistics()
        self.__logger.debug(df_goalkeeper)

    def run(self):
        """mainプロセス"""

        self._screenshot('snap')

        # Player Statisticsを選択
        self.__scrape_player_statistics()

        self._close_driver()

if __name__ == '__main__':

    with open('logging.yaml', 'r') as yml:
        _config = yaml.safe_load(yml)
    config.dictConfig(_config)

    s = Sofascore('https://www.sofascore.com/brentford-liverpool/Usab')
    s.run()