import os, time

# 项目顶层目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件目录
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

# 日志文件目录
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 截图保存目录
SCREENSHOT_DIR = os.path.join(BASE_DIR, 'screenshot', time.strftime('%Y-%m-%d'))

# 测试脚本的顶层目录
TEST_CASE_TOP_DIR = os.path.join(BASE_DIR, 'test_case')

# 测试数据
TEST_DATA_DIR = os.path.join(BASE_DIR, 'test_case_data')
TEST_DATA_EXCEL_FILE = os.path.join(BASE_DIR, 'test_data', 'test_data.xlsx')

SETTING_LOCAL_FILE = os.path.join(CONFIG_DIR, "settings_local.py")
if os.path.exists(SETTING_LOCAL_FILE):
    # execfile(SETTING_LOCAL_FILE)
    exec(compile(open(SETTING_LOCAL_FILE).read(), SETTING_LOCAL_FILE, 'exec'))

