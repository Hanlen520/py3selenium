import os, sys
from public.ReadConfig import ReadConfig
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidElementStateException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from config import settings
from public.Log import MyLog, Log

rc = ReadConfig("config.ini")

def fail_on_screenshot(function):
    '运行出现失败时保存截图'
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


class BasePage(object):
    url = ""
    base_url = rc.get_bs("base_url")

    def __init__(self, selenium):
        self.selenium = selenium

    def refresh(self):
        self.selenium.refresh()

    def navigate_back(self):
        self.selenium.back()

    def selenium_get_url(self, url):
        try:
            self.selenium.get('about:blank')
            self.selenium.get(str(url))
        except Exception as ex:
            log = MyLog.get_log()
            logger = log.get_logger()
            logger.error("Can not open the url:[{}]".format(url))
            raise ex
        return self

    def get_current_page_url(self):
        return self.selenium.current_url

    def get_page_title(self):
        return self.selenium.title

    def get_cookie_value(self):
        return self.selenium.get_cookie('client_identity')['value']

    def frame_switch_content(self):         # 从frame中切回主文档
        return self.selenium.switch_to.default_content()

    def frame_switch_father_frame(self):         # 从子frame切回到父frame
        return self.selenium.switch_to.parent_frame()

    def switch_to_alert(self):      # 切入警告框
        return self.selenium.switch_to.alert

    # ---------------------------------------------------------------------------------------------------------------
    '''判断某个frame是否被添加到了dom里并且可见，切换frame, 可见代表元素可显示且宽和高都大于0'''

    @fail_on_screenshot
    def switch_to_frame(self, iframe, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.frame_to_be_available_and_switch_to_it(iframe))

    # ---------------------------------------------------------------------------------------------------------------
    '''判断某个元素是否被添加到了dom里并且可见，可见代表元素可显示且宽和高都大于0'''
    @fail_on_screenshot
    def find_element_by_css(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    @fail_on_screenshot
    def find_element_by_link_text(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.LINK_TEXT, selector)))

    @fail_on_screenshot
    def find_element_by_partial_link_text(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.PARTIAL_LINK_TEXT, selector)))

    @fail_on_screenshot
    def find_element_by_id(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.ID, selector)))

    @fail_on_screenshot
    def find_element_by_xpath(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.XPATH, selector)))

    @fail_on_screenshot
    def find_element_by_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.NAME, selector)))

    @fail_on_screenshot
    def find_element_by_class_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.CLASS_NAME, selector)))

    @fail_on_screenshot
    def find_element_by_tag_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.TAG_NAME, selector)))

    # ----------------------------------------------------------------------------------------------------------------
    '''判断是否至少有1个元素存在于dom树中，如果定位到就返回列表'''

    @fail_on_screenshot
    def find_elements_by_css(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

    @fail_on_screenshot
    def find_elements_by_class_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.presence_of_all_elements_located((By.CLASS_NAME, selector)))

    @fail_on_screenshot
    def find_elements_by_link_text(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.presence_of_all_elements_located((By.LINK_TEXT, selector)))

    @fail_on_screenshot
    def find_elements_by_xpath(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.presence_of_all_elements_located((By.XPATH, selector)))

    # -------------------------------------------------------------------------------------------------------------
    '''判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素'''

    @fail_on_screenshot
    def invisible_element_by_id(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.invisibility_of_element_located((By.ID, selector)))

    @fail_on_screenshot
    def invisible_element_by_xpath(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.invisibility_of_element_located((By.XPATH, selector)))

    @fail_on_screenshot
    def invisible_element_by_css(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.invisibility_of_element_located((By.CSS_SELECTOR, selector)))

    @fail_on_screenshot
    def invisible_element_by_link_text(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.invisibility_of_element_located((By.LINK_TEXT, selector)))

    @fail_on_screenshot
    def invisible_element_by_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.invisibility_of_element_located((By.NAME, selector)))

    @fail_on_screenshot
    def invisible_element_by_class_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.invisibility_of_element_located((By.CLASS_NAME, selector)))

    @fail_on_screenshot
    def invisible_element_by_tag_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.invisibility_of_element_located((By.TAG_NAME, selector)))

    @fail_on_screenshot
    def invisible_element_by_partial_link_text(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.invisibility_of_element_located((By.PARTIAL_LINK_TEXT, selector)))

    # -----------------------------------------------------------------------------------------------------------------

    '''判断指定的元素中是否包含了预期的字符串，返回布尔值'''

    @fail_on_screenshot
    def text_to_be_present_in_element_by_id(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element((By.ID, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_by_name(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element((By.NAME, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_by_class_name(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element((By.CLASS_NAME, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_by_xpath(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element((By.XPATH, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_by_tag_name(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element((By.TAG_NAME, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_by_css(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text))

    # -----------------------------------------------------------------------------------------------------------------

    '''判断指定元素的属性值中是否包含了预期的字符串，返回布尔值'''

    @fail_on_screenshot
    def text_to_be_present_in_element_value_by_css(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element_value((By.CSS_SELECTOR, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_value_by_id(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element_value((By.ID, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_value_by_name(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element_value((By.NAME, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_value_by_css_name(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element_value((By.CLASS_NAME, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_value_by_xpath(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element_value((By.XPATH, selector), text))

    @fail_on_screenshot
    def text_to_be_present_in_element_value_by_tag_name(self, selector, wait_time=int(rc.get_bs("timeout")), text=None):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.text_to_be_present_in_element_value((By.TAG_NAME, selector), text))


    # -----------------------------------------------------------------------------------------------------------------
    '''判断title,返回布尔值'''

    @fail_on_screenshot
    def page_title_is(self, title, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(expected.title_is(title))

    @fail_on_screenshot
    def page_title_contains(self, title, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(expected.title_contains(title))

    # -----------------------------------------------------------------------------------------------------------------

    '''判断某个元素中是否可见并且是enable的，代表可点击'''

    @fail_on_screenshot
    def element_to_be_click_able_by_id(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.element_to_be_clickable((By.ID, selector)))

    @fail_on_screenshot
    def element_to_be_click_able_by_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.element_to_be_clickable((By.NAME, selector)))

    @fail_on_screenshot
    def element_to_be_click_able_by_class_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.element_to_be_clickable((By.CLASS_NAME, selector)))

    @fail_on_screenshot
    def element_to_be_click_able_by_css(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.element_to_be_clickable((By.CSS_SELECTOR, selector)))

    @fail_on_screenshot
    def element_to_be_click_able_by_tag_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.element_to_be_clickable((By.TAG_NAME, selector)))

    @fail_on_screenshot
    def element_to_be_click_able_by_xpath(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.element_to_be_clickable((By.XPATH, selector)))

    @fail_on_screenshot
    def element_to_be_click_able_by_link_text(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.element_to_be_clickable((By.LINK_TEXT, selector)))

    # -----------------------------------------------------------------------------------------------------------------

    '''判断元素是否可见，如果可见就返回这个元素，不可见返回False'''

    @fail_on_screenshot
    def visibility_of_element_by_id(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.ID, selector)))

    @fail_on_screenshot
    def visibility_of_element_by_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.NAME, selector)))

    @fail_on_screenshot
    def visibility_of_element_by_class_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.CLASS_NAME, selector)))

    @fail_on_screenshot
    def visibility_of_element_by_css(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    @fail_on_screenshot
    def visibility_of_element_by_xpath(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.XPATH, selector)))

    @fail_on_screenshot
    def visibility_of_element_by_tag_name(self, selector, wait_time=int(rc.get_bs("timeout"))):
        self.get_traceback_info()
        return WebDriverWait(self.selenium, wait_time).until(
            expected.visibility_of_element_located((By.TAG_NAME, selector)))

    def get_cookie_by_name(self, name):
        cookie = self.selenium.get_cookie(name)
        return cookie['value']

    def get_session_id(self):
        return self.get_cookie_by_name("TSID")

    def get_traceback_info(self):
        '此方法是获取调用识别元素的代码所在文件(page)和行号'
        case_name = sys._getframe(2).f_back.f_code.co_filename.split('\\')[-1]
        case_line = sys._getframe(2).f_back.f_lineno
        tracebackInfo = "[%s][line:%s]" % (case_name, case_line)
        os.environ['trace_info'] = tracebackInfo



