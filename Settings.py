from selenium import webdriver
import urllib.request
import os


class options(object):
    def __init__(self):
        self.root_url = 'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query='
        self.add_url = "&sort=1&photo=0&field=0&pd=4&ds=&de=&cluster_rank=77&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start="
        self.driver_path = './chromedriver/chromedriver_96.exe'

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')