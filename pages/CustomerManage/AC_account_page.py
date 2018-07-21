from pages.base_page import BasePage
from selenium.webdriver.support.select import Select
import time

class ACAccountPage(BasePage):
    def verify_current_page(self):
        page = self.find_element_by_xpath("//div[@class='tabs-wrap']/ul/li[2]/a/span[1]").text   # 确定title栏page打开
        return page

    def new_AC(self, appellation, chineseName, nationality, IDverify, IDcountry, IDnum, mobileNum, email, country, ACLevel, currency):
        self.find_element_by_xpath("//*[@id='customer_proposal_onestep_datagrid_toolbar']/a[3]/span/span").click()      # 点击“新增”按钮
        time.sleep(3)
        Select(self.find_element_by_id('titleA')).select_by_visible_text(appellation + ' ')      # 称谓
        self.find_element_by_id('chineseNameA').send_keys(chineseName)      # 中文姓名
        Select(self.find_element_by_id('nationalityA')).select_by_visible_text(nationality)    # 国籍
        Select(self.find_element_by_id('customerInfoIdDocumentA')).select_by_visible_text(IDverify)  # 证明文件
        Select(self.find_element_by_id('idDocumentCountryA')).select_by_visible_text(IDcountry)  # 签发国家
        self.find_element_by_id('idDocumentNumberA').send_keys(IDnum)  # 证件号码
        Select(self.find_element_by_id('mobilePhonePrefixA')).select_by_visible_text('中國 (86)')  # 手提电话前缀
        self.find_element_by_id('mobilePhoneA').send_keys(mobileNum)  # 手提电话
        self.find_element_by_id('emailA').send_keys(email)  # 电邮
        Select(self.find_element_by_id('countryA')).select_by_visible_text(country)    # 国家
        self.find_element_by_xpath('//*[@id="customer_proposal_proposalOneStepAdd"]/div/div[3]/ul/li[5]/a/span').click()  # 切换TAB交易账号
        self.find_element_by_id('new_accountInfo_activate_GTS2').click()        # 勾选GTS2账户
        Select(self.find_element_by_id('new_accountLevel_GTS2')).select_by_visible_text(ACLevel)       # 账户级别
        Select(self.find_element_by_id('new_currency_GTS2')).select_by_visible_text(currency)      # 账户币种
        self.find_element_by_xpath('//*[@id="tab-tools-open-onestep"]/a/span/span').click()     # 提交
        time.sleep(5)
        self.switch_to_alert().accept()     # 警告框点确认
        time.sleep(5)

    def return_openAC_info(self):
        proposalStatusTxt = self.find_element_by_xpath("//div[@class='datagrid-view2']/div[2]//child::td[@field='proposalStatusTxt']/div").text     # 返回第二行数据审核状态
        chineseName = self.find_element_by_xpath("//div[@class='datagrid-view2']/div[2]//child::td[@field='chineseName']/div").text       # 返回中文姓名
        return (proposalStatusTxt, chineseName)

    def search_customer_info(self, chineseName):
        element = self.find_element_by_id('chineseNameOSSearch')
        element.clear()
        element.send_keys(chineseName)  # 中文姓名
        self.find_element_by_xpath('//*[@id="customer_proposal_onestep_queryForm_search"]/span/span').click()   # 点击搜索按钮

    def approval_AC_proposal(self):
        self.find_element_by_xpath("//div[@class='datagrid-view2']/div[2]//child::td[@field='id']/div/input").click()   # 勾选第二行的复选框
        self.find_element_by_xpath("//*[@id='customer_proposal_onestep_datagrid_toolbar']/a[1]/span/span").click()      # 勾选审批按钮
        self.find_element_by_xpath("//div[@class='messager-button']/a[2]/span").click()     # 确定审批
        time.sleep(3)
        sucessInfo = self.find_element_by_xpath("//div[@id='_my97DP']/./following-sibling::div[1]/div[2]/div[2]").text  # 审批结果提示信息
        self.find_element_by_xpath("//div[@class='messager-button']/a[1]/span/span").click()    # 审批结果提示信息确认
        return sucessInfo
