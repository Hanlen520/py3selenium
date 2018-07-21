import unittest, time, random
from pages.index_page import IndexPage
from pages.login_page import LoginPage
from pages.CustomerManage.AC_account_page import ACAccountPage
from test_case.base import BaseSeleniumTestCase


class CustomerInfo(BaseSeleniumTestCase):

    def setUp(self):
        super().setUp()
        LoginPage(self.selenium).goto_base_page()

    def test_open_account(self):
        '正常开户'
        LoginPage(self.selenium).login_with_username_and_password(self.dataDict['username'], self.dataDict['password'])
        IndexPage(self.selenium).page_navigation(self.dataDict['一级目录'], self.dataDict['二级目录'])
        pages = ACAccountPage(self.selenium).verify_current_page()
        self.assertEqual(pages, self.dataDict['二级目录'])
        time.sleep(3)
        ACAccountPage(self.selenium).new_AC(self.dataDict['稱謂'], self.dataDict['中文姓名'], self.dataDict['國籍'],
                                            self.dataDict['證明文件'], self.dataDict['簽發國家'], random.randint(10001, 999999999),
                                            self.dataDict['手提電話'], self.dataDict['電郵'], self.dataDict['國家'],
                                            self.dataDict['賬戶級別'], self.dataDict['帳號幣種']+' ')
        ACAccountPage(self.selenium).search_customer_info(self.dataDict['中文姓名'])  # 根据中文姓名查询
        time.sleep(2)
        ACinfo = ACAccountPage(self.selenium).return_openAC_info()      # 返回表信息
        self.assertEqual(ACinfo[0], '待批核')      # 验证返回结果：提案状态
        self.assertEqual(ACinfo[1], self.dataDict['中文姓名'])        # 验证返回结果：中文姓名
        sucessInfo = ACAccountPage(self.selenium).approval_AC_proposal()     # 审批提案
        self.assertIn('開戶成功', sucessInfo)

    def tearDown(self):
        super().tearDown()

if __name__ == '__main__':
    unittest.main()
