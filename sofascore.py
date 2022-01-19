import yaml
import datetime
from logging import config, getLogger

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import page_accessor


class SofaScore(page_accessor.PageAccessor):

    def __init__(self, url):
        super().__init__()
        self._update_url(url)
        self._change_window_size(1200, 400)
        self.__parser = 'html.parser'
        self.__logger = getLogger('sofascore')

        self.__players = {}
        self.__home_manager = ''
        self.__away_manager = ''

    def __scrape_match_detail(self):

        soup = BeautifulSoup(self._driver.page_source.encode('utf-8'),  self.__parser)
        match__info_element = soup.find('div', {'class': 'styles__MatchInfoWrapper-sc-s032oy-0 guUPVs'})

        element = match__info_element.find_all('div', {'class': ['dKtWQT']})

        self.__start_date = datetime.datetime.strptime(element[0].text.replace('Start date: ', ''), '%d %b %Y %H:%M')
        self.__location = element[1].text.split('Venue')[0].replace('Location: ', '')
        self.__venue = element[1].text.split('Venue: ')[1]
        self.__referee = element[2].text.split(',')[0].replace('Referee: ', '')
        self.__referee_country = element[2].text.split(', ')[1]

        self.__logger.info(self.__start_date)
        self.__logger.info(self.__location)
        self.__logger.info(self.__venue)
        self.__logger.info(self.__referee)
        self.__logger.info(self.__referee_country)

    def __get_df_match_info(self):

        soup = BeautifulSoup(self._driver.page_source.encode('utf-8'),  self.__parser)
        match_html = soup.find_all('div', {'class': 'TabsWrapper__Wrapper-sc-1lsyq24-0 loCAKW'})[0]

        home_match_info = {}
        away_match_info = {}
        for stats in match_html.find_all('div', {'class': 'Cell-sc-t6h3ns-0 styles__StatisticsItemCell-sc-1imujgi-1 doxblE'}):
            stats = stats.find_all('div', {'class': ['styles__StatisticsItemContent-sc-1imujgi-0']})
            home_match_info[stats[1].text] = stats[0].text
            away_match_info[stats[1].text] = stats[2].text

        return home_match_info, away_match_info

    def __scrape_match_info(self):

        self._driver.find_element(by=By.XPATH, value='//a[text()="ALL"]').click()
        df_home_all_match_info, df_away_all_match_info = self.__get_df_match_info()

        self._driver.find_element(by=By.XPATH, value='//a[text()="1ST"]').click()
        df_home_1st_match_info, df_away_1st_match_info = self.__get_df_match_info()

        self._driver.find_element(by=By.XPATH, value='//a[text()="2ND"]').click()
        df_home_2nd_match_info, df_away_2nd_match_info = self.__get_df_match_info()

        self.__logger.info(df_home_all_match_info)
        self.__logger.info(df_away_all_match_info)
        self.__logger.info(df_home_1st_match_info)
        self.__logger.info(df_away_1st_match_info)
        self.__logger.info(df_home_2nd_match_info)
        self.__logger.info(df_away_2nd_match_info)

    def __scrape_player_list(self):

        # Lineupsを選択
        self._driver.find_element(by=By.XPATH, value='//a[text()="Lineups"]').click()

        # Players欄を４分割
        soup = BeautifulSoup(self._driver.page_source.encode('utf-8'),  self.__parser)
        players_html = soup.find_all('div', {'class': 'Tabs__Content-sc-fivvzb-1 eufWyl'})[1]
        players_html = players_html.find_all('div', {'class': 'Section-sc-umtr2b-0 bGpZoa'})
        home_player = players_html[0]
        away_player = players_html[1]
        home_missing_player = players_html[2]
        away_missing_player = players_html[3]

        # ホームチームの選手を取得
        for player in home_player.find_all('div', {'class': 'Playerstyles__Name-sc-ci0cyk-7 gGrSwr'}):
            name = player.text.replace('(c) ', '')
            self.__players[name] = 'starting'

        for player in home_player.find_all('div', {'class': 'styles__BorderedListItem-sc-100dy5l-2 gJkTGc borderedItem'}):
            name = player.find('div', {'class': 'Content-sc-1morvta-0 styles__NameWrapper-sc-100dy5l-5 cZWTbp'})['title']
            if player.find('div', {'class': 'Content-sc-1morvta-0 ixemiF u-txt-2 manager'}):
                self.__home_manager = name
                continue
            self.__players[name] = ''

        for player in home_missing_player.find_all('div', {'class': 'styles__BorderedListItem-sc-100dy5l-2 gJkTGc borderedItem'}):
            name = player.find('div', {'class': 'Content-sc-1morvta-0 styles__NameWrapper-sc-100dy5l-5 cZWTbp'})['title']
            status = player.find('div', {'class': ['styles__MissingPlayerDescription-sc-100dy5l-13']})['type']
            self.__players[name] = status

        # アウェーチームの選手を取得
        for player in away_player.find_all('div', {'class': 'Playerstyles__Name-sc-ci0cyk-7 gGrSwr'}):
            name = player.text.replace('(c) ', '')
            self.__players[name] = 'starting'

        for player in away_player.find_all('div', {'class': 'styles__BorderedListItem-sc-100dy5l-2 gJkTGc borderedItem'}):
            name = player.find('div', {'class': 'Content-sc-1morvta-0 styles__NameWrapper-sc-100dy5l-5 cZWTbp'})['title']
            if player.find('div', {'class': 'Content-sc-1morvta-0 ixemiF u-txt-2 manager'}):
                self.__away_manager = name
                continue
            self.__players[name] = ''

        for player in away_missing_player.find_all('div', {'class': 'styles__BorderedListItem-sc-100dy5l-2 gJkTGc borderedItem'}):
            name = player.find('div', {'class': 'Content-sc-1morvta-0 styles__NameWrapper-sc-100dy5l-5 cZWTbp'})['title']
            status = player.find('div', {'class': ['styles__MissingPlayerDescription-sc-100dy5l-13']})['type']
            self.__players[name] = status

        self.__logger.info(self.__home_manager)
        self.__logger.info(self.__away_manager)
        for k, v in self.__players.items():
            self.__logger.info(f'{k}: {v}')

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

        self.__scrape_match_detail()
        self.__scrape_player_statistics()
        self.__scrape_player_list()
        self.__scrape_match_info()

        self._close_driver()

if __name__ == '__main__':

    with open('logging.yaml', 'r') as yml:
        _config = yaml.safe_load(yml)
    config.dictConfig(_config)

    scraper = SofaScore('https://www.sofascore.com/brentford-liverpool/Usab')
    scraper.run()