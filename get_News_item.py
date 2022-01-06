from Settings import options
from bs4 import BeautifulSoup
from urllib.parse import quote
from selenium import webdriver
import os
import math
import re


class Crawling_news(options):
    def __init__(self, keywork, get_item_count, crawling_type):
        super(Crawling_news, self).__init__()
        self.keyword = keywork
        self.get_item_count = get_item_count
        self.query = quote(self.keyword)
        self.driver = webdriver.Chrome(os.path.abspath(self.driver_path), chrome_options=self.chrome_options)
        self.crawling_type = crawling_type

    def get_item(self):
        pages = math.ceil(self.get_item_count / 10)

        url_list = []
        name_list = []

        stack_count = 0
        now_page = 0
        loop = 1

        while loop:
            try:
                if now_page == 0:
                    news_url = f'{self.root_url}{self.query}{self.add_url}1'
                else:
                    news_url = f'{self.root_url}{self.query}{self.add_url}{now_page}1'
                    print(news_url)

                self.driver.get(news_url)
                self.driver.implicitly_wait(5)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                datas = soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > a')
                print(len(datas))

                for i in range(len(datas)):
                    temp = datas[i].text.strip()
                    indx = temp.find(self.keyword)

                    if self.crawling_type == 0:
                        url_list.append(datas[i].get('href'))
                        name_list.append(datas[i].text.strip())
                    elif self.crawling_type == 1:
                        if indx != -1:
                            url_list.append(datas[i].get('href'))
                            name_list.append(datas[i].text.strip())
                    elif self.crawling_type == 2:
                        if indx == -1:
                            url_list.append(datas[i].get('href'))
                            name_list.append(datas[i].text.strip())

                now_page = now_page + 1

                if len(datas) == 0:
                    self.driver.close()

            except:
                break

        try:
            url_list = url_list[:self.get_item_count]
            name_list = name_list[:self.get_item_count]
        except:
            url_list = url_list
            name_list = name_list

        return url_list, name_list
