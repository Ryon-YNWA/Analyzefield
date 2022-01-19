from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scraper:

    def __init__(self):

        # 初期設定
        self.__options = Options()
        self.__options.add_argument('--headless')
        self.__options.add_argument('--start-maximized')
        self.__options.add_argument('--disable-extensions')
        self.__options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36') 

        # driverの取得
        self._driver = webdriver.Chrome(options=self.__options)
        self._driver.implicitly_wait(10)

    def _update_url(self, url):
        self._driver.get(url)

    def _change_window_size(self, width, height):
        self._driver.set_window_size(width, height)

    def _screenshot(self, name, extension='png'):

        # サイトの大きさを取得
        width = self._driver.execute_script('return document.body.clientWidth')
        height = self._driver.execute_script('return document.body.clientHeight')
        self._driver.set_window_size(width, height)

        # スクリーンショットを撮影
        filename = f'{name}.{extension}'
        self._driver.save_screenshot(filename)

    def _close_driver(self):

        self._driver.close()
        self._driver.quit()