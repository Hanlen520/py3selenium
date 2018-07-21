import time
from pages.base_page import BasePage
from selenium.webdriver.support.select import Select

class LoginPage(BasePage):

    def goto_base_page(self):
        self.selenium_get_url(self.base_url)

    def login_with_username_and_password(self, username, password):
        element = self.find_element_by_id('userNo')     # 账号
        element.clear()
        element.send_keys(username)
        element = self.find_element_by_id('password')      # 密码
        element.clear()
        element.send_keys(password)
        company = self.find_element_by_id('companyId')     # 选择公司
        Select(company).select_by_value('1')
        language = self.find_element_by_id('localSelect')   # 选择语言
        Select(language).select_by_value('zh_TW')
        element = self.find_element_by_id('loginBtn')       # 点击登陆
        element.click()
        time.sleep(5)
        return self

    def login_with_null_password(self, username):
        # 输入注册时密码
        self.switch_to_frame('x-URS-iframe')
        element = self.find_element_by_name('email')
        element.clear()
        element.send_keys(username)
        element = self.find_element_by_name('password')
        element.clear()
        element = self.find_element_by_id('dologin')
        element.click()
        time.sleep(2)
        return self

    def login_with_null_username(self, password):
        # 输入注册时密码
        self.switch_to_frame('x-URS-iframe')
        element = self.find_element_by_name('email')
        element.clear()
        element = self.find_element_by_name('password')
        element.clear()
        element.send_keys(password)
        element = self.find_element_by_id('dologin')
        element.click()
        time.sleep(2)
        return self
