# py3selenium
关于框架：<br>
py3selenium框架基于Selenium+Unittest搭建的WebUI自动化测试框架<br>
特点：<br>
使用POM（页面对象模式）设计，使代码更加有逻辑性，测试脚本更加规范，后期更加容易维护以及复用性更高<br>
支持多种定位方式，包括（xpath/css/class/ID/text/link_text/name）<br>
框架集成了Selenium的常用定位方法，使元素定位更加方便<br>
使用HTMLTestRunner作为自动生成测试报告，报告更加美观，更加详细，内容更丰富<br>
Logging日志输出，可以看到每一步做的操作<br>
Excel作为数据管理，实现代码，数据分离，使框架的使用起来更加简单<br>
部署环境：<br>
Python 3.0及以后版本<br>
使用到的package主要有：<br>
unittest, selenium, configparser, xlrd, logging<br>
支持的浏览器及驱动：<br>
基于Selenium支持的所有浏览器<br>
browser == "Chrome"<br>
browser == "firefox"<br>
browser == "IE"<br>
browser == "phantomjs"<br>
browser == "opera"<br>
browser == "edge"<br>
geckodriver(Firefox):https://github.com/mozilla/geckodriver/releases<br>
Chromedriver(Chrome):https://sites.google.com/a/chromium.org/chromedriver/home<br>
IEDriverServer(IE):http://selenium-release.storage.googleapis.com/index.html<br>
operadriver(Opera):https://github.com/operasoftware/operachromiumdriver/releases<br>
MicrosoftWebDriver(Edge):https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver<br>
定位元素方式：<br>
class IndexPage(BasePage):
    def get_user_name(self):
        # 获取用户昵称
        name = self.find_element_by_class_name('top_menu_user').text
        return name

    def page_navigation(self, category, subCategory, sunCategory=None):
        self.find_element_by_xpath("//div[text()='%s']" % category).click()       # 点击'客戶管理'
        self.find_element_by_xpath("//div[text()='%s']/../following-sibling::div[1]//span[text()='%s']" %(category, subCategory)).click()      # 統一賬號提案
        time.sleep(3)
配置文件信息（config.ini）：
[BS]
env = test
timeout = 10
base_url = http://192.168.35.100:8083
admin = fxadmin
password = 123456
读取配置文件数据
class ReadConfig:
    """
    创建ConfigParser对象，读取指定目录conf_path配置文件config_name
    """
    def __init__(self, config_name):
        self.conf = configparser.ConfigParser()
        # 中文乱码问题需要添加encoding="utf-8-sig"
        self.conf.read(os.path.join(CONFIG_DIR, config_name), encoding="utf-8-sig")

    def get_bs(self, name):
        value = self.conf.get("BS", name)
        return value

    def get_db(self, name):
        value = self.conf.get("DB", name)
        return value
数据驱动设计：
（1）page脚本中的方法需要根据业务设定参数，如（参数列表中的username和password）：
    def login_with_username_and_password(self, username, password):
        element = self.find_element_by_id('userNo')     # 账号
        element.clear()
        element.send_keys(username)
        element = self.find_element_by_id('password')      # 密码
        element.clear()
        element.send_keys(password)
(2)case脚本调用多个page脚本中的方法，根据业务，组合成为一个业务场景，在调用过程中，传入对应的参数： 
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
（3）步骤（2）中的dataDict是一个自己封装的方法，可以根据当前case的方法名去解析Excel中跟这个方法名相同的case_name,并获取到excel中该行的数据与表头组合成为一个字典，解析过程：
    def get_excel_data_by_casename(self, excelFile, colIndex=0, sheetName=u'test_csv'):  # 修改自己路径
        test_name = self.get_current_case_name()  # 获取调用函数的函数名称(test_name)
        data = xlrd.open_workbook(excelFile)
        table = data.sheet_by_name(sheetName)  # 获得表格
        nrows = table.nrows  # 拿到总共行数
        colnames = table.row_values(colIndex)  # 某一行数据 ['姓名', '用户名', '联系方式', '密码']
        rownums = 0
        findrow = 0
        for i in range(nrows):
            cell_value = table.cell_value(i, colIndex)
            if test_name == str(cell_value):
                findrow += 1
                rownums = i
        assert findrow == 1, 'None or more than one test name in excel sheet, please check!'
        row = table.row_values(rownums)
        excelDict = {}
        for j in range(0, len(colnames)):
            # if row[j] == '':
            #     continue
            excelDict[colnames[j]] = row[j]  # 表头与数据对应
        return excelDict
Excel数据维护格式：
caseName	          description	 username	password	indexname	 一级目录	  二级目录	三级目录	稱謂	中文姓名	國籍
test_login_success	验证正常登陆	fxadmin	 123456	   fxadmin						
test_open_account	  验证正常开户	fxadmin	 123456		 客戶管理	  統一賬號提案		              先生	 超人	    中國

【核心亮点一】：
pages/base_page.py中，加了一个装饰器，如下：
def fail_on_screenshot(function):
    '运行出现失败时保存截图的路径'
    def get_screenshot_dir():
        if not os.path.exists(settings.SCREENSHOT_DIR):
            os.mkdir(settings.SCREENSHOT_DIR)
        return settings.SCREENSHOT_DIR

    def get_current_time_str():
        return datetime.strftime(datetime.now(), "%H-%M-%S")

    def wrapper(*args, **kwargs):
        instance, selector = args[0], args[1]
        try:
            return function(*args, **kwargs)
        except (TimeoutException, NoSuchElementException, InvalidElementStateException) as ex:
            log = Log(os.getenv('trace_info'))
            logger = log.get_logger()
            logger.info("Could not find the selector: [{}]".format(selector))
            filename = "{}.png".format(get_current_time_str())
            logger.debug(instance.selenium.page_source)
            if rc.get_open_close("IS_SCREENSHOT") == "True":
                # 设置为True时保存截图
                screenshot_path = os.path.join(get_screenshot_dir(), filename)
                instance.selenium.save_screenshot(screenshot_path)
            raise ex
    return wrapper
此装饰器的主要作用是运用在所有find_element方法上，让后面的元素识方法调用时，可以自动获取当前执行脚本的文件名和行号，一旦元素识别异常时，自动将出错信息打印到日志(附带截图功能)，识别元素的方法封装如下：
'''判断某个frame是否被添加到了dom里并且可见，切换frame'''

    @fail_on_screenshot
    def switch_to_frame(self, iframe, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.frame_to_be_available_and_switch_to_it(iframe))
好处：所有page页面的元素识别都是调用加了装饰器的find_element方法，不需要在逻辑的每一句加入断言和日志打印以及截图的代码，大大精简了代码，且日志打印的非常明确，直接看出是那个py文件的哪一行有错误。
【核心亮点二】：
因unittest在脚本执行顺序上一直有一个痛点，就是脚本执行顺序很难人为控制(用过unittest的都懂)，而在实际业务中，往往脚本是需要设定执行顺序的，脚本之间想完全独立，很难。基于这个痛点，我设计了一套逻辑可以让脚本按照自己编排好的顺序来批量执行，详情可参照我的CSDN博客发表文章：
https://blog.csdn.net/xinyuanjing123/article/details/80793651
好处：自然就是可以让脚本按照自己编排的顺序执行，当脚本具有耦合性时，完美解决问题。

日志输出
2018-07-15 19:18:49,303 [test_login.py][TestLogin][INFO] CASE-->>[test_login_success] START- 描述:验证正常登陆
2018-07-15 19:19:20,590 [login_page.py][line:11][INFO] Could not find the selector: [userNo]
2018-07-15 19:21:13,796 [test_login.py][TestLogin][INFO] CASE-->>[test_login_success] START- 描述:验证正常登陆
2018-07-15 19:21:45,099 [login_page.py][line:11][INFO] Could not find the selector: [userNo]
2018-07-15 19:21:45,163 [test_login.py][TestLogin][INFO] CASE-->>[test_login_success] END
生成测试报告：自动添加到report目录下，根据时间命名的文件。报告模板是用的通用的 HTMLTestRunner 
