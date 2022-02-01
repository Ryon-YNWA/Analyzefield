import yaml
import uuid
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

        self.__match_id = str(uuid.uuid4())
        self.__all_players = {}
        self.__home_players = {}
        self.__away_players = {}
        self.__home_manager = ''
        self.__away_manager = ''

        # DB用レコード
        self.match_info_records = []
        self.match_stats_records = []
        self.player_stats_records = []


    def __scrape_base_info(self):

        # Player Statisticsを選択
        self._driver.find_element(by=By.XPATH, value='//a[text()="Player statistics"]').click()

        # ホームチームの出場した選手一覧を取得
        self._driver.find_elements(by=By.XPATH, value='//div[contains(@class,"styles__HeaderImageWrapper-sc-17k0iju-1")]')[1].click()
        df = self.__get_df_player_statistics()
        for name in df.index.values.tolist():
            self.__home_players[name] = 'starting'

        # アウェーチームの出場した選手一覧を取得
        self._driver.find_elements(by=By.XPATH, value='//div[contains(@class,"styles__HeaderImageWrapper-sc-17k0iju-1")]')[2].click()
        df = self.__get_df_player_statistics()
        for name in df.index.values.tolist():
            self.__away_players[name] = 'starting'

        # Lineupsを選択
        self._driver.find_element(by=By.XPATH, value='//a[text()="Lineups"]').click()
        soup = BeautifulSoup(self._driver.page_source.encode('utf-8'),  self.__parser)

        # チーム名を取得
        title = soup.find('h2', {'class': 'styles__PageTitle-sc-21zwb3-1 UHBeo'})
        self.__home_team = title.text.split(' - ')[0]
        self.__away_team = title.text.split(' - ')[1]
        self.__logger.info(self.__home_team)
        self.__logger.info(self.__away_team)

        # スコアを取得
        # score = soup.find('div', {'class': 'styles__StyledResult-sc-1llrsmh-5 ilGqqP'})

        # 選手を取得
        players_html = soup.find_all('div', {'class': 'Tabs__Content-sc-fivvzb-1 eufWyl'})[1]
        players_html = players_html.find_all('div', {'class': 'Section-sc-umtr2b-0 bGpZoa'})
        home_player = players_html[0]
        away_player = players_html[1]
        home_missing_player = players_html[2]
        away_missing_player = players_html[3]

        # ホームチームのベンチ選手一覧を取得
        for player in home_player.find_all('div', {'class': 'styles__BorderedListItem-sc-100dy5l-2 gJkTGc borderedItem'}):
            name = player.find('div', {'class': 'Content-sc-1morvta-0 styles__NameWrapper-sc-100dy5l-5 cZWTbp'})['title']
            if player.find('div', {'class': 'Content-sc-1morvta-0 ixemiF u-txt-2 manager'}):
                self.__home_manager = name
                continue
            self.__home_players[name] = 'sub'

        # ホームチームの欠場選手一覧を取得
        for player in home_missing_player.find_all('div', {'class': 'styles__BorderedListItem-sc-100dy5l-2 gJkTGc borderedItem'}):
            name = player.find('div', {'class': 'Content-sc-1morvta-0 styles__NameWrapper-sc-100dy5l-5 cZWTbp'})['title']
            status = player.find('div', {'class': ['styles__MissingPlayerDescription-sc-100dy5l-13']})['type']
            self.__home_players[name] = status

        # アウェーチームのベンチ選手一覧を取得
        for player in away_player.find_all('div', {'class': 'styles__BorderedListItem-sc-100dy5l-2 gJkTGc borderedItem'}):
            name = player.find('div', {'class': 'Content-sc-1morvta-0 styles__NameWrapper-sc-100dy5l-5 cZWTbp'})['title']
            if player.find('div', {'class': 'Content-sc-1morvta-0 ixemiF u-txt-2 manager'}):
                self.__away_manager = name
                continue
            self.__away_players[name] = 'sub'

        # アウェーチームの欠場選手一覧を取得
        for player in away_missing_player.find_all('div', {'class': 'styles__BorderedListItem-sc-100dy5l-2 gJkTGc borderedItem'}):
            name = player.find('div', {'class': 'Content-sc-1morvta-0 styles__NameWrapper-sc-100dy5l-5 cZWTbp'})['title']
            status = player.find('div', {'class': ['styles__MissingPlayerDescription-sc-100dy5l-13']})['type']
            self.__away_players[name] = status

        self.__all_players.update(self.__home_players)
        self.__all_players.update(self.__away_players)

        self.__logger.info(self.__all_players)
        self.__logger.info(self.__home_manager)
        self.__logger.info(self.__home_players.items())
        self.__logger.info(self.__away_manager)
        self.__logger.info(self.__away_players.items())

    def __scrape_match_info(self):

        # スクレイピング
        soup = BeautifulSoup(self._driver.page_source.encode('utf-8'),  self.__parser)
        match__info_element = soup.find('div', {'class': 'styles__MatchInfoWrapper-sc-s032oy-0 guUPVs'})
        element = match__info_element.find_all('div', {'class': ['dKtWQT']})

        # レコードの作成
        record = dict()
        record['match_id'] = self.__match_id
        record['start_date'] = datetime.datetime.strptime(element[0].text.replace('Start date: ', ''), '%d %b %Y %H:%M')
        record['location'] = element[1].text.split('Venue')[0].replace('Location: ', '')
        record['venue'] = element[1].text.split('Venue: ')[1]
        record['referee_name'] = element[2].text.split(',')[0].replace('Referee: ', '')
        record['referee_country'] = element[2].text.split(', ')[1]
        self.match_info_records.append(record)

    def __create_record_match_stats(self, half):

        soup = BeautifulSoup(self._driver.page_source.encode('utf-8'),  self.__parser)
        match_html = soup.find_all('div', {'class': 'TabsWrapper__Wrapper-sc-1lsyq24-0 loCAKW'})[0]

        # レコードの作成
        home_record = dict()
        home_record['match_id'] = self.__match_id
        # home_record['team'] = self.__home_team
        home_record['team'] = 'Liverpool'
        home_record['side'] = 'Home'
        home_record['half'] = half

        away_record = dict()
        away_record['match_id'] = self.__match_id
        # away_record['team'] = self.__away_team
        away_record['team'] = 'Brentford'
        away_record['side'] = 'Away'
        away_record['half'] = half

        for stats in match_html.find_all('div', {'class': 'Cell-sc-t6h3ns-0 styles__StatisticsItemCell-sc-1imujgi-1 doxblE'}):
            stats = stats.find_all('div', {'class': ['styles__StatisticsItemContent-sc-1imujgi-0']})
            home_record[stats[1].text] = stats[0].text
            away_record[stats[1].text] = stats[2].text

        return [home_record, away_record]

    def __scrape_match_stats(self):

        self._driver.find_element(by=By.XPATH, value='//a[text()="1ST"]').click()
        self.match_stats_records.extend(self.__create_record_match_stats('1st'))

        self._driver.find_element(by=By.XPATH, value='//a[text()="2ND"]').click()
        self.match_stats_records.extend(self.__create_record_match_stats('2nd'))

    def __create_record_player_stats(self, df):

        #n レコードの作成
        for name, values in df.to_dict(orient='index').items():

            # 
            record = dict()
            record['match_id'] = self.__match_id
            record['player_name'] = name

            if name in self.__home_players.keys():
                record['status'] = self.__home_players[name]
                record['team_name'] = self.__home_team
            elif name in self.__away_players.keys():
                record['status'] = self.__away_players[name]
                record['team_name'] = self.__away_team
            else:
                continue

            # スクレイピングした情報の追加
            record.update(values)

            # 欠損値を削除する
            record = {k: v for k, v in record.items() if pd.notna(v)}

            self.player_stats_records.append(record)

        for name in list(set(self.__all_players.keys()) - set(df.to_dict(orient='index').keys())):

            # 
            record = dict()
            record['match_id'] = self.__match_id
            record['player_name'] = name

            if name in self.__home_players.keys():
                record['status'] = self.__home_players[name]
                record['team_name'] = self.__home_team
            elif name in self.__away_players.keys():
                record['status'] = self.__away_players[name]
                record['team_name'] = self.__away_team
            else:
                continue

            # 欠損値を削除する
            record = {k: v for k, v in record.items() if pd.notna(v)}

            self.player_stats_records.append(record)

        self.__logger.info(self.player_stats_records)

    def __get_df_player_statistics(self):

        soup = BeautifulSoup(self._driver.page_source.encode('utf-8'),  self.__parser)
        table = soup.find('table', {'class': 'styles__Table-sc-17k0iju-6 eApptp'})
        df = pd.read_html(str(table), index_col=1)[0]
        df.drop('#', axis=1, inplace=True)
        return df

    def __scrape_player_statistics(self):

        # Player Statisticsを選択
        self._driver.find_element(by=By.XPATH, value='//a[text()="Player statistics"]').click()

        # Player Statisticsを順にdataframeで取得
        self._driver.find_element(by=By.XPATH, value='//a[text()="Summary"]').click()
        df_summary = self.__get_df_player_statistics()

        self._driver.find_element(by=By.XPATH, value='//a[text()="Attack"]').click()
        df_attack= self.__get_df_player_statistics()

        self._driver.find_element(by=By.XPATH, value='//a[text()="Defence"]').click()
        df_defence = self.__get_df_player_statistics()

        self._driver.find_element(by=By.XPATH, value='//a[text()="Passing"]').click()
        df_passing = self.__get_df_player_statistics()

        self._driver.find_element(by=By.XPATH, value='//a[text()="Duels"]').click()
        df_duels = self.__get_df_player_statistics()

        self._driver.find_element(by=By.XPATH, value='//a[text()="Goalkeeper"]').click()
        df_goalkeeper = self.__get_df_player_statistics()

        # 全てのデータをマージ
        df = df_summary.join(df_attack.join(df_defence.join(df_passing.join(df_duels.join(df_goalkeeper, rsuffix='_'), rsuffix='_'), rsuffix='_'), rsuffix='_'), rsuffix='_')
        df.to_csv('player_stats.csv')

        self.__create_record_player_stats(df)

    def run(self):
        """mainプロセス"""

        self._screenshot('snap')

        self.__scrape_base_info()

        self.__scrape_match_info()

        self.__scrape_match_stats()

        self.__scrape_player_statistics()

        self._close_driver()

if __name__ == '__main__':

    with open('logging.yaml', 'r') as yml:
        _config = yaml.safe_load(yml)
    config.dictConfig(_config)

    sso = SofaScore('https://www.sofascore.com/liverpool-fc-porto/Usckb')
    sso.run()

    import assets.database as db
    db.init_db()
    db.insert_match_info(sso.match_info_records)
    db.insert_match_stats(sso.match_stats_records)
    db.insert_player_stats(sso.player_stats_records)