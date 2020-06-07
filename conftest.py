import path as path
from appium import webdriver
import subprocess
import os
import pytest
import time
from selenium.webdriver import ActionChains
from appium import webdriver
import subprocess
import os
import pytest
from pathlib import Path
import time
from selenium.webdriver import ActionChains
from testrail import *
from allure_commons.types import AttachmentType
import allure
import test_assaycustomchip
# from robot.libraries.BuiltIn import BuiltIn
# import SeleniumLibrary
import timeit
from selenium.webdriver.common.keys import Keys


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
            print("inside if")
            test_assaycustomchip.case_fields()
            test_assaycustomchip.Time()

            if test_assaycustomchip.update_testrail == True:
                print("yes true")
                test_assaycustomchip.fail_update()
            else:
                print("not true")

        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))

    if rep.when == 'call' and rep.passed:
        test_assaycustomchip.stop()
        if test_assaycustomchip.update_testrail == True:
            test_assaycustomchip.pass_update()


@pytest.fixture(scope='module', autouse=True)
def teardown_module():
    yield
    test_assaycustomchip.teardwn()


@pytest.fixture(scope="function")
def driver():
    # app = os.getenv('HOME')
    # print(app)
    # if os.path.isfile(str(app) + "\D50238\workbooktest.workbook"):
    #     os.remove(str(app) + "\D50238\workbooktest.workbook")
    #     print("file removed")
    # else:
    #     print('file not removed')

    desktop = str(os.path.join(Path.home(), "Desktop\D50238"))
    try:
        if os.path.isfile(desktop + "\workbooktest.workbook"):
            os.remove(desktop + "\workbooktest.workbook")
    except:
        print("workbook file not found")

    desktop = str(os.path.join(Path.home(), "Desktop\D50238"))
    try:
        if os.path.isfile(desktop + "\workbookcheck.workbook"):
            os.remove(desktop + "\workbookcheck.workbook")
    except:
        print("workbook file not found")


    # appdata = os.getenv('APPDATA')
    # verifydata = " <CsvPath>Processed Data\D50238_2019-01-29_14-34-13_2019-01-29_11-19-56.549_TNFa_FITC_0_TNFa_FITC.csv</CsvPath>"
    # verifyfile = os.path.exists(appdata + "\Assay Analyzer 2.0\D50238\CustomParameters.dat")
    # if verifyfile == True:
    #     with open(appdata + "\Assay Analyzer 2.0\D50238\History.xml", 'r') as file:
    #         if verifydata in file.read():
    #             print("data verified")
    #             return True
    #         else:
    #             return False

    path = os.getcwd() + "/open_tejas.bat"
    subprocess.call(path)
    desired_caps = {}
    desired_caps["app"] = "Root"
    global driver
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723',
        desired_capabilities=desired_caps)
    driver.implicitly_wait(60)

    tejasWindow = driver.find_element_by_accessibility_id("AutomationId_MainWindow")
    print(tejasWindow)
    windowHandle = tejasWindow.get_attribute("NativeWindowHandle")
    print(windowHandle)
    int_window = int(windowHandle)
    windowHandle = hex(int_window)
    print(windowHandle)
    new_caps = {}
    new_caps["appTopLevelWindow"] = windowHandle
    new_caps["platformName"] = "Windows"
    new_caps["deviceName"] = "WindowsPC"

    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723',
        desired_capabilities=new_caps)
    driver.implicitly_wait(10)
    yield driver
    verify = driver.find_element_by_name("ASSAY ANALYZER 2.0").is_displayed()
    return verify
#
# @pytest.fixture(scope='session', autouse=True)
# def teardown():
#     yield
#     test_assaycustomchip.test_close_desktopapp