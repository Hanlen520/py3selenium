from pages.login_page import LoginPage
from pages.index_page import IndexPage
from test_case.base import BaseSeleniumTestCase
import unittest

class TestLogin(BaseSeleniumTestCase):
    def setUp(self):
        super().setUp()
        LoginPage(self.selenium).goto_base_page()

    def test_login_success(self):
        LoginPage(self.selenium).login_with_username_and_password(self.dataDict['username'], self.dataDict['password'])
        # 校验登陆成功后首页用户昵称是否与登陆信息一致
        nickname = IndexPage(self.selenium).get_user_name()
        try:
            self.assertIn(self.dataDict['indexname'], nickname)
        except AssertionError as e:
            self.logger.error(e)

    def tearDown(self):
        super().tearDown()

if __name__ == '__main__':
    unittest.main()
