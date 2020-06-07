import unittest
from pathlib import Path

from appium import webdriver
import subprocess, sys
from subprocess import Popen, PIPE
import os
from os import path
import keyboard
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
from testrail import *
from allure_commons.types import AttachmentType
import json
import allure
from robot.libraries.BuiltIn import BuiltIn
import timeit
from selenium.webdriver.common.keys import Keys


# sys.path.append(r'C:\Users\Fleek\PycharmProjects\tejastest\venv\testrail.py')


# addImagePath(common.cfgImageLibrary)

# s = Screen()
# timeout = 2

# ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
class assay():
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    global client
    global run_id
    run_id = None
    client = APIClient('https://berkeleylights.testrail.io/')
    client.user = 'ashish.rawat@berkeleylights.com'
    client.password = 'Fleek@2016'

    def __init__(self, driver):
        self.driver = driver

    def createTestRun(self, test_ids=[], name="Assay Analyzer 2.0 Automated Smoke Test NON-CLD"):
        response = client.send_post(
            'add_run/1',
            {'suite_id': 1,
             'name': name,
             'include_all': False,
             'case_ids': test_ids
             }
        )
        global run_id
        run_id = str(response["id"])

    def closeTestRun(self):
        global run_id
        response = client.send_post(
            'close_run/' + run_id,
            {}
        )

    def updateTestCase(self, testCaseId, result):
        global run_id
        if result == "pass":
            status = 1
        elif result == "fail":
            status = 5
        # else:
        # self.log.failed("Unknows Status ID for TestRail test update. Please use 'pass' or 'fail' for the tests.")
        print(testCaseId)
        print(run_id)
        response = client.send_post(
            'add_result_for_case/' + run_id + '/' + testCaseId,
            {
                'status_id': status,
                'comment': 'Test Executed - Status updated from Automated Smoke Test Suite'
            }
        )
    def capture_page_screenshot(self):
        ul = BuiltIn().get_library_instance('SeleniumLibrary')
        path = ul.capture_page_screenshot()
        # allure.attach.file(path, name="screenshot", attachment_type=allure.attachment_type.JPG)
        allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        # return path

    def case_fields(self, testid):
        global run_id
        response = client.send_get(
            'get_case/' + testid
        )
        print("printing response.")
        # print json.dumps(response, sort_keys=True, indent=4)
        print("Title")
        print
        response["title"]
        print("Steps:-")
        print
        response["custom_steps"]
        print("Expected Output:")
        print
        response["custom_expected"]

    '''Testcase T35911'''

    def start_tejas(self):
        path = os.getcwd() + "/open_tejas.bat"
        subprocess.call(path)
        desired_caps = {}
        desired_caps["app"] = "Root"
        global driver
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=desired_caps)
        driver.implicitly_wait(30)

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
        driver.implicitly_wait(60)
        verify = driver.find_element_by_name("ASSAY ANALYZER 2.0").is_displayed()
        return verify

    def close(self):
        self.driver.find_element_by_accessibility_id("PART_Close").click()
        self.driver.find_element_by_accessibility_id("DiscardButton").click()
        self.driver.quit()

    """42395"""

    # def verify_columncsv(self):
    #     self.driver.find_element_by_accessibility_id(
    #         "AutomationId_SettingsWindow_SettingsMenu_MenuElement_ColumnsByCSVType").click()
    #     time.sleep(3)
    #     self.driver.find_element_by_accessibility_id(
    #         "AutomationId_SettingsWindow_ColumnsByCSVTypeView_ColumnsListBySelectedType_ColumnName_Target_Index").click()
    #     self.driver.find_element_by_name("Apply").click()


