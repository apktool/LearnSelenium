import time
import uuid
import json
import random
import base64
import requests
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

user = {
    'username': '17600000000',
    'password': 'cGFzc3dvcmQ='
}


def set_driver():
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    desired_capabilities["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                 "Chrome/59.0.3071.104 Safari/537.36")
    desired_capabilities["phantomjs.page.settings.loadImages"] = True
    desired_capabilities["phantomjs.page.customHeaders.Upgrade-Insecure-Requests"] = 1
    desired_capabilities["phantomjs.page.customHeaders.Cache-Control"] = "max-age=0"
    desired_capabilities["phantomjs.page.customHeaders.Connection"] = "keep-alive"


    # driver = webdriver.Chrome('/home/hadoop/Workspace/LearnSelenium/chromedriver')
    driver = webdriver.PhantomJS( 
        executable_path="/home/hadoop/Workspace/newrank/phantomjs-2.1.1-linux-x86_64/bin/phantomjs",
        desired_capabilities=desired_capabilities,
        service_log_path="ghostdriver.log"
    )
    driver.implicitly_wait(1)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    driver.maximize_window()

    driver.get(url = 'http://www.newrank.cn/public/login/login.html?back=http%3A//www.newrank.cn/')
    driver.find_element_by_css_selector('.login-normal-tap:nth-of-type(2)').click()
    driver.find_element_by_id('account_input').send_keys(user['username'])
    driver.find_element_by_id('password_input').send_keys(base64.b64decode(str.encode(user['password'])).decode('utf-8'))
    driver.find_element_by_id('pwd_confirm').click()
    print(driver.current_url)
    time.sleep(random.randint(5, 10))

    return driver


def get_data(driver, url):
    cookies = driver.get_cookies();
    s = requests.session()

    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    text = s.get(url).json()
    article_classes = ['lastestArticle', 'topArticle']
    for article_class in article_classes:
        aclass = text['value'][article_class]
        for article in aclass:
            title = article['title']
            summary = article['summary']
            publicTime = article['publicTime']
            clicksCount = article['clicksCount']
            likeCount = article['clicksCount']
            articleURL = article['url']
            sql = "INSERT INTO newrank_account_info VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (str(uuid.uuid1()), url.split('=')[1].split('&')[0], article_class, title, summary, clicksCount, likeCount, articleURL, publicTime)
            executesql(sql)


def executesql(sql):
    try:
        cnx = mysql.connector.connect(user='python', password='python', database='testDB')
    except mysql.connector.Error as err:
        print("Connetion errors have done {}".format(err))
    finally:
        cursor = cnx.cursor()

    cursor.execute(sql)
    cnx.commit()


if __name__ == '__main__':
    original_url = 'http://www.newrank.cn/xdnphb/detail/getAccountArticle?uuid={}&flag=true'
    driver = set_driver()

    from account import accounts
    for uuid_index in accounts.values():
        url = original_url.format(uuid_index)
        data = get_data(driver, url)
        print(url)
