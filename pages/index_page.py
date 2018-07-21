import time
from pages.base_page import BasePage

class IndexPage(BasePage):

    def get_user_name(self):
        # 获取用户昵称
        name = self.find_element_by_class_name('top_menu_user').text
        return name

    def log_out(self):
        element = self.find_element_by_class_name('button_short01')
        element.click()

    def page_navigation(self, category, subCategory, sunCategory=None):
        self.find_element_by_xpath("//div[text()='%s']" % category).click()       # 点击'客戶管理'
        self.find_element_by_xpath("//div[text()='%s']/../following-sibling::div[1]//span[text()='%s']" %(category, subCategory)).click()      # 統一賬號提案
        time.sleep(3)

    def del_received_all_emails(self):
        self.find_element_by_id('fly0').click()     # 选择所有邮件
        self.find_element_by_class_name('nui-btn-text').click()     # 点击删除按钮
        assert self.visibility_of_element_by_class_name('rm1') == False, 'receive box is not null !'

    def goto_write_letter_page(self):
        self.find_element_by_xpath(r'//*[@id="dvNavTop"]/ul[1]/li[2]/span[2]').click()  # 点击'写信'
