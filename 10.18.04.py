import time
import uuid
import random
import base64
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
    driver.get(url)
    print(driver.current_url)
    time.sleep(random.randint(5, 10))

    all_names = driver.find_elements_by_xpath("//a[@class='ellipsis']")
    all_read_counts = driver.find_elements_by_xpath("//span[@class='read-count']")
    all_links_counts = driver.find_elements_by_xpath("//span[@class='links-count']")
    all_links = driver.find_elements_by_xpath("//a[@class='ellipsis']")
    all_times = driver.find_elements_by_xpath("//span[@class='info-detail-article-date']")

    print(len(all_names))

    for index in range(0, len(all_names)):
        space = 'popularity' if index < 10 else 'latest'
        sql = "INSERT INTO newrank_account_info VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (str(uuid.uuid1()), url.split('=')[1] , space, all_names[index].text, all_read_counts[index].text, all_links_counts[index].text, all_links[index].get_attribute('href'), all_times[index].text)
        executesql(sql)


def get_url(file_name):
    with open(file_name) as f:
        accounts = f.readlines()
    return accounts


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
    original_url = 'http://www.newrank.cn/public/info/detail.html?account='
    driver = set_driver()
    accounts = get_url('account.txt')
    for account in accounts:
        url = original_url + account.strip('\n')
        data = get_data(driver, url)
