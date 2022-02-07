from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains

sleep_sec = 2


def naver_login(title, news_url, id, pwd, tags):
    driver = webdriver.Chrome('./chromedriver/chromedriver_96.exe')

    action = ActionChains(driver)
    url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
    uid = id
    upw = pwd

    driver.get(url)
    time.sleep(sleep_sec)

    tag_id = driver.find_element_by_name('id')
    tag_pw = driver.find_element_by_name('pw')

    tag_id.click()
    pyperclip.copy(uid)
    tag_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(sleep_sec)

    tag_pw.click()
    pyperclip.copy(upw)
    tag_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(sleep_sec)

    login_btn = driver.find_element_by_id('log.login')
    login_btn.click()
    time.sleep(sleep_sec)

    for i in range(len(news_url)):
        if i != 0:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        driver.get('https://cafe.naver.com/fencers')
        time.sleep(sleep_sec)

        news_page = driver.find_element_by_xpath('//*[@id="menuLink69"]')
        news_page.click()
        time.sleep(sleep_sec)

        driver.switch_to.frame('cafe_main')
        write_page = driver.find_element_by_xpath('//*[@id="writeFormBtn"]')
        write_page.click()

        time.sleep(sleep_sec)
        driver.switch_to.window(driver.window_handles[1])

        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[1]/div[2]/div/textarea').click()
        action.send_keys(f'{title[i]}').perform()
        time.sleep(sleep_sec)

        driver.find_element_by_xpath('//span[contains(text(),"내용을")]').click()
        action.send_keys(news_url[i], Keys.ENTER).perform()
        time.sleep(5)

        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[3]/div/div/input').click()

        tag_list = tags.split(',')
        for tag in tag_list:
            action.send_keys(tag, Keys.ENTER).perform()
            time.sleep(sleep_sec)

        complete = driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[1]/div/a')
        complete.click()
        time.sleep(sleep_sec)

    driver.close()
