from allure_commons._allure import title

from assay import assay
import csvwrite
import allure
import pytest
import allure_pytest

global test_case_ids

test_case_ids = [815, 819, 821, 747, 748, 749, 752, 753, 754, 761, 801, 802, 805, 781, 782, 783, 784, 767, 772, 875,
                 876, 877, 881, 126358, 126365, 126366, 126370, 126371, 126379, 126387, 768, 775,
                 126367, 787, 126398, 126399, 762, 806, 810, 770, 910, 777, 126338, 785]

global execution_time
execution_time = []

global update_testrail
update_testrail = False

"""test case 815"""
test = ""


@allure.title('this is the test title')
def test_Start_222466(driver):
    global lp
    lp = assaycld(driver)
    global test
    test = str(test_case_ids[0])
    lp.time_start()
    if update_testrail == True:
        print("got it")
        lp.createTestRun(test_case_ids)

    # verify = lp.start_tejas()
    # assert verify == True, "tejas not started"


def stop():
    # print("stop")
    time = lp.time_stop()
    execution_time.append(time)


def Time():
    print("time")
    time = 0
    execution_time.append(time)


def case_fields():
    print("case field")
    lp.case_fields(test)


def fail_update():
    print("fail update")
    lp.updateTestCase(test, "fail")


def pass_update():
    pass
    lp.updateTestCase(test, "pass")


def teardwn():
    if update_testrail == True:
        # print("teardown")
        lp.closeTestRun()
    csvwrite.write_csv(execution_time)


"""test case C222468"""


def test_maximize_222468():
    global test
    test = str(test_case_ids[1])
    lp.maximize()
    lp.time_start()


"""testcase 222469"""


def test_logoverify_222469():
    global test
    test = str(test_case_ids[2])
    lp.time_start()
    response = lp.logo_verify()
    assert response == True, "logo not found"
#
#
# """testcase C222470"""
#
#
# def test_versionnumber_222470():
#     global test
#     test = str(test_case_ids[3])
#     verify = lp.verify_version_number()
#     assert verify == True, "version number not found"

#
# """testcase T222471"""
#
#
# def test_verifyshortinfo():
#     global test
#     test = str(test_case_ids[4])
#     verify = lp.verify_shortinformation()
#     assert verify == True, "content not found"
#
#
# """testcase C222475"""
#
#
# def test_verifyfilterwind_222475():
#     global test
#     test = str(test_case_ids[5])
#     verify = lp.verify_filterbuilder()
#     assert verify == True, "filter builder window not found"
#
# """Testcase 31260"""
#
# def test_notify_newversion_31260():
#     # global test
#     # test = str(test_case_ids[5])
#     lp.clickupdate()
#     verify= lp.verify_version_notify()
#     assert verify==True,"version update not notified"
#
#
#
# """Testcase 31266"""
#
# def test_notify_latestnewversion_31266():
#     # global test
#     # test = str(test_case_ids[5])
#     lp.time_start()
#     lp.clickupdate()
#     verify= lp.verify_latestversion_check()
#     assert verify==True,"latest version update not notified"
#     lp.closenotify()
#
# "below testcase failed in this build"
# """Testcase 31895"""
#
# def test_installatest_version_31895():
#     # global test
#     # test = str(test_case_ids[5])
#     lp.time_start()
#     lp.clickupdate()
#     verify= lp.install_latestversion()
#     assert verify==True,"save confimation not display"
#     # lp.closenotify()
#
# def test_installconfirmation():
#     lp.time_start()
#     lp.verify_CLDopen()
#     lp.clickupdate()
#     # lp.verify_installconfirmation() # need much time to install latest update
#     lp.closenotify()
#
#
#
#
# """testcase T35914"""
#
#
# def test_verifydataimporttemplateselements():
#     # global test
#     # test = "126379"
#     lp.verify_data_import_templates_element()
#     cld = lp.verify_data_import_templates_element_cld()
#     assert cld == True, "cld not found"
#     add = lp.verify_data_import_templates_element_add()
#     assert add == True, "add button not found"
#     edit = lp.verify_data_import_templates_element_edit()
#     assert edit == True, "edit button not found"
#     copy = lp.verify_data_import_templates_element_copy()
#     assert copy == True, "copy button not found"
#     remove = lp.verify_data_import_templates_element_remove()
#     assert remove == True, "Remove button not found"
#     imp = lp.verify_data_import_templates_element_import()
#     assert imp == True, "import button not found"
#     export = lp.verify_data_import_templates_element_export()
#     assert export == True, "export button not found"
#
#
# """testcase T35915"""
#
#
# def test_verifyworkbooktypeelement():
#     # global test
#     # test = "126387"
#     lp.time_start()
#     lp.verify_workbook_type_element()
#     custom = lp.verify_workbook_type_element_custom()
#     assert custom == True, "custom not found"
#     add = lp.verify_workbook_type_element_add()
#     assert add == True, "add button not found"
#     edit = lp.verify_workbook_type_element_edit()
#     assert edit == True, "edit button not found"
#     copy = lp.verify_workbook_type_element_copy()
#     assert copy == True, "copy button not found"
#     remove = lp.verify_workbook_type_element_remove()
#     assert remove == True, "remove button not found"
#
#
# """testcase T35885"""
#
#
# def test_workbookexplorer():
#     # global test
#     # test = "747"
#     lp.time_start()
#     save = lp.workbook_explorer_save()
#     assert save == True, "save button not found"
#     openworkbook = lp.workbook_explorer_openworkbook()
#     assert openworkbook == True, "open workbook button not found"
#     addchip = lp.workbook_explorer_addchip()
#     assert addchip == True, "add chip button not found"
#     addfilter = lp.workbook_explorer_addfilter()
#     assert addfilter == True, "add filter button not found"
#     addgraph = lp.workbook_explorer_addgraph()
#     assert addgraph == True, "add graph button not found"
#

"""Testcase T36382"""


def test_openworkbooktype():
    # global test
    # test = "126395"
    lp.time_start()
    verify = lp.open_workbook_type()
    assert verify == True, "CLD workbook not open"


"""testcase T35886"""


def test_addchip():
    # global test
    # test = "748"
    lp.time_start()
    chip = lp.add_chip()
    assert chip == True, "chip not found"

#
# """testcase C222476"""
#
#
# def test_verifyexpander_222476():
#     global test
#     test = str(test_case_ids[6])
#     lp.time_start()
#     verify = lp.verify_expander()
#     assert verify == True, "expander not working"
#
#
# """testcase T35887"""
#
#
# def test_verifyoptionchip():
#     # global test
#     # test = "749"
#     lp.time_start()
#     lp.verify_option_chip()
#     timeline = lp.verify_timeline()
#     assert timeline == True, "view in timeline not found"
#     gallery = lp.verify_gallery()
#     assert gallery == True, "view in gallery not found"
#     rawdata = lp.verify_rawdata()
#     assert rawdata == True, "view in rawdata not found"
#     remove = lp.verify_remove()
#     assert remove == True, "remove not found"
#     reload = lp.verify_reload()
#     assert reload == True, "reload not found"
#     folder = lp.verify_containing_folder()
#     assert folder == True, "containing folder not found"
#
#
# """testcase C222480"""
#
#
# def test_verifyremovechip():
#     global test
#     test = str(test_case_ids[7])
#     lp.time_start()
#     verify = lp.verify_removechip()
#     assert verify == False, "chip not removed"
#
#
# """testcase C222481"""
#
#
# def test_verifysavebutton_222481():
#     global test
#     test = str(test_case_ids[8])
#     lp.time_start()
#     chip = lp.add_chip()
#     assert chip == True, "chip not found"
#     verify = lp.verify_saveworkbookbutton()
#     assert verify == True, "explorer pane not found"
#
#
# """testcase 222482"""
#
#
# def test_usersaveworkbook_222482():
#     global test
#     test = str(test_case_ids[9])
#     lp.time_start()
#     lp.verify_usersaveworkbook()
#     # assert verify == True, "workbook not saved"
#
#
# """testcase C222483"""
#
# #
# def test_openworkbook_222483():
#     global test
#     test = str(test_case_ids[10])
#     lp.time_start()
#     lp.verify_changeworkbook()
#     lp.add_chip()
#     verify = lp.verify_useropenworkbook()
#     assert verify == True, "workbook not found"
#
#
# """testcase T42384"""
#
# """containinffolder"""
#
#
# """testcase 222485"""
#
#
# def test_graphscreen_222485():
#     global test
#     test = str(test_case_ids[11])
#     lp.time_start()
#     # lp.verify_changeworkbook()
#     verify = lp.verify_graphbutton()
#     assert verify == True, "graph window not found"
#
#
# """testcase C222486"""
#
#
# def test_verify_reloadchip_222486():
#     global test
#     test = str(test_case_ids[12])
#     lp.time_start()
#     lp.add_chip()
#     lp.verify_reloadchips()
#
#
# """testcase C222488"""
#
#
# def test_verifychippopup_222488():
#     global test
#     test = str(test_case_ids[13])
#     lp.time_start()
#     verify = lp.verify_chipconfirmation()
#     assert verify == True, "chip has been removed"
#
#
# """testcase C222489"""
#
#
# def test_verify_draganddropui_222489():
#     global test
#     test = str(test_case_ids[14])
#     lp.time_start()
#     verify = lp.verify_draganddropui()
#     assert verify == True, "ui has been changed"


"""testcase T35888"""

def test_opentimeline():
    global test
    test = "752"
    lp.time_start()
    verify = lp.open_timeline()
    assert verify == "Chip Timeline"
    # not completed


"""testcase T35892"""


def test_chiptimelineimagesequence():
    global test
    test = "762"
    lp.time_start()
    lp.timeline_image_sequence_expander()
    sequence1 = lp.timeline_image_sequence1()
    assert sequence1 == True, "image sequence not found"
    sequence2 = lp.timeline_image_sequence2()
    assert sequence2 == True, "image sequence not found"
    sequence3 = lp.timeline_image_sequence3()
    assert sequence3 == True, "image sequence not found"
    sequence4 = lp.timeline_image_sequence4()
    assert sequence4 == True, "image sequence not found"


def test_selectimagesequence():
    lp.time_start()
    lp.select_image_sequence()
    edit = lp.timeline_edit_button1()
    print(edit)
    lp.timeline_edit_button2()
    lp.timeline_edit_button3()
    lp.timeline_edit_button4()


# """testcase T42305"""
#
#
# def test_verify_imagecubeselect():
#     global test
#     test = "42305"
#     lp.time_start()
#     lp.verify_imagecubeselect()
#
#
# """testcase  T42390"""
#
#
# def test_verify_csvimagepath():
#     global test
#     test = "42390"
#     lp.time_start()
#     verify = lp.verify_csvimagepath()
#     assert verify == True, "full csv path not found"
#     lp.close_timeline()
#
#
# """testcase T42383"""
#
#
# def test_verify_reloadchip():
#     global test
#     test = "42383"
#     lp.time_start()
#     # lp.add_chip()
#     lp.verify_reloadchips()

#
# """testcase 754"""
#
#
# def test_rawdata():
#     global test
#     test = "754"
#     lp.time_start()
#     verify = lp.open_raw_data()
#     assert verify == "Raw Data"
#
# """testcase T42257"""
#
#
# def test_verify_uniquenessfortps():
#     global test
#     test = "42257"
#     lp.time_start()
#     lp.verify_opensettings()
#     lp.verify_columncsv()
#     lp.verify_uniquenessfortps()
#     lp.verify_findattr()
#     lp.verify_selectatt()
#     verify = lp.verify_rowdata()
#     assert verify == True, "data is not unique"
#
#
# """testcase T42258"""
#
# def test_verify_removegrouping():
#     global test
#     test = "42258"
#     # lp.verify_removegrouping()
#     verify = lp.verify_removegrouping()
#     assert verify == False, "grouping not removed"
#
#
# """testcase T42265"""
#
# def test_verify_addcondinbottomarea():
#     global test
#     test = "42265"
#     lp.verify_addcondinbottomarea()
#     lp.verify_getattrinbottomarea()
#     lp.verify_otherattrinbottomarea()
#     lp.verify_compatr()
#     # lp.verify_compareattr()
#
#     verify = lp.verify_compareattr()
#     assert verify == True, "condition1 failed"
#     # verify1 = lp.verify_compareattr1()
#     # assert verify1 == True, "condition2 failed"
#     # verify3 = lp.verify_compareattr2()
#     # assert verify3 == True, "condition3 failed"
#     lp.verify_header()
#
#
# """testcase T42272"""
#
#
# def test_verify_reorderingcolumns():
#     global test
#     test = "42272"
#     verify = lp.verify_reorderinggridcolumns()
#     assert verify == "D50238", "reordering column failed"
#
#
# """testcase T42282"""
#
#
# def test_verify_reorderinglistcolumns():
#     global test
#     test = "42282"
#     lp.time_start()
#     lp.verify_reorderinglistcolumns()
#
#
# """testcase T42303"""
#
#
# def test_verify_customparameter():
#     global test
#     test = "42303"
#     lp.time_start()
#     lp.verify_addcustomparameter()
#     lp.verify_otherattribute()
#     verify = lp.verify_customparameter()
#     assert verify == True, "data verified"
#     verify = lp.verify_workbookparamincolumn()
#     assert verify == True, "parameter not found"
#
#
# """testcase T42389"""
#
# def test_verify_viewpeningraph():
#     global test
#     test = "42389"
#     lp.time_start()
#     verify = lp.verify_viewpeningraph()
#     assert verify == "Scatter Plot", "scatter plot not found in graph"
#     lp.verify_graphxaxis()
#     verify = lp.verify_chipaattr()
#     assert verify == True, "chip not displayed"
#
#
# """testcase T42418"""
#
# def test_verify_sortcolumnheader():
#     global test
#     test = "T42418"
#     lp.time_start()
#     lp.close_graph()
#     # lp.open_raw_data()
#   check= lp.verify_sortcolumnheader()
#     assert check==True, "0 value not show"
#     lp.verify_headerdata()
#     lp.verify_cutcustomdata()
#
#
# """testcase  T42421"""
#
# def test_verify_workbookforparameter():
#     global test
#     test = "42421"
#     lp.time_start()
#     lp.verify_workbookforparameter()
#     lp.close_raw_data()
#     lp.open_workbook_type()
#     lp.add_chip()
#     # lp.verify_Cancel()
#     lp.verify_opensavedworkbook()
#     lp.verify_openworkbooktype1()
#     lp.add_chip()
#     lp.verify_deleteworkbook()
#     #lp.open_workbook_type()
#     #lp.add_chip()
#     lp.open_raw_data()
#
#
# """testcase 42395"""
#
# def test_TPS_Target():
#     global test
#     test = "42395"
#     lp.time_start()
#     lp.open_workbook_close()
#     lp.add_chip()
#     lp.verify_opensettings()
#     lp.verify_savedcsvcol()
#     lp.click_filter()
#     lp.add_chip_in_filter()
#     lp.filter_name('Filter1')
#     response = lp.TPS_data()
#     assert response == True, "target value not displayed"
#     verify = lp.totalShow()
#     assert verify == True, "Total value not displayed"
#     Greater = lp.compareIndex()
#     assert Greater == True, "Total value displayed"
#
# def test_2Dfilter():
#     global test
#     test = "42436"
#     lp.time_start()
#     lp.filter2DShow()

# def test_close_desktopapp():
#     lp.time_start()
#     lp.verify_delapplication
