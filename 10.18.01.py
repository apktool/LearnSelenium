import random
import time
from selenium import webdriver
 
browser = webdriver.Chrome('/home/hadoop/Workspace/LearnSelenium/chromedriver')
browser.get(url = 'http://www.newrank.cn/public/login/login.html?back=http%3A//www.newrank.cn/')
browser.find_element_by_css_selector('.login-normal-tap:nth-of-type(2)').click()
browser.find_element_by_id('account_input').send_keys('17620481942')
browser.find_element_by_id('password_input').send_keys('qwedcvb')
browser.find_element_by_id('pwd_confirm').click()
print(browser.current_url)

time.sleep(random.randint(5, 10))
browser.get('http://www.newrank.cn/public/info/detail.html?account=rmrbwx')
print(browser.current_url)
