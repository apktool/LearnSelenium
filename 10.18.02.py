import random
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
 

def set_driver():
    driver = webdriver.Chrome('/home/hadoop/Workspace/LearnSelenium/chromedriver')
    driver.get(url = 'http://www.newrank.cn/public/login/login.html?back=http%3A//www.newrank.cn/')
    driver.find_element_by_css_selector('.login-normal-tap:nth-of-type(2)').click()
    driver.find_element_by_id('account_input').send_keys('17600000000')
    driver.find_element_by_id('password_input').send_keys('password')
    driver.find_element_by_id('pwd_confirm').click()
    print(driver.current_url)

    time.sleep(random.randint(5, 10))
    driver.get('http://www.newrank.cn/public/info/detail.html?account=rmrbwx')
    print(driver.current_url)
    with open('abc.html', 'w') as f:
        f.write(driver.page_source)

    return driver

if __name__ == '__main__':
    driver = set_driver()
    print(driver.get_cookies())
