import unittest
from filecmp import cmp
from pathlib import Path

import pytest
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

    '''Testcase T35912'''

    @allure.step('to maximize assay analyzer window')
    def maximize(self):
        self.driver.find_element_by_accessibility_id("MaximizeButton").click()
        # allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    '''Testcase T35913'''

    @allure.step('to verify assay analyzer logo')
    def logo_verify(self):
        verify = self.driver.find_element_by_accessibility_id("PART_WindowTitleThumb").is_displayed()
        return verify

    '''TestCase T35885'''

    @allure.step('to verify save button in workbook element')
    def workbook_explorer_save(self):
        save = self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Save").is_displayed()
        return save

    @allure.step('to verify open button in workbook explorer')
    def workbook_explorer_openworkbook(self):
        openworkbook = self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Open").is_displayed()
        return openworkbook

    @allure.step('to verify add chip folder button in workbook explorer')
    def workbook_explorer_addchip(self):
        addchip = self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddChipFolder(s)").is_displayed()
        return addchip

    @allure.step('to verify add new filter button in workbook explorer')
    def workbook_explorer_addfilter(self):
        addfilter = self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddNewFilter").is_displayed()
        return addfilter

    @allure.step('to verify add new graph button in workbook explorer')
    def workbook_explorer_addgraph(self):
        addgraph = self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddNewGraph").is_displayed()
        return addgraph

    '''TestCase T35916

        def create_workbook_type(self):
            driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
            driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_Settings").click()
            driver.find_element_by_name("Workbook Types").click()
            driver.find_element_by_accessibility_id(
                "AutomationId_SettingsWindow_AppLevel_TemplateBuilder_WorkflowsView_Workflows_Add").click()
            driver.find_element_by_accessibility_id(
                "AutomationId_SettingsWindow_AppLevel_TemplateBuilder_ManageWorkflowView_WorkflowName").send_keys("CLD")
            driver.find_element_by_accessibility_id(
                "AutomationId_SettingsWindow_AppLevel_TemplateBuilder_ManageWorkflowView_Apply").click()
            cld = driver.find_element_by_accessibility_id("AutomationId_SettingsWindow_AppLevel_TemplateBuilder_WorkflowsView_Workflows_Item_CLD").is_displayed()
            driver.find_element_by_accessibility_id("AutomationId_SettingsWindow_Apply").click()
            return cld

        def remove_workbook_type(self):
            #driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
            driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
            driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_Settings").click()
            driver.find_element_by_name("Workbook Types").click()
            driver.find_element_by_accessibility_id("AutomationId_SettingsWindow_AppLevel_TemplateBuilder_WorkflowsView_Workflows_Item_CLD").click()
            driver.find_element_by_accessibility_id("AutomationId_SettingsWindow_AppLevel_TemplateBuilder_WorkflowsView_Workflows_Remove").click()
            driver.find_element_by_accessibility_id("AutomationId_SettingsWindow_Apply").click()
            time.sleep(5)'''

    '''TestCase T35917'''

    @allure.step('to open CLD chip from new workbook')
    def open_workbook_type(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_NewWorkbook").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_CLD").click()
        # driver.find_element_by_accessibility_id("CancelButton").click()
        verify = self.driver.find_element_by_name("CLD.").is_displayed()
        return verify

    '''TestCase T35886'''

    @allure.step('to add chip from add chip folder')
    def add_chip(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddChipFolder(s)").click()
        time.sleep(3)
        self.driver.find_element_by_name("Desktop (pinned)").click()
        time.sleep(3)
        self.driver.find_element_by_name("D37712").click()
        time.sleep(2)
        # driver.find_element_by_accessibility_id("0").click()
        self.driver.find_element_by_accessibility_id("1").click()
        chip = self.driver.find_element_by_name("D37712").is_displayed()
        return chip

    def time_start(self):

        global start
        start = timeit.default_timer()

    def time_stop(self):
        stop = timeit.default_timer()
        execution_time = str(stop - start) + " sec"
        # print("Program Executed in " + str(execution_time))
        return execution_time

    '''TestCase T35887'''

    @allure.step('to right cick chip to verify options')
    def verify_option_chip(self):
        global actionchains
        actionchains = ActionChains(self.driver)
        chip = self.driver.find_element_by_name("D37712")
        actionchains.context_click(chip).perform()

    @allure.step('to verify open timeline option')
    def verify_timeline(self):
        timeline = self.driver.find_element_by_name("Open in Timeline").is_displayed()
        return timeline

    @allure.step('to verify open gallery option')
    def verify_gallery(self):
        gallery = self.driver.find_element_by_name("Open in Gallery").is_displayed()
        return gallery

    @allure.step('to verify open in raw data option')
    def verify_rawdata(self):
        rawdata = self.driver.find_element_by_name("Open in Raw Data").is_displayed()
        return rawdata

    @allure.step('to verify remove chips option')
    def verify_remove(self):
        remove = self.driver.find_element_by_name("Remove chip(s)").is_displayed()
        return remove

    @allure.step('to verify reload reload chip option')
    def verify_reload(self):
        reload = self.driver.find_element_by_name("Reload chip(s)").is_displayed()
        return reload

    @allure.step('to verify open containing folder option')
    def verify_containing_folder(self):
        containingFolder = self.driver.find_element_by_name("Open Containing Folder").is_displayed()
        return containingFolder

    '''TestCase 750'''

    @allure.step('to click new filter button and verify new filter window')
    def click_filter(self):
        self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddNewFilter").click()
        filter = self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder")
        verify = filter.get_attribute("Name")
        return verify

    '''TestCase 751'''

    def hide_chips(self):
        self.driver.find_element_by_accessibility_id("Expander").click()
        hide = self.driver.find_element_by_name("D50238").is_displayed()
        self.driver.find_element_by_accessibility_id("Expander").click()
        return hide

    '''TestCase T35888'''

    @allure.step('to verify open chip timeline window')
    def open_timeline(self):
        chip = self.driver.find_element_by_name("D37712")
        actionchains = ActionChains(self.driver)
        actionchains.context_click(chip).perform()
        self.driver.find_element_by_name("Open in Timeline").click()
        time.sleep(5)
        timeline = self.driver.find_element_by_accessibility_id("AutomationId_TimeLine")
        verify = timeline.get_attribute("Name")

        return verify

    @allure.step('to verify close chip timeline window')
    def close_timeline(self):
        actionchains = ActionChains(self.driver)
        timeline = self.driver.find_element_by_accessibility_id("AutomationId_TimeLine")
        actionchains.context_click(timeline).perform()
        self.driver.find_element_by_name("Hide").click()

    '''TestCase T35889'''

    @allure.step('to open gallery window')
    def open_gallery(self):
        actionchains = ActionChains(self.driver)
        time.sleep(2)
        chip = self.driver.find_element_by_name("D37712")
        actionchains.context_click(chip).perform()
        galopen = self.driver.find_element_by_name("Open in Gallery")
        galopen.click()
        time.sleep(12)
        gallery = self.driver.find_element_by_name("Gallery").is_displayed()
        return gallery

    @allure.step('to close gallery window')
    def close_gallfil(self):
        actionchains = ActionChains(self.driver)
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery").click()
        gallery = self.driver.find_element_by_accessibility_id("AutomationId_Gallery")
        actionchains.context_click(gallery).perform()
        time.sleep(2)
        self.driver.find_element_by_name("Hide").click()

    @allure.step('to close gallery window')
    def close_gallery(self):
        time.sleep(3)
        actionchains = ActionChains(self.driver)
        gal = self.driver.find_element_by_accessibility_id("AutomationId_Gallery")
        gal.click()
        gallery = self.driver.find_element_by_accessibility_id("AutomationId_Gallery")
        actionchains.context_click(gallery).perform()
        time.sleep(2)
        self.driver.find_element_by_name("Hide").click()

    '''TestCase T35890'''

    @allure.step('to open raw data window')
    def open_raw_data(self):
        chip = self.driver.find_element_by_name("D37712")
        actionchains = ActionChains(self.driver)
        actionchains.context_click(chip).perform()
        self.driver.find_element_by_name("Open in Raw Data").click()
        time.sleep(5)
        raw = self.driver.find_element_by_accessibility_id("AutomationId_RawData")
        verify = raw.get_attribute("Name")
        time.sleep(3)
        return verify

    @allure.step('to close raw data window')
    def close_raw_data(self):
        time.sleep(3)
        actionchains = ActionChains(self.driver)
        raw = self.driver.find_element_by_accessibility_id("AutomationId_RawData")
        actionchains.context_click(raw).perform()
        time.sleep(3)
        self.driver.find_element_by_name("Hide").click()

    '''TestCase 755'''

    def remove_chip(self):
        actionchains = ActionChains(self.driver)
        chip = self.driver.find_element_by_name("D50238")
        actionchains.context_click(chip).perform()
        self.driver.find_element_by_name("Remove chip(s)").click()
        self.driver.find_element_by_accessibility_id("OKButton").click()
        try:
            a = self.driver.find_element_by_name("D50238").is_displayed()
            return a
        except:
            b = False
            return b

    '''TestCase 756'''

    def verify_save_workbook(self):
        self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Save").click()
        save = self.driver.find_element_by_accessibility_id("1")
        verify = save.get_attribute("Name")
        self.driver.find_element_by_accessibility_id("2").click()
        return verify

    '''TestCase 757'''

    def save_workbook(self):
        self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Save").click()
        self.driver.find_element_by_accessibility_id("1001").send_keys("reordercol")
        self.driver.find_element_by_accessibility_id("1").click()
        try:
            time.sleep(3)
            data = self.driver.find_element_by_name("Save As")
            data1 = data.is_displayed()
        except:
            data1 = False

        if data1 == True:
            self.driver.find_element_by_name("Yes").click()

    '''TestCase 758'''

    def open_workbook(self):
        self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Open").click()
        time.sleep(3)
        self.driver.find_element_by_name("reordercol.workbook").click()
        self.driver.find_element_by_accessibility_id("1").click()

    '''TestCase 126332'''

    def new_graph(self):
        self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddNewGraph").click()
        time.sleep(2)
        graph = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder")
        verify = graph.get_attribute("Name")
        return verify

    '''Chip Timeline TestCases'''

    '''TestCase 761 '''

    @allure.step('to verify timeline view in chiptimeline')
    def verify_chiptimeline_timeline_view(self):
        view = self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ChipTimeline").is_displayed()
        return view

    @allure.step('to verify matching grid in chiptimeline')
    def verify_chiptimeline_matching_grid(self):
        grid = self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ChipColumns").is_displayed()
        return grid

    '''TestCase T35914'''

    @allure.step('to open data template from settings')
    def verify_data_import_templates_element(self):
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Settings").click()
        self.driver.find_element_by_name("Data Import Template").click()

    @allure.step('to verify CLD chip in data import template')
    def verify_data_import_templates_element_cld(self):
        cld = self.driver.find_element_by_name("CLD").is_displayed()
        return cld

    @allure.step('to verify add button in data import template')
    def verify_data_import_templates_element_add(self):
        add = self.driver.find_element_by_name("Add").is_displayed()
        return add

    @allure.step('to verify edit button in data import template')
    def verify_data_import_templates_element_edit(self):
        edit = self.driver.find_element_by_name("Edit").is_displayed()
        return edit

    @allure.step('to verify copy button in data import template')
    def verify_data_import_templates_element_copy(self):
        copy = self.driver.find_element_by_name("Copy").is_displayed()
        return copy

    @allure.step('to verify remove button in data import template')
    def verify_data_import_templates_element_remove(self):
        remove = self.driver.find_element_by_name("Remove").is_displayed()
        return remove

    @allure.step('to verify import button in data import template')
    def verify_data_import_templates_element_import(self):
        imp = self.driver.find_element_by_name("Import").is_displayed()
        return imp

    @allure.step('to verify export button in data import template')
    def verify_data_import_templates_element_export(self):
        export = self.driver.find_element_by_name("Export").is_displayed()
        self.driver.find_element_by_name("Cancel").click()
        return export

    '''TestCase T35915'''

    @allure.step('to open wprkbooktypes from settings')
    def verify_workbook_type_element(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Settings").click()
        self.driver.find_element_by_name("Workbook Types").click()

    @allure.step('to verify custom chip in data import template')
    def verify_workbook_type_element_custom(self):
        custom = self.driver.find_element_by_accessibility_id(
            "AutomationId_SettingsWindow_AppLevel_TemplateBuilder_WorkflowsView_Workflows_Item_Custom").is_displayed()
        return custom

    @allure.step('to verify add button in data import template')
    def verify_workbook_type_element_add(self):
        add = self.driver.find_element_by_accessibility_id(
            "AutomationId_SettingsWindow_AppLevel_TemplateBuilder_WorkflowsView_Workflows_Add").is_displayed()
        return add

    @allure.step('to verify edit button in data import template')
    def verify_workbook_type_element_edit(self):
        edit = self.driver.find_element_by_accessibility_id(
            "AutomationId_SettingsWindow_AppLevel_TemplateBuilder_WorkflowsView_Workflows_Edit").is_displayed()
        return edit

    @allure.step('to verify copy button in data import template')
    def verify_workbook_type_element_copy(self):
        copy = self.driver.find_element_by_accessibility_id(
            "AutomationId_SettingsWindow_AppLevel_TemplateBuilder_WorkflowsView_Workflows_Copy").is_displayed()
        return copy

    @allure.step('to verify remove button in data import template')
    def verify_workbook_type_element_remove(self):
        remove = self.driver.find_element_by_accessibility_id(
            "AutomationId_SettingsWindow_AppLevel_TemplateBuilder_WorkflowsView_Workflows_Remove").is_displayed()
        self.driver.find_element_by_accessibility_id("AutomationId_SettingsWindow_Cancel").click()
        return remove

    '''TestCase T35918'''

    def cld_workbook(self):
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_NewWorkbook").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_CLDWorkbook").click()

    '''TestCase T35904'''

    def raw_data_column_sorting(self):
        self.driver.find_element_by_accessibility_id("PenId").click()
        time.sleep(3)
        sort = self.driver.find_element_by_accessibility_id("CellElement_0_1")
        element = sort.get_attribute("Name")
        return element

    def raw_data_column_sorting1(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("PenId").click()
        time.sleep(6)
        sort = self.driver.find_element_by_accessibility_id("CellElement_0_1")
        abc = sort.get_attribute("Name")
        self.driver.find_element_by_accessibility_id("PenId").click()
        time.sleep(1)
        return abc

    '''TestCase T35906'''

    def raw_data_new_parameter(self):
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_NewParameter").click()
        verify = self.driver.find_element_by_name("NEW PARAMETER").is_displayed()
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_ParameterEditor_Close").click()
        return verify

    '''TestCase T35907'''

    def raw_data_add_new_parameter(self):
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_NewParameter").click()
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_ParameterEditor_Entries").click()
        time.sleep(3)

        actionchains = ActionChains(self.driver)
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.ARROW_UP).perform()
        actionchains.send_keys(Keys.RETURN).perform()

        time.sleep(5)

        self.driver.find_element_by_accessibility_id("AutomationId_RawData_ParameterEditor_ParameterInput").send_keys(
            "parameter")
        self.driver.find_element_by_name("Fields").click()
        element = self.driver.find_element_by_name("[Empty : CellCount]")
        actionchains = ActionChains(self.driver)
        actionchains.double_click(element).perform()

        self.driver.find_element_by_accessibility_id("Multiply").click()

    def penid_attribute(self):
        actionchains = ActionChains(self.driver)
        penid = self.driver.find_element_by_name("[Empty : PenId]")
        actionchains.double_click(penid).perform()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_ParameterEditor_Apply").click()

    def raw_data_verify_parameter(self):
        self.driver.find_element_by_name("ChipId").click()
        actionchains = ActionChains(self.driver)
        for x in range(0, 10):
            actionchains.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(5)
        parameter = self.driver.find_element_by_name("Empty : parameter").is_displayed()
        return parameter

    def raw_data_verify_parameter_in_grid(self):
        for x in range(0, 18):
            self.driver.find_element_by_accessibility_id("HorizontalLargeIncrease").click()
        grid = self.driver.find_element_by_accessibility_id("Empty : parameter").is_displayed()
        return grid

    '''TestCase T35907'''

    '''def raw_data_add_new_parameter(self):
            driver.find_element_by_accessibility_id("AutomationId_RawData_NewParameter").click()
            driver.find_element_by_accessibility_id("AutomationId_RawData_ParameterEditor_Entries").click()
            time.sleep(3)
            driver.find_element_by_accessibility_id("AutomationId_RawData_ParameterEditor_Entries_Item_Empty").click()
            driver.find_element_by_accessibility_id("RichTextBox").send_keys("shivam")
            driver.find_element_by_name("Fields").click()
            element = driver.find_element_by_name("[Load-3 : CellCount]")
            actionchains = ActionChains(driver)
            actionchains.double_click(element).perform()
            driver.find_element_by_name("Operators").click()
            mul = driver.find_element_by_name(" * ")
            actionchains.double_click(mul).perform()
            driver.find_element_by_accessibility_id("PART_ExpressionNodeEditor").click()
            time.sleep(3)
            driver.find_element_by_accessibility_id("PART_ExpressionNodeEditor").send_keys("2")
            driver.find_element_by_accessibility_id("AutomationId_RawData_ParameterEditor_Apply").click()
            time.sleep(5)'''

    def raw_data(self):
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_NewParameter").click()
        driver.find_element_by_accessibility_id("RichTextBox").send_keys("shivam")

    '''TestCase C222520'''

    def raw_data_drag_drop(self):
        time.sleep(3)
        actionchains = ActionChains(self.driver)
        drag = self.driver.find_element_by_accessibility_id("Assay : Cube")
        drop = self.driver.find_element_by_name("GridViewGroupPanel")
        actionchains.drag_and_drop(drag, drop).perform()
        time.sleep(3)

    def raw_data_drag_drop_items(self):
        actionchains = ActionChains(self.driver)
        drag = self.driver.find_element_by_accessibility_id("PenId")
        drop = self.driver.find_element_by_name("GridViewGroupPanel")
        actionchains.drag_and_drop(drag, drop).perform()
        # time.sleep(2)
        # driver.find_element_by_accessibility_id("ExpanderButton").click()
        # verify = driver.find_element_by_accessibility_id("GroupRow_D50238_2").is_displayed()
        # return verify

    '''TestCase T35654'''

    def raw_data_remove_grouping(self):
        self.driver.find_element_by_accessibility_id("PART_CloseButton").click()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("PART_CloseButton").click()

    '''TestCase C222520'''

    @allure.step('Drag and drop position of attribute in raw data and verify reordering happen')
    def raw_data_reordering_column(self):
        actionchains = ActionChains(self.driver)
        # self.driver.find_element_by_accessibility_id("PenId").click()
        time.sleep(3)
        sort = self.driver.find_element_by_accessibility_id("CellElement_0_1")
        element = sort.get_attribute("Name")
        time.sleep(3)
        # verify = self.driver.find_element_by_accessibility_id("CellElement_0_1").is_displayed()
        drag = self.driver.find_element_by_accessibility_id("PenId")
        drop = self.driver.find_element_by_accessibility_id("Assay : Cube")
        actionchains.drag_and_drop(drag, drop).perform()
        time.sleep(2)
        return element

    def raw_data_verifyreordering(self):
        getcount = self.driver.find_element_by_accessibility_id("CellElement_0_2")
        verifycount = getcount.get_attribute("Name")
        # print(verifycount)
        return verifycount

        try:
            # data = self.driver.find_element_by_accessibility_id("CellElement_0_3")
            data1 = verifycount.is_displayed()
            return data1
        except:
            data2 = False
            return data2

    """Testcase C234945"""

    @allure.step('to open AbD chip from new workbook')
    def open_AbDworkbook_type(self):
        self.driver.find_element_by_name("Cancel").click()
        time.sleep(4)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_NewWorkbook").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_AbD").click()
        # driver.find_element_by_accessibility_id("CancelButton").click()
        try:
            self.driver.find_element_by_name("Confirmation").is_displayed()
            time.sleep(2)
            self.driver.find_element_by_name("No").click()
        except:
            print("confirmation is not displayed")
        time.sleep(2)
        verify = self.driver.find_element_by_name("AbD.").is_displayed()
        return verify

    """Testcase C234939"""

    @allure.step('to delete history.xml file')
    def deletehistoryfile(self):
        desktop = str(os.path.join(Path.home(), "Desktop\D37712"))
        try:
            if os.path.isfile(desktop + "\history.xml"):
                os.remove(desktop + "\history.xml")
        except:
            print("history file not found")

    @allure.step('To open T-cell workbook')
    def open_Tcellworkbook(self):
        time.sleep(4)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_NewWorkbook").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_T-Cell").click()
        # driver.find_element_by_accessibility_id("CancelButton").click()
        try:
            verify1 = self.driver.find_element_by_name("Confirmation").is_displayed()
            time.sleep(2)
            self.driver.find_element_by_name("No").click()
        except:
            print('confirmation page not dispalyed')
        time.sleep(2)
        verify = self.driver.find_element_by_name("T-Cell.").is_displayed()
        return verify

    def verify_alertwindow(self):
        verify = self.driver.find_element_by_name("Alert").is_displayed()
        time.sleep(2)
        self.driver.find_element_by_name("OK").click()
        return verify

    @allure.step('verify dataset/chip location')
    def verify_chiplocation(self):
        appdata = os.getenv('APPDATA')
        print(appdata)
        # os.remove(appdata + "\Assay Analyzer 2.0\D37712\CLD.History.xml")
        # chip = self.driver.find_element_by_name("D37712")
        # actionchains.context_click(chip).perform()
        # self.driver.find_element_by_name("Open in Timeline").click()
        time.sleep(3)
        verifyfile = path.exists(appdata + "\Assay Analyzer 2.0\D37712\CLD.History.xml")
        return verifyfile

    def verify_CLDopen(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_NewWorkbook").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_CLD").click()
        time.sleep(2)
        self.driver.find_element_by_name("Confirmation").is_displayed()
        time.sleep(2)
        self.driver.find_element_by_name("No").click()

    @allure.step('verify history file generated or not')
    def verify_historyfile(self):
        desktop = str(os.path.join(Path.home(), "Desktop\D37712"))
        try:
            if os.path.isfile(desktop + "\history.xml"):
                return True
        except:
            b = False
            return b

    '''TestCase C222521'''

    @allure.step('Drag and drop position of attribute in raw data')
    def raw_data_column_drag(self):
        actionchains = ActionChains(self.driver)
        drop = self.driver.find_element_by_name("Assay : CellCount")
        drag = self.driver.find_element_by_name("PenId")
        actionchains.drag_and_drop(drag, drop).perform()

    # @allure.step('arrange in default position of grid in raw data')
    # def verify_changetodefault_grid(self):

    # drag = self.driver.find_element_by_accessibility_id("Assay : Cube")
    # drop =  self.driver.find_element_by_accessibility_id("PenId")
    # actionchains.drag_and_drop(drag, drop).perform()

    '''TestCase T35600'''

    def chip_timeline_open_from_window(self):
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Window").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Windows").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_ChipTimeline").click()
        verify = self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ChipTimeline").is_displayed()
        return verify

    '''TestCase T35899'''

    @allure.step('to add chip in new filter window')
    def add_chip_in_filter(self):
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_Chips").click()
        self.driver.find_element_by_name("D37712").click()
        # self.driver.find_element_by_name("D37712").click()
        time.sleep(3)

    '''comment'''
    '''TestCase T35900'''

    @allure.step('to add filter name in new filter window')
    def filter_name(self, name):
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_FilterName").send_keys(name)
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("HeaderCloseButton").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("HeaderDropDownMenu").click()
        time.sleep(2)
        self.driver.find_element_by_name("Tabbed document").click()
        time.sleep(3)

    """testcase 30567"""

    @allure.step('to open filter in tabbed document')
    def filter_tabbed(self):
        time.sleep(2)
        open = self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder")
        time.sleep(2)
        open.click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("HeaderCloseButton").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("HeaderDropDownMenu").click()
        time.sleep(2)
        self.driver.find_element_by_name("Tabbed document").click()
        time.sleep(3)

    @allure.step('to close filter window')
    def close_filter(self):
        time.sleep(2)
        # self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder").click()
        close = self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder")
        close.click()
        time.sleep(3)
        actionchains = ActionChains(self.driver)
        actionchains.context_click(close).perform()
        time.sleep(2)
        self.driver.find_element_by_name("Hide").click()

    '''TestCase T35901'''

    @allure.step('to click add condition button')
    def add_condition_filter(self):
        self.driver.implicitly_wait(100)
        plus_icon = self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_AddCondition")
        time.sleep(2)
        plus_icon.click()
        time.sleep(2)
        select = self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_DimensionSelector")
        time.sleep(2)
        select.click()
        # driver.find_element_by_name("PenId").click()
        time.sleep(2)

    @allure.step('to parameter from drop down')
    def abc(self):
        select = self.driver.find_element_by_name("Empty:Cell_Count")
        time.sleep(2)
        select.click()
        time.sleep(2)

    @allure.step('to verify penid in dropdown')
    def penid(self):
        pen = self.driver.find_element_by_name("PenId").is_displayed()
        return pen

    @allure.step('to verify penstate in dropdown')
    def pen_state(self):
        state = self.driver.find_element_by_name("PenState").is_displayed()
        # state = driver.find_element_by_name("PenState1").is_displayed()
        return state

    @allure.step('to verify empty:penid in dropdown')
    def Empty_pen_filter(self):
        time.sleep(3)
        select = self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_DimensionSelector")
        time.sleep(2)
        select.click()
        select1 = self.driver.find_element_by_accessibility_id("PART_EditableTextBox").send_keys("Empty")
        penid = self.driver.find_element_by_name("Empty:Pen_Id").is_displayed()
        return penid

    @allure.step('to verify empty:deviceid in dropdown')
    def Empty_device_id(self):
        time.sleep(2)
        deviceid = self.driver.find_element_by_name("Empty:Device_Id").is_displayed()
        return deviceid

    @allure.step('to verify empty:cellcountverified in dropdown')
    def Empty_cell_count_verified(self):
        cellcount = self.driver.find_element_by_name("Empty:Cell_Count_Verified").is_displayed()
        return cellcount

    @allure.step('to verify empty:cellcount in dropdown')
    def Empty_cell_count(self):
        loadcellcount = self.driver.find_element_by_name("Empty:Cell_Count").is_displayed()
        return loadcellcount

    @allure.step('to verify empty:celltype in dropdown')
    def load_celltype(self):
        celltype = self.driver.find_element_by_name("Empty:Cell_Type").is_displayed()
        return celltype

    @allure.step('to verify load3:penid in dropdown')
    def load_pen_id(self):
        loadpenid = self.driver.find_element_by_name("Load-3:PenId").is_displayed()
        return loadpenid

    @allure.step('to verify load3:celcountverified in dropdown')
    def cell_count_verified(self):
        cellcountverified = self.driver.find_element_by_name("Load-3:CellCountVerified").is_displayed()
        return cellcountverified

    @allure.step('to verify load3:cellcount in dropdown')
    def cell_count(self):
        cellcounts = self.driver.find_element_by_name("Load-3:CellCount").is_displayed()
        return cellcounts

    @allure.step('to verify load3:celltype in dropdown')
    def cell_type(self):
        celltypes = self.driver.find_element_by_name("Load-3:CellType").is_displayed()
        return celltypes

    '''TestCase T35903'''

    @allure.step('to close filter window')
    def filter_close(self):
        time.sleep(3)
        actionchains = ActionChains(self.driver)
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_SaveFilter").click()
        time.sleep(2)
        close = self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder")
        actionchains.context_click(close).perform()
        self.driver.find_element_by_name("Hide").click()

    @allure.step('to save filter button oneD and verify saved filter')
    def filter_save_button_oned(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Window").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_New").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_WorkbookExplorer").click()
        time.sleep(5)
        verify = self.driver.find_element_by_name("fil").is_displayed()
        return verify

    '''TestCase T35984'''

    def verify_savefilter(self):
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_SaveFilter").click()
        time.sleep(2)

    @allure.step('to save filter button twoD and verify saved filter')
    def filter_save_button_twod(self):
        time.sleep(2)
        verify = self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_ContextMenu_ElementsTree_Element_Fil2").is_displayed()
        return verify

    '''Testcase T35983'''

    @allure.step('to add twoD condition in filter')
    def filter_twod_condition(self):
        # actionchains = ActionChains(driver)
        '''driver.find_element_by_accessibility_id("HeaderCloseButton").click()
            driver.find_element_by_accessibility_id("HeaderDropDownMenu").click()
            driver.find_element_by_name("Tabbed document").click()'''
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_FilterDimension").click()
        self.driver.find_element_by_name("2-D").click()
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_AddCondition").click()
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_AggregationMode").click()
        # time.sleep(3)
        self.driver.find_element_by_name("Max").click()

    @allure.step('to click xaxis attribute in filter')
    def filter_twod_xaxis(self):
        actionchains = ActionChains(self.driver)
        time.sleep(8)
        xaxis = self.driver.find_element_by_accessibility_id(
            "AutomationId_FilterBuilder_2DFilter_XAxis_Values").is_displayed()

        select = self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_2DFilter_XAxis_Values")
        select.click()
        time.sleep(2)
        for x in range(0, 6):
            actionchains.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(4)
        # time.sleep(3)
        self.driver.find_element_by_name("Empty:Cell_Count_Verified").click()
        return xaxis

    @allure.step('to click yaxis attribute in filter')
    def filter_twod_yaxis(self):
        time.sleep(3)
        yaxis = self.driver.find_element_by_accessibility_id(
            "AutomationId_FilterBuilder_2DFilter_YAxis_Values")
        yaxis.click()
        # drpdown=self.driver.find_element_by_accessibility_id("RadComboBox")
        # drpdown[2].click()
        time.sleep(2)
        for x in range(0, 3):
            self.driver.find_element_by_accessibility_id("VerticalLargeIncrease").click()

        # self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_2DFilter_YAxis_Values")
        # yaxis.click()
        time.sleep(2)
        # axis_select = self.driver.find_element_by_accessibility_id("PART_EditableTextBox")
        # axis_select.send_keys("Empty")
        self.driver.find_element_by_name("Empty:Cell_Count_Verified").click()
        # return yaxis

    @allure.step('to verify 2D filter chart')
    def filter_verify_chart(self):
        verify = self.driver.find_element_by_accessibility_id(
            "AutomationId_FilterBuilder_2DFilter_Chart").is_displayed()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Window").click()
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_New").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_WorkbookExplorer").click()
        return verify

    '''TestCase T35627'''

    def filter_select_string_parameter(self):
        self.driver.find_element_by_name("Load-3:Device_Id").click()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_StringFilter_Items").click()
        self.driver.find_element_by_name("D50238").click()
        verify = self.driver.find_element_by_name("1535").is_displayed()
        return verify

    '''TestCase T35893'''

    @allure.step('to open settings in gallery')
    def gallery_setting(self):
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery_OpenSettings").click()

    @allure.step('to verify visible option in gallery settings')
    def visible(self):
        visible = self.driver.find_element_by_accessibility_id("Visible").is_displayed()
        return visible

    @allure.step('to verify show rank option in gallery settings')
    def show_rank(self):
        rank = self.driver.find_element_by_accessibility_id("Show Rank").is_displayed()
        return rank

    @allure.step('to verify column name option in gallery settings')
    def column_name(self):
        column = self.driver.find_element_by_accessibility_id("Name").is_displayed()
        return column

    @allure.step('to verify column footer option in gallery settings')
    def column_footer(self):
        footer = self.driver.find_element_by_accessibility_id("Parameters").is_displayed()
        return footer

    @allure.step('to verify row height option in gallery settings')
    def row_height(self):
        height = self.driver.find_element_by_name("Row Height :").is_displayed()
        return height

    @allure.step('to verify digits after comma option in gallery settings')
    def digits_after_comma(self):
        digits = self.driver.find_element_by_name("Digits after comma :").is_displayed()
        return digits

    @allure.step('to verify pen reject approval option in gallery settings')
    def pen_reject_approval(self):
        pen = self.driver.find_element_by_accessibility_id(
            "AutomationId_GallerySettings_PenRejectApproval").is_displayed()
        self.driver.find_element_by_accessibility_id("AutomationId_GallerySettings_Close").click()
        return pen

    '''TestCase 35895'''

    def gallery_sort_element(self):
        self.driver.find_element_by_accessibility_id("Id").click()
        time.sleep(1)
        sort = self.driver.find_element_by_name("Pen_1").is_displayed()
        return sort

    def gallery_sort_element1(self):
        self.driver.find_element_by_accessibility_id("Id").click()
        time.sleep(1)
        sort = self.driver.find_element_by_name("Pen_1758").is_displayed()
        self.driver.find_element_by_accessibility_id("Id").click()
        return sort

    def attribute_showup_under_each_image_sequence(self):
        self.driver.find_element_by_accessibility_id()

    '''TestCase T35609'''

    def gallery_image_sequence_load3(self):
        load3 = self.driver.find_element_by_accessibility_id("Load-3").is_displayed()
        return load3

    def gallery_image_sequence_load5(self):
        load5 = self.driver.find_element_by_accessibility_id("Load-5").is_displayed()
        return load5

    def gallery_image_sequence_pe(self):
        pe = self.driver.find_element_by_accessibility_id("TPS-PE").is_displayed()
        return pe

    def gallery_image_sequence_fitc(self):
        fitc = self.driver.find_element_by_accessibility_id("TPS-FITC").is_displayed()
        return fitc

    '''TestCase T35610'''

    def gallery_show_rank(self):
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery_OpenSettings").click()
        self.driver.find_element_by_accessibility_id("CellElement_0_1").click()
        self.driver.find_element_by_accessibility_id("CellElement_1_1").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GallerySettings_Apply").click()
        verify = self.driver.find_element_by_name("1535").is_displayed()
        return verify

    '''TestCase T35612'''

    def gallery_increase_row_height(self):
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery_OpenSettings").click()
        self.driver.find_element_by_accessibility_id("increase").click()
        self.driver.find_element_by_accessibility_id("increase").click()
        self.driver.find_element_by_accessibility_id("increase").click()
        self.driver.find_element_by_accessibility_id("increase").click()
        self.driver.find_element_by_accessibility_id("increase").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GallerySettings_Apply").click()

    '''TestCase T35670'''

    def gallery_reorder_column(self):
        actionchains = ActionChains(self.driver)
        drag = self.driver.find_element_by_accessibility_id("Load-3")
        drop = self.driver.find_element_by_accessibility_id("TPS-PE")
        actionchains.drag_and_drop(drag, drop).perform()

    '''TestCase T35667'''

    def gallery_change_brightness_contrast(self):
        actionchains = ActionChains(self.driver)
        load = self.driver.find_element_by_accessibility_id("Load-3")
        actionchains.context_click(load).perform()
        self.driver.find_element_by_accessibility_id("IncreaseButton").click()
        self.driver.find_element_by_accessibility_id("IncreaseButton").click()
        self.driver.find_element_by_accessibility_id("IncreaseButton").click()
        self.driver.find_element_by_accessibility_id("IncreaseButton").click()
        self.driver.find_element_by_accessibility_id("IncreaseButton").click()
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery").click()

    '''TestCase T35615'''

    def gallery_visible_pens(self):
        visible = self.driver.find_element_by_name(" Visible 1535 of 1535 pens").is_displayed()
        return visible

    '''TestCase T35896'''

    def gallery_attribute_list(self):
        self.driver.find_element_by_accessibility_id("CellElement_0_0").click()

    def verify_attribute_penid(self):
        penid = self.driver.find_element_by_name("PenId: ").is_displayed()
        return penid

    def verify_attribute_deviceid(self):
        deviceid = self.driver.find_element_by_name("Device_Id: ").is_displayed()
        return deviceid

    def verify_attribute_cellcountverified(self):
        cell = self.driver.find_element_by_name("CellCountVerified: ").is_displayed()
        return cell

    def verify_attribute_cellcount(self):
        cellcount = self.driver.find_element_by_name("CellCount: ").is_displayed()
        return cellcount

    '''TestCases T35897'''

    def gallery_select_pens(self):
        pens = []
        pens = self.driver.find_elements_by_accessibility_id("ThreeStateSwitcher_Selected")
        for x in range(1, 4):
            pens[x].click()

    '''TestCase T35975'''

    def gallery_export_csv(self):
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery_ExportMenu_ExportToCSV").click()
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery_ExportToCSV_Export").click()
        verify = self.driver.find_element_by_name("Selected pens have been successfully exported.").is_displayed()
        self.driver.find_element_by_accessibility_id("OKButton").click()
        return verify

    '''TestCase T35974'''

    @allure.step('to select attributes in gallery settings')
    def gallery_select_data_attribute(self):
        element = []
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery_OpenSettings").click()
        self.driver.find_element_by_accessibility_id("VerticalLargeIncrease").click()
        element = self.driver.find_elements_by_accessibility_id("AutomationId_GallerySettings_ColumnFooters")
        actionchains = ActionChains(self.driver)
        actionchains.move_to_element_with_offset(element[6], 60, 65)
        actionchains.click()
        actionchains.perform()
        for x in range(0, 3):
            actionchains.send_keys(Keys.ARROW_DOWN).perform()
            actionchains.send_keys(Keys.RETURN).perform()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("CellElement_6_0").click()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_GallerySettings_Apply").click()
        return len(element)
        time.sleep(5)
        #
        #
        # element = []
        # self.driver.find_element_by_accessibility_id("AutomationId_Gallery_OpenSettings").click()
        # self.driver.find_element_by_accessibility_id("VerticalLargeIncrease").click()
        # time.sleep(4)
        # element1= self.driver.find_elements_by_accessibility_id("AutomationId_GallerySettings_ColumnFootersAlt")
        # # element1.click()
        # time.sleep(2)
        # actionchains = ActionChains(self.driver)
        # actionchains.move_to_element_with_offset(element[7], 50, 60)
        # actionchains.click()
        # actionchains.perform()
        # for x in range(0, 3):
        #     actionchains.send_keys(Keys.ARROW_DOWN).perform()
        #     actionchains.send_keys(Keys.RETURN).perform()
        # time.sleep(2)
        # self.driver.find_element_by_accessibility_id("CellElement_6_0").click()
        # time.sleep(3)
        # self.driver.find_element_by_accessibility_id("AutomationId_GallerySettings_Apply").click()
        # return len(element)
        # time.sleep(5)

    @allure.step('to verify Empty: PenId: is displayed')
    def verify_attribute1(self):
        verify1 = self.driver.find_element_by_name("Assay: PenId: ").is_displayed()
        return verify1

    @allure.step('to verify Empty: CellCountVerified: is displayed')
    def verify_attribute2(self):
        verify2 = self.driver.find_element_by_name("Assay: Score: ").is_displayed()
        return verify2

    @allure.step('to verify Empty: CellCount: is displayed')
    def verify_attribute3(self):
        verify3 = self.driver.find_element_by_name("Assay_2: PenId: ").is_displayed()
        return verify3

    @allure.step('to verify Load: PenId: is displayed')
    def verify_attribute4(self):
        verify4 = self.driver.find_element_by_name("Assay_2: Score: ").is_displayed()
        return verify4

    @allure.step('to verify Empty: parameter: is displayed')
    def verify_attribute5(self):
        verify5 = self.driver.find_element_by_name("Assay_2: rQP: ").is_displayed()
        return verify5

    @allure.step('to click export pdf in gallery and save pdf in explorer')
    def gallery_export_pdf(self):
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery_ExportMenu_ExportToPDF").click()
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery_ExportToPDF_Export").click()
        actionchains = ActionChains(self.driver)
        try:
            time.sleep(3)
            data = self.driver.find_element_by_name("data.pdf")
            data1 = data.is_displayed()
        except:
            data1 = False

        if data1 == True:
            data.click()
            actionchains.send_keys(Keys.DELETE).perform()

        self.driver.find_element_by_accessibility_id("1001").send_keys("data")
        self.driver.find_element_by_accessibility_id("1").click()
        time.sleep(5)
        self.driver.find_element_by_accessibility_id("CancelButton").click()

    '''TestCase T35910'''

    @allure.step('to verify parameter: is displayed')
    def raw_data_parameter_in_gallery(self):
        verify = self.driver.find_element_by_name("parameter: ").is_displayed()
        return verify

    '''TestCase T35894'''

    @allure.step('to click settings and select and verify CellCount: is displayed')
    def gallery_select_attribute(self):
        actionchains = ActionChains(self.driver)
        self.driver.find_element_by_accessibility_id("AutomationId_Gallery_OpenSettings").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GallerySettings_ColumnFooters").click()
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.RETURN).perform()
        time.sleep(10)
        # driver.find_element_by_accessibility_id("AutomationId_GallerySettings_ColumnFooters_Item_CellCount").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GallerySettings_Apply").click()
        cell = self.driver.find_element_by_name("CellCount: ").is_displayed()
        return cell

    '''TestCase T35969'''

    @allure.step('to verify empty image sequence in gallery')
    def gallery_image_sequence_empty(self):
        empty = self.driver.find_element_by_accessibility_id("Empty").is_displayed()
        return empty

    @allure.step('to verify load image sequence in gallery')
    def gallery_image_sequence_load(self):
        load = self.driver.find_element_by_accessibility_id("Load").is_displayed()
        return load

    @allure.step('to verify culture image sequence in gallery')
    def gallery_image_sequence_culture(self):
        culture = self.driver.find_element_by_accessibility_id("Culture").is_displayed()
        return culture

    @allure.step('to verify assay image sequence in gallery')
    def gallery_image_sequence_assay(self):
        assay = self.driver.find_element_by_accessibility_id("Assay").is_displayed()
        return assay

    @allure.step('to verify culture_2 image sequence in gallery')
    def gallery_image_sequence_culture2(self):
        culture2 = self.driver.find_element_by_accessibility_id("Culture_2").is_displayed()
        return culture2

    @allure.step('to verify assay_2 image sequence in gallery')
    def gallery_image_sequence_assay2(self):
        assay2 = self.driver.find_element_by_accessibility_id("Assay_2").is_displayed()
        return assay2

    '''TestCase T35621'''

    def gallery_custom_parameter_attribute(self):
        abc = self.driver.find_element_by_name("abc: ").is_displayed()
        return abc
    '''TestCase T35663


    def gallery_enlarge_image():
        actionchains = ActionChains(driver)
        image = driver.find_element_by_accessibility_id("PART_ImageHost")
        actionchains.double_click(image).perform()
        enlarged = driver.find_element_by_name("Enlarged Image").is_displayed()
        driver.find_element_by_accessibility_id("PART_Close").click()
        return enlarged '''

    '''TestCase T35970'''

    def add_graph_button(self):
        self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddNewGraph").click()
        graph = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder")
        verify = graph.get_attribute("Name")
        return verify

    def add_graph(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_GraphType").click()
        self.driver.find_element_by_name("Scatter Plot").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Chip").click()
        # driver.find_element_by_name("C:\Users\Fleek\Desktop\D50238").click()
        self.driver.find_element_by_name("D50238").click()
        verify = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot").is_displayed()
        return verify

    '''TestCase T35971'''

    def graph_builder_graph_type(self):
        graph = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_GraphType").is_displayed()
        return graph

    def graph_builder_chip(self):
        chip = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Chip").is_displayed()
        return chip

    def graph_builder_save_button(self):
        save = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Save")
        verify = save.get_attribute("Name")
        return verify

    def graph_builder_export(self):
        export = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Export").is_displayed()
        return export

    def graph_builder_setting(self):
        setting = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Settings").is_displayed()
        return setting

    def graph_builder_linktogallery(self):
        gallery = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_LinkToGallery")
        verify = gallery.get_attribute("Name")
        return verify

    def graph_builder_linktorawdata(self):
        raw = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_LinkToRawData")
        verify = raw.get_attribute("Name")
        return verify

    def graph_builder_select(self):
        select = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_SelectOrZoom")
        verify = select.get_attribute("Name")
        return verify

    def graph_builder_xaxis(self):
        xaxis = self.driver.find_element_by_accessibility_id(
            "AutomationId_GraphBuilder_ScatterPlot_XAxis_Values").is_displayed()
        return xaxis

    def graph_builder_yaxis(self):
        yaxis = self.driver.find_element_by_accessibility_id(
            "AutomationId_GraphBuilder_ScatterPlot_YAxis_Values").is_displayed()
        return yaxis

    def graph_builder_groupby(self):
        color = self.driver.find_element_by_accessibility_id(
            "AutomationId_GraphBuilder_ScatterPlot_Color").is_displayed()
        return color

    '''TestCase T35972'''

    def graph_builder_axis_attribute(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_XAxis_Values").click()
        self.driver.find_element_by_name("Load_3:Pen_Id").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_YAxis_Values").click()
        self.driver.find_element_by_name("Load_3:Cell_Count_Verified").click()
        time.sleep(2)
        graph = self.driver.find_element_by_accessibility_id(
            "AutomationId_GraphBuilder_ScatterPlot_Chart_Legend").is_displayed()
        return graph

    '''TestCase T35973'''

    def verify_legend(self):
        verify = self.driver.find_element_by_name("Undecided").is_displayed()
        return verify

    def graph_builder_change_groupby(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_Color").click()
        self.driver.find_element_by_name("Load_3:Cell_Type").click()
        time.sleep(5)
        verify = self.driver.find_element_by_name("Jurkat").is_displayed()
        return verify

    '''TestCase T35976'''

    def graph_builder_save(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Save").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_SaveGraph_Name").send_keys("graph")
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_SaveGraph_Apply").click()
        verify = self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_ContextMenu_ElementsTree_Element_Graph").is_displayed()
        return verify

    def close_graph(self):
        actionchains = ActionChains(self.driver)
        hide = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder")
        actionchains.context_click(hide).perform()
        self.driver.find_element_by_name("Hide").click()

    '''TestCase T35977'''

    def graph_builder_open_saved_graph(self):
        open = self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_ContextMenu_ElementsTree_Element_Graph")
        actionchains = ActionChains(self.driver)
        actionchains.double_click(open).perform()
        time.sleep(5)

    def verify_xaxis(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_XAxis_Values").click()
        xaxis = self.driver.find_element_by_name("Load_3:Pen_Id").is_displayed()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_XAxis_Values").click()
        return xaxis

    def verify_yaxis(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_YAxis_Values").click()
        yaxis = self.driver.find_element_by_name("Load_3:Cell_Count_Verified").is_displayed()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_YAxis_Values").click()
        return yaxis

    def verify_color_dropdown(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_Color").click()
        color = self.driver.find_element_by_name("Load_3:Cell_Type").is_displayed()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_Color").click()
        return color

    '''TestCase T35978'''

    def add_graph_histogram(self):
        self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddNewGraph").click()

    def histogram_select_attribute(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_GraphType").click()
        self.driver.find_element_by_name("Histogram").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Chip").click()
        # driver.find_element_by_name("C:\Users\Fleek\Desktop\D50238").click()
        self.driver.find_element_by_name("D50238").click()
        verify = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Histogram").is_displayed()
        return verify

    def histogram_xaxis(self):
        xaxis = self.driver.find_element_by_accessibility_id(
            "AutomationId_GraphBuilder_Histogram_XAxis_Values").is_displayed()
        return xaxis

    def histogram_bin_value(self):
        bin = self.driver.find_element_by_accessibility_id(
            "AutomationId_GraphBuilder_Histogram_BinCounts").is_displayed()
        return bin

    def histogram_null_value_checkbox(self):
        null = self.driver.find_element_by_accessibility_id(
            "AutomationId_GraphBuilder_Histogram_ShowNullableValues").is_displayed()
        return null

    '''TestCase T35979'''

    def histogram_select_xaxis(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Histogram_XAxis_Values").click()
        self.driver.find_element_by_name("Load_3:Cell_Count_Verified").click()
        time.sleep(3)
        histogram = self.driver.find_element_by_accessibility_id(
            "AutomationId_GraphBuilder_Histogram_Chart").is_displayed()
        return histogram

    '''TestCase 35981'''

    def histogram_save(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Save").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_SaveGraph_Name").send_keys("graph1")
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_SaveGraph_Apply").click()
        save = self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_ContextMenu_ElementsTree_Element_Graph1").is_displayed()
        return save

    '''TestCase T35982'''

    def open_histogram(self):
        actionchains = ActionChains(self.driver)
        open = self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_ContextMenu_ElementsTree_Element_Graph1")
        actionchains.double_click(open).perform()

    def verify_axis(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Histogram_XAxis_Values").click()
        axis = self.driver.find_element_by_name("Load_3:Cell_Count_Verified").is_displayed()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Histogram_XAxis_Values").click()
        return axis

    def verify_bin(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Histogram_BinCounts").click()
        bin = self.driver.find_element_by_name("5").is_displayed()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Histogram_BinCounts").click()
        return bin

    def filter(self):
        self.driver.find_element_by_accessibility_id("abcd").click()
        # allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    def gallery(self):
        self.driver.find_element_by_name("demo").click()

    '''TestCase T35980'''

    def change_bin_quantity(self):
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Chip").click()
        self.driver.find_element_by_name("D50238").click()
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_Histogram_BinCounts").click()
        self.driver.find_element_by_name("6").click()
        bin = self.driver.find_element_by_name("0..0.7").is_displayed()
        return bin

    '''Timeline T35892'''

    def timeline_image_sequence_expander(self):
        actionchains = ActionChains(self.driver)
        chip = []
        chip = self.driver.find_elements_by_name("D50238")
        actionchains.move_to_element_with_offset(chip[1], 10, 10).click().perform()
        time.sleep(5)

    def timeline_image_sequence1(self):
        time.sleep(3)
        sequence1 = self.driver.find_element_by_accessibility_id(
            "AutomationId_TimeLine_TimeLineItem_Sequence_2019-01-28_15-36-49.731_SingleCells").is_displayed()
        return sequence1

    def timeline_image_sequence2(self):
        sequence2 = self.driver.find_element_by_accessibility_id(
            "AutomationId_TimeLine_TimeLineItem_Sequence_2019-01-28_12-38-21.092_PostCalibration").is_displayed()
        return sequence2

    def timeline_image_sequence3(self):
        sequence3 = self.driver.find_element_by_accessibility_id(
            "AutomationId_TimeLine_TimeLineItem_Sequence_2019-01-28_12-56-24.964_PostPenning").is_displayed()
        return sequence3

    def timeline_image_sequence4(self):
        sequence4 = self.driver.find_element_by_accessibility_id(
            "AutomationId_TimeLine_TimeLineItem_Sequence_2019-01-28_13-12-21.447_SingleCells").is_displayed()
        return sequence4

    '''Select Image Sequence'''

    def select_image_sequence(self):
        fitc = []
        self.driver.find_element_by_accessibility_id(
            "AutomationId_TimeLine_TimeLineItem_Sequence_2019-01-28_15-36-49.731_SingleCells").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_TimeLine_TimeLineItem_Sequence_2019-01-28_17-59-21.312_SingleCells").click()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_TimeLineItem_PE").click()
        fitc = self.driver.find_elements_by_accessibility_id("AutomationId_TimeLine_TimeLineItem_FITC")
        fitc[1].click()

    def timeline_edit_button1(self):
        edit = self.driver.find_elements_by_name("edit")
        edit[1].click()

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_Name").send_keys("Load_3")

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_CSVFile").click()

        self.driver.find_element_by_accessibility_id("VerticalSmallIncrease").click()

        time.sleep(2)
        csv = []
        csv = self.driver.find_elements_by_class_name("TextBlock")
        csv[8].click()
        # time.sleep(5)

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_AddCSV").click()
        self.driver.find_element_by_accessibility_id("VerticalLargeIncrease").click()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_Save").click()
        self.driver.find_element_by_accessibility_id("OKButton").click()
        # return len(csv)

    def timeline_edit_button2(self):
        edit = self.driver.find_elements_by_name("edit")
        edit[2].click()

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_Name").send_keys("Load_5")

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_CSVFile").click()

        csv = []
        csv = self.driver.find_elements_by_class_name("TextBlock")
        csv[7].click()
        time.sleep(2)

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_AddCSV").click()
        self.driver.find_element_by_accessibility_id("VerticalLargeIncrease").click()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_Save").click()
        self.driver.find_element_by_accessibility_id("OKButton").click()

    def timeline_edit_button3(self):
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ChipColumns_Item_Load_3").click()
        actionchains = ActionChains(self.driver)
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.ARROW_DOWN).perform()

        edit = self.driver.find_elements_by_name("edit")
        edit[3].click()

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_Name").send_keys("TPS_PE")

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_CSVFile").click()

        csv = []
        csv = self.driver.find_elements_by_class_name("TextBlock")
        csv[3].click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_CSVType").click()
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.RETURN).perform()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_AddCSV").click()
        self.driver.find_element_by_accessibility_id("VerticalLargeIncrease").click()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_FilterCriteriaValue").click()
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.ARROW_UP).perform()
        actionchains.send_keys(Keys.RETURN).perform()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_Save").click()
        self.driver.find_element_by_accessibility_id("OKButton").click()

    def timeline_edit_button4(self):
        actionchains = ActionChains(self.driver)
        edit = self.driver.find_elements_by_name("edit")
        edit[4].click()

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_Name").send_keys("TPS_FITC")

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_CSVFile").click()

        csv = []
        csv = self.driver.find_elements_by_class_name("TextBlock")
        csv[4].click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_CSVType").click()
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.RETURN).perform()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_AddCSV").click()
        self.driver.find_element_by_accessibility_id("VerticalLargeIncrease").click()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_FilterCriteriaValue").click()
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.ARROW_UP).perform()
        actionchains.send_keys(Keys.RETURN).perform()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_Save").click()
        # driver.find_element_by_accessibility_id("OKButton").click()

    '''Chip Timeline Delete Image Sequence'''

    def delete_image_sequence(self):
        '''driver.find_element_by_accessibility_id("AutomationId_TimeLine_ChipColumns_Item_TPS_PE").click()
        actionchains = ActionChains(driver)
        actionchains.send_keys(Keys.ARROW_UP).perform()
        actionchains.send_keys(Keys.ARROW_UP).perform()'''
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ImageSequence_Remove_Load_3").click()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ImageSequence_Remove_Load_5").click()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ImageSequence_Remove_TPS_PE").click()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ImageSequence_Remove_TPS_FITC").click()

    '''Remove raw data parameter'''

    def remove_new_parameter(self):
        self.driver.find_element_by_name("ChipId").click()
        actionchains = ActionChains(self.driver)
        for x in range(0, 10):
            actionchains.send_keys(Keys.ARROW_DOWN).perform()
        parameter = []
        parameter = self.driver.find_elements_by_accessibility_id("AutomationId_RawData_RemoveParameter")
        parameter[35].click()
        self.driver.find_element_by_accessibility_id("OKButton").click()
        return len(parameter)

    """testcase T42264"""

    def verify_version_number(self):
        versionnumber = self.driver.find_element_by_name("ASSAY ANALYZER 2.0").is_displayed()
        return versionnumber

    """testcase T42442"""

    def verify_shortinformation(self):
        self.driver.find_element_by_name("Help").click()
        self.driver.find_element_by_name("About").click()
        self.driver.find_element_by_name("Version 20191129.2").is_displayed()
        desc = self.driver.find_element_by_name(
            "Powerful software that is designed to work with gigabytes of data obtained from Optoﬂuidic platforms developed by Berkeley Lights. The main usage of the app is to help biologists easily find, check and export data to pdf files in minutes.").is_displayed()
        pr = self.driver.find_elements_by_accessibility_id("PART_Close")
        print(pr)
        pr[1].click()
        return desc

    """testcase T42195"""

    def verify_filterbuilder(self):
        self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddNewFilter").click()
        time.sleep(5)
        filterwind = self.driver.find_element_by_accessibility_id("HeaderElement").is_displayed()  # "Rad Pane Group"
        time.sleep(3)
        pr = self.driver.find_elements_by_accessibility_id("HeaderDropDownMenu")
        # print(pr)
        pr[1].click()
        self.driver.find_element_by_name("Hide").click()
        return filterwind

    """testcase T42196"""

    def verify_expander(self):
        self.driver.find_element_by_accessibility_id("Expander").click()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("Expander").click()
        time.sleep(2)
        chiptext = self.driver.find_element_by_name("D50238").is_displayed()
        return chiptext

    """testcase T42200"""

    def verify_removechip(self):
        global actionchains
        actionchains = ActionChains(self.driver)
        chip = self.driver.find_element_by_name("D50238")
        actionchains.context_click(chip).perform()
        time.sleep(3)
        self.driver.find_element_by_name("Remove chip(s)").click()
        self.driver.find_element_by_accessibility_id("OKButton").click()
        try:
            a = self.driver.find_element_by_name("D50238").is_displayed()
            return a
        except:
            b = False
            return b

    """testcase T42201"""

    def verify_saveworkbookbutton(self):
        self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Save").click()
        explorerwin = self.driver.find_element_by_name("Save As").is_displayed()
        time.sleep(2)
        actionchains = ActionChains(self.driver)
        # scrolldown = self.driver.find_elements_by_accessibility_id("DownButton")
        # print(scrolldown)
        # actionchains.double_click(scrolldown[2]).perform()
        try:
            data = self.driver.find_element_by_name("workbooktest.workbook")
            data1 = data.is_displayed()
        except:
            data1 = False

        if data1 == True:
            data.click()
            actionchains.send_keys(Keys.DELETE).perform()
            time.sleep(2)
        self.driver.find_element_by_accessibility_id("1001").send_keys("workbooktest")
        time.sleep(3)
        return explorerwin

    """testcase T42202"""

    def verify_usersaveworkbook(self):
        save = self.driver.find_element_by_accessibility_id("1").is_displayed()
        self.driver.find_element_by_accessibility_id("1").click()
        try:
            time.sleep(3)
            data = self.driver.find_element_by_name("Save As")
            data1 = data.is_displayed()
        except:
            data1 = False

        if data1 == True:
            self.driver.find_element_by_name("Yes").click()
        time.sleep(3)
        return save

    """testcase T42383"""

    def verify_changeworkbook(self):
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_NewWorkbook").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Custom").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("OKButton").click()

    def verify_reloadchips(self):
        global actionchains
        actionchains = ActionChains(self.driver)
        chip1 = self.driver.find_element_by_name("D50238")
        actionchains.context_click(chip1).perform()
        time.sleep(3)
        self.driver.find_element_by_name("Open in Raw Data").click()
        chip2 = self.driver.find_element_by_name("D50238")
        actionchains.context_click(chip2).perform()
        time.sleep(3)
        self.driver.find_element_by_name("Reload chip(s)").click()
        time.sleep(3)
        timeline = self.driver.find_element_by_accessibility_id("AutomationId_RawData")
        actionchains.context_click(timeline).perform()
        self.driver.find_element_by_name("Hide").click()

    """testcase 42203"""

    def verify_useropenworkbook(self):
        time.sleep(2)
        actionchains = ActionChains(self.driver)
        self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Open").click()
        self.driver.find_element_by_name("Desktop").click()
        time.sleep(2)
        chip = self.driver.find_element_by_name("D50238").click()
        actionchains.double_click(chip).perform()
        time.sleep(2)
        workbook = self.driver.find_element_by_name("workbooktest.workbook").is_displayed()
        self.driver.find_element_by_name("workbooktest.workbook").click()
        self.driver.find_element_by_accessibility_id("1").click()
        time.sleep(2)
        self.driver.find_element_by_name("Cancel").click()
        return workbook

    """testcase T42304"""

    def verify_graphbutton(self):
        self.driver.find_element_by_accessibility_id(
            "AutomationId_WorkbookExplorer_AdditionalButton_AddNewGraph").click()
        graphbutton = self.driver.find_element_by_name("Graph Builder").is_displayed()
        time.sleep(3)
        actionchains = ActionChains(self.driver)
        chip = self.driver.find_element_by_name("Graph Builder")
        actionchains.context_click(chip).perform()
        self.driver.find_element_by_name("Hide").click()
        return graphbutton

    """testcase T42453"""

    def verify_chipconfirmation(self):
        global actionchains
        actionchains = ActionChains(self.driver)
        chip = self.driver.find_element_by_name("D50238")
        actionchains.context_click(chip).perform()
        time.sleep(3)
        self.driver.find_element_by_name("Remove chip(s)").click()
        close = self.driver.find_elements_by_accessibility_id("PART_Close")
        close[1].click()
        chipvisible = self.driver.find_element_by_name("D50238").is_displayed()
        return chipvisible

    """testcase T42454"""

    def verify_draganddropui(self):
        global actionchains
        actionchains = ActionChains(self.driver)
        source = self.driver.find_element_by_name("D50238")
        destination = self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer")
        time.sleep(2)
        actionchains.drag_and_drop(source, destination).perform()
        time.sleep(3)
        checkui = source.is_displayed()
        return checkui

    """testcase 42305"""

    def verify_imagecubeselect(self):
        actionchains = ActionChains(self.driver)
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ImageSequence_Edit_TPS_FITC").click()
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_FilterCriteriaType").click()
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.RETURN).perform()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_Event_Save").click()

    """testcase T42390"""

    def verify_csvimagepath(self):

        self.driver.find_element_by_accessibility_id("AutomationId_TimeLine_ChipColumns_Item_TPS_PE").click()
        actionchains = ActionChains(self.driver)
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(4)
        verify = self.driver.find_element_by_name(
            "D50238_2019-01-29_14-34-13_2019-01-29_11-19-56.549_TNFa_FITC_0_TNFa_FITC.csv").is_displayed()
        return verify

    def verify_opensettings(self):
        time.sleep(1)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Settings").click()
        time.sleep(2)

    def verify_columncsv(self):
        self.driver.find_element_by_accessibility_id(
            "AutomationId_SettingsWindow_SettingsMenu_MenuElement_ColumnsByCSVType").click()
        time.sleep(3)
        self.driver.find_element_by_name("TargetBased").click()
        time.sleep(3)

        # time.sleep(2)
        # data = self.driver.find_element_by_name("Gate_Path")
        # for tar in data:
        #     if not tar.is_selected():
        #         tar.click()
        #
        # self.driver.find_element_by_accessibility_id(
        #     "AutomationId_SettingsWindow_ColumnsByCSVTypeView_ColumnsListBySelectedType_ColumnName_Gate_Path").click ()
        try:
            data = self.driver.find_element_by_accessibility_id(
                "AutomationId_SettingsWindow_ColumnsByCSVTypeView_ColumnsListBySelectedType_ColumnIsSelected_Target_Index")
            data1 = data.is_selected()
        except:
            data1 = True

        if data1 == False:
            self.driver.find_element_by_accessibility_id(
                "AutomationId_SettingsWindow_ColumnsByCSVTypeView_ColumnsListBySelectedType_ColumnName_Target_Index").click()

        try:
            data = self.driver.find_element_by_accessibility_id(
                "AutomationId_SettingsWindow_ColumnsByCSVTypeView_ColumnsListBySelectedType_ColumnIsSelected_Gate_Path")
            data1 = data.is_selected()
        except:
            data1 = True

        if data1 == False:
            self.driver.find_element_by_accessibility_id(
                "AutomationId_SettingsWindow_ColumnsByCSVTypeView_ColumnsListBySelectedType_ColumnName_Gate_Path").click()

        self.driver.find_element_by_accessibility_id("AutomationId_SettingsWindow_Apply").click()

    """testcase T42257"""

    def verify_uniquenessfortps(self):
        time.sleep(5)
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_AllHeadersVisible").click()
        chipidcheck = self.driver.find_elements_by_accessibility_id("AutomationId_RawData_HeaderVisibility")
        chipidcheck[0].click()
        time.sleep(3)
        penidcheck = self.driver.find_elements_by_accessibility_id("AutomationId_RawData_HeaderVisibility")
        penidcheck[1].click()
        self.driver.find_element_by_name("ChipId").click()

    def verify_findattr(self):
        global actionchains
        actionchains = ActionChains(self.driver)
        for x in range(0, 6):
            actionchains.send_keys(Keys.ARROW_DOWN).perform()

    def verify_selectatt(self):
        time.sleep(4)
        targetpathcheck = self.driver.find_elements_by_accessibility_id("AutomationId_RawData_HeaderVisibility")
        targetpathcheck[15].click()
        time.sleep(5)
        cubecheck = self.driver.find_elements_by_accessibility_id("AutomationId_RawData_HeaderVisibility")

        cubecheck[10].click()
        # gatepath = self.driver.find_elements_by_accessibility_id("AutomationId_RawData_HeaderVisibility")
        #
        # gatepath[12].click()

    def verify_rowdata(self):
        time.sleep(4)
        chipid = self.driver.find_element_by_accessibility_id("CellElement_0_0")
        chipidname = chipid.get_attribute("Name")

        penid = self.driver.find_element_by_accessibility_id("CellElement_0_1")
        penidname = penid.get_attribute("Name")

        time.sleep(5)
        targetindex = self.driver.find_element_by_accessibility_id("CellElement_0_15")
        targetindexname = targetindex.get_attribute("Name")

        cube = self.driver.find_element_by_accessibility_id("CellElement_0_17")
        cubename = cube.get_attribute("Name")

        # gatepath = self.driver.find_element_by_accessibility_id("CellElement_0_18")
        # gatepathname = gatepath.get_attribute("Name")

        # firstrowdata = chipidname + penidname + cubename + gatepathname

        firstrowdata = chipidname + penidname + targetindexname + cubename
        print(firstrowdata)

        time.sleep(5)
        chipid1 = self.driver.find_element_by_accessibility_id("CellElement_1_0")
        chipidname1 = chipid1.get_attribute("Name")

        penid1 = self.driver.find_element_by_accessibility_id("CellElement_1_1")
        penidname1 = penid1.get_attribute("Name")

        time.sleep(3)
        targetindex1 = self.driver.find_element_by_accessibility_id("CellElement_1_15")
        targetindexname1 = targetindex1.get_attribute("Name")

        cube1 = self.driver.find_element_by_accessibility_id("CellElement_1_17")
        cubename1 = cube1.get_attribute("Name")

        # gatepath1 = self.driver.find_element_by_accessibility_id("CellElement_1_18")
        # gatepathname1 = gatepath1.get_attribute("Name")

        # secondrowdata = chipidname1 + penidname1 + cubename1 + gatepathname1
        secondrowdata = chipidname1 + penidname1 + targetindexname1 + cubename1
        print(secondrowdata)

        if firstrowdata == secondrowdata:
            return False

        else:
            return True

    """testcase T42258"""

    def verify_removegrouping(self):
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_AllHeadersVisible").click()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_AllHeadersVisible").click()
        time.sleep(2)
        actionchains = ActionChains(self.driver)
        drag = self.driver.find_element_by_accessibility_id("ChipId")
        drop = self.driver.find_element_by_name("GridViewGroupPanel")
        actionchains.drag_and_drop(drag, drop).perform()
        time.sleep(3)
        drag = self.driver.find_element_by_accessibility_id("PART_CloseButton")
        closegrouping = self.driver.find_element_by_accessibility_id("PART_CloseButton")
        closegrouping.click()
        time.sleep(3)
        closevisible = drag.is_displayed()
        return closevisible

    """testcase T42265"""

    def verify_addcondinbottomarea(self):
        time.sleep(4)
        actionchains = ActionChains(self.driver)
        fieldsclick = self.driver.find_element_by_name("Fields")
        actionchains.double_click(fieldsclick).perform()
        time.sleep(2)
        firstattr = self.driver.find_element_by_name("[Load_3 : CellCountVerified]")
        actionchains.double_click(firstattr).perform()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("GreaterThan").click()

    def verify_getattrinbottomarea(self):
        actionchains = ActionChains(self.driver)
        for x in range(0, 4):
            actionchains.send_keys(Keys.ARROW_DOWN).perform()

    def verify_otherattrinbottomarea(self):
        actionchains = ActionChains(self.driver)
        time.sleep(3)
        secndattr = self.driver.find_element_by_name("[Load_5 : CellCountVerified]")
        actionchains.double_click(secndattr).perform()

    def verify_compatr(self):
        actionchains = ActionChains(self.driver)
        time.sleep(3)
        self.driver.find_element_by_name("TPS_PE : Target_Index").click()
        time.sleep(2)
        for x in range(0, 5):
            actionchains.send_keys(Keys.ARROW_UP).perform()
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_AllHeadersVisible").click()
        load3check = self.driver.find_elements_by_accessibility_id("AutomationId_RawData_HeaderVisibility")
        load3check[4].click()
        load5check = self.driver.find_elements_by_accessibility_id("AutomationId_RawData_HeaderVisibility")
        load5check[10].click()

    def verify_compareattr(self):
        time.sleep(4)
        load3 = self.driver.find_element_by_accessibility_id("Cell_0_4")
        load3name = load3.get_attribute("Value.Value")
        print(load3name)
        time.sleep(2)
        load5 = self.driver.find_element_by_accessibility_id("Cell_0_10")
        load5name = load5.get_attribute("Value.Value")
        print(load5name)

        if int(load3name) > int(load5name):
            return True
        else:
            return False

    def verify_compareattr1(self):
        time.sleep(4)
        load3 = self.driver.find_element_by_accessibility_id("CellElement_1_4")
        load3name = load3.get_attribute("Value.Value")

        load5 = self.driver.find_element_by_accessibility_id("CellElement_1_10")
        load5name = load5.get_attribute("Value.Value")

        if int(load3name) > int(load5name):
            return True
        else:
            return False

    def verify_header(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_AllHeadersVisible").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_AllHeadersVisible").click()

    def verify_compareattr2(self):
        time.sleep(4)
        load3 = self.driver.find_element_by_accessibility_id("CellElement_2_4")
        load3name = load3.get_attribute("Name")

        load5 = self.driver.find_element_by_accessibility_id("CellElement_2_10")
        load5name = load5.get_attribute("Name")

        if load3name > load5name:
            return True
        else:
            return False

    "testcase T42272"

    def verify_reorderinggridcolumns(self):
        global actionchains
        actionchains = ActionChains(self.driver)
        source = self.driver.find_element_by_accessibility_id("ChipId")
        destination = self.driver.find_element_by_accessibility_id("Load_3 : PenId")
        actionchains.drag_and_drop(source, destination).perform()
        time.sleep(5)
        checkreorder = self.driver.find_element_by_accessibility_id("CellElement_0_3")
        checkreordername = checkreorder.get_attribute("Name")
        return checkreordername

    """testcase T42282"""

    def verify_reorderinglistcolumns(self):
        global actionchains
        actionchains = ActionChains(self.driver)
        source = self.driver.find_elements_by_name("ChipId")
        destination = self.driver.find_elements_by_name("Load_3 : PenId")
        time.sleep(4)
        actionchains.drag_and_drop(source[0], destination[0]).perform()

        # checkreorder = self.driver.find_element_by_name("ChipId")
        # checkreordername = checkreorder.get_attribute("Name")
        # return checkreordername

    """testcase T42303"""

    def verify_addcustomparameter(self):
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_NewParameter").click()
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_ParameterEditor_Entries").click()
        time.sleep(3)

        actionchains = ActionChains(self.driver)
        actionchains.send_keys(Keys.ARROW_DOWN).perform()
        actionchains.send_keys(Keys.RETURN).perform()

        time.sleep(5)

        self.driver.find_element_by_accessibility_id(
            "AutomationId_RawData_ParameterEditor_ParameterInput").send_keys(
            "Customparameter")
        self.driver.find_element_by_name("Fields").click()
        time.sleep(4)
        element1 = self.driver.find_element_by_name("[Load_3 : CellCount]")
        actionchains = ActionChains(self.driver)
        actionchains.double_click(element1).perform()
        time.sleep(3)
        operator = self.driver.find_element_by_accessibility_id("GreaterThan")
        operator.click()

    def verify_otherattribute(self):
        actionchains = ActionChains(self.driver)
        for x in range(0, 3):
            actionchains.send_keys(Keys.ARROW_DOWN).perform()
        # actionchains.send_keys(Keys.ARROW_DOWN).perform()
        element2 = self.driver.find_element_by_name("[Load_5 : CellCountVerified]")
        actionchains.double_click(element2).perform()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_ParameterEditor_Apply").click()

    def verify_customparameter(self):
        time.sleep(8)
        appdata = os.getenv('APPDATA')
        # verifyfile = path.exists(appdata + "\Assay Analyzer 2.0\D50238\CustomParameters.dat")
        # return verifyfile

        verifydata = "{\"Name\":\"Load_5 : Customparameter\",\"Expression\":\" [Load_3 : CellCount]  >  [Load_5 : CellCountVerified] \"}]"
        verifyfile = path.exists(appdata + "\Assay Analyzer 2.0\D50238\CustomParameters.dat")
        if verifyfile == True:
            with open(appdata + "\Assay Analyzer 2.0\D50238\CustomParameters.dat", 'r') as file:
                if verifydata in file.read():
                    print("data verified")
                    return True
                else:
                    return False

    """testcase T42389"""

    def verify_viewpeningraph(self):
        actionchains = ActionChains(self.driver)
        time.sleep(3)
        righclick = self.driver.find_elements_by_name("1")
        righclick[0].click()
        keyboard.press_and_release('shift + down')
        # actionchains.send_keys(Keys.SHIFT).perform()
        time.sleep(3)
        element = self.driver.find_element_by_accessibility_id("Cell_1_3")
        actionchains.context_click(element).perform()
        time.sleep(2)
        self.driver.find_element_by_name("Graph").click()
        time.sleep(2)
        self.driver.find_element_by_name("Scatter Plot").click()
        time.sleep(6)
        verifyingraph = self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_GraphType")
        dropdown = verifyingraph.get_attribute("Value.Value")
        return dropdown

    def verify_graphxaxis(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_XAxis_Values").click()
        self.driver.find_element_by_name("Load_3:Pen_Id").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_GraphBuilder_ScatterPlot_YAxis_Values").click()
        self.driver.find_element_by_name("Load_3:Device_Id").click()

    def verify_chipaattr(self):
        verify = self.driver.find_element_by_name("D50238").is_displayed()
        return verify

    """testcase T42418"""

    def verify_sortcolumnheader(self):
        actionchains = ActionChains(self.driver)
        drag = self.driver.find_element_by_accessibility_id("Load_3 : CellCountVerified")
        drop = self.driver.find_element_by_name("GridViewGroupPanel")
        actionchains.drag_and_drop(drag, drop).perform()
        verify = self.driver.find_element_by_name("0").is_displayed()
        return verify

    def verify_headerdata(self):
        actionchains = ActionChains(self.driver)
        # headerdata = self.driver.find_elements_by_accessibility_id("ExpanderButton")
        # print(headerdata)
        headerdata = self.driver.find_element_by_accessibility_id("ExpanderButton")
        actionchains.move_to_element_with_offset(headerdata, 20, 1).perform()
        time.sleep(2)
        actionchains.click()

    def verify_cutcustomdata(self):
        self.driver.find_element_by_accessibility_id("AutomationId_RawData_RemoveParameter").click()

    """testcase T42421"""

    def verify_workbookforparameter(self):
        actionchains = ActionChains(self.driver)
        self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Save").click()
        try:
            data = self.driver.find_element_by_name("workbookcheck.workbook")
            data1 = data.is_displayed()
        except:
            data1 = False

        if data1 == True:
            data.click()
            actionchains.send_keys(Keys.DELETE).perform()
        self.driver.find_element_by_accessibility_id("1001").send_keys("workbookcheck")
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("1").click()

    def open_workbook_type(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_NewWorkbook").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Custom").click()
        time.sleep(3)
        try:
            data = self.driver.find_element_by_name("CONFIRMATION")
            data1 = data.is_displayed()
        except:
            data1 = False

        if data1 == True:
            self.driver.find_element_by_accessibility_id("OKButton").click()

    def verify_opensavedworkbook(self):
        actionchains = ActionChains(self.driver)
        self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Open").click()
        time.sleep(3)
        self.driver.find_element_by_name("Desktop (pinned)").click()
        click = self.driver.find_element_by_name("D50238")
        actionchains.double_click(click).perform()
        self.driver.find_element_by_name("workbookcheck.workbook").click()
        self.driver.find_element_by_accessibility_id("1").click()
        time.sleep(3)
        self.driver.find_element_by_name("Cancel").click()

    def verify_workbookparamincolumn(self):
        self.driver.find_element_by_name("ChipId").click()
        actionchains = ActionChains(self.driver)
        for x in range(0, 10):
            actionchains.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(2)
        parameter = self.driver.find_element_by_name("Load_5 : Customparameter").is_displayed()
        return parameter

    def verify_deleteworkbook(self):
        actionchains = ActionChains(self.driver)
        self.driver.find_element_by_accessibility_id("AutomationId_WorkbookExplorer_Save").click()
        try:
            data = self.driver.find_element_by_name("workbookcheck.workbook")
            data1 = data.is_displayed()
        except:
            data1 = False

        if data1 == True:
            data.click()
            actionchains.send_keys(Keys.DELETE).perform()

        self.driver.find_element_by_accessibility_id("2").click()

    def verify_Cancel(self):
        self.driver.find_element_by_name("Cancel").click()

    def verify_openworkbooktype1(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_NewWorkbook").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Custom").click()

    def verify_opensettings(self):
        time.sleep(1)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Settings").click()
        time.sleep(2)

    """42395"""

    def verify_savedcsvcol(self):

        target = self.driver.find_elements_by_accessibility_id(
            "AutomationId_SettingsWindow_SettingsMenu_MenuElement_ColumnsByCSVType")
        for i in range(0, 4):
            target[1].click()

        self.driver.find_element_by_name("TargetBased").click()
        verify = self.driver.find_elements_by_name("Target_Index")
        for tar in verify:
            if not tar.is_selected():
                tar.click()

        self.driver.find_element_by_accessibility_id(
            "AutomationId_SettingsWindow_ColumnsByCSVTypeView_ColumnsListBySelectedType_ColumnName_Target_Index").click()
        self.driver.find_element_by_name("Apply").click()

    def TPS_data(self):

        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_AddCondition").click()
        self.driver.find_element_by_name("Target").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_DimensionSelector").click()
        actionchain = ActionChains(self.driver)
        for a in range(0, 5):
            actionchain.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(2)
        self.driver.find_element_by_name("TPS_PE:Target_Index").click()
        time.sleep(2)
        increase = self.driver.find_elements_by_accessibility_id("increase")
        for a in range(0, 4):
            increase[1].click()
        target_text = self.driver.find_element_by_name("Targets: ").is_displayed()
        return target_text

    def totalShow(self):
        total_text = self.driver.find_element_by_name("Total: ").is_displayed()
        return total_text

    def compareIndex(self):
        target = self.driver.find_element_by_name("10")
        targetval = target.get_attribute("Name")
        print(targetval)
        total = self.driver.find_element_by_name("4")
        totalval = total.get_attribute("Name")
        print(totalval)

        if int(targetval) > int(totalval):
            return True
        else:
            return False

    """42436"""

    def filter2DShow(self):

        self.driver.find_element_by_name("").click()
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_FilterDimension").click()
        self.driver.find_element_by_name("2-D").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_AddCondition").click()
        self.driver.find_element_by_name("Target").click()
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_2DFilter_XAxis_Values").click()
        time.sleep(2)
        actionchain = ActionChains(self.driver)
        for a in range(0, 5):
            actionchain.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(2)
        self.driver.find_element_by_name("TPS_PE:Device_Id").click()
        self.driver.find_element_by_accessibility_id("AutomationId_FilterBuilder_2DFilter_YAxis_Values").click()
        for b in range(0, 2):
            actionchain.send_keys(Keys.ARROW_DOWN).perform()
        self.driver.find_element_by_name("TPS_PE:Target_Index").click()
        # can't be further automate because of selection polygon

    def checkHistoryFile(self):

        app = os.getenv('APPDATA')
        print(app)
        if os.path.isfile(app + "\Assay Analyzer 2.0\D50238\History.xml"):
            os.remove(app + "\Assay Analyzer 2.0\D50238\History.xml")
            print("file removed")
        else:
            print('file not removed')

    def confirmationPage(self):
        actionchains = ActionChains(self.driver)
        chip = self.driver.find_element_by_name("D50238")
        actionchains.context_click(chip).perform()
        self.driver.find_element_by_name("Open in Gallery").click()
        time.sleep(8)
        verify = self.driver.find_element_by_name("Confirmation").is_displayed()

        self.driver.find_element_by_name("Cancel").click()
        return verify

    def rawDatacheck(self):
        actionchains = ActionChains(self.driver)
        chip = self.driver.find_element_by_name("D50238")
        actionchains.context_click(chip).perform()
        self.driver.find_element_by_name("Open in Raw Data").click()
        time.sleep(8)
        verify = self.driver.find_element_by_name("Confirmation").is_displayed()

        self.driver.find_element_by_name("Cancel").click()
        return verify


    def open_workbook_close(self):
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("AutomationId_MainWindow_NavigationMenu_MenuElement_File").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_NewWorkbook").click()
        self.driver.find_element_by_accessibility_id(
            "AutomationId_MainWindow_NavigationMenu_MenuElement_Custom").click()
        time.sleep(2)
        self.driver.find_element_by_accessibility_id("CancelButton").click()


    def verify_delapplication(self):

        self.driver.find_element_by_accessibility_id("PART_Close").click()
        time.sleep(2)
        # verify = self.driver.find_element_by_name("Confirmation").is_displayed()
        self.driver.find_element_by_accessibility_id("DiscardButton").click()


    """----------------------------------------------------------------------------"""

    def deleteworkbook(self):
        desktop = str(os.path.join(Path.home(), "Desktop\D50238\workbooktest.workbook"))
        os.remove(desktop)

    """----------------------------------------------------------------------------"""
