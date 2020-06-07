from pathlib import Path

from appium import webdriver
import subprocess
import os
import sys
import pytest
import time

import os.path
from selenium.webdriver import ActionChains
from testrail import *
from allure_commons.types import AttachmentType

# desktop = str(os.path.join(Path.home(), "DESKTOP\D0238"))
#app = os.getenv(desktop)
# print(desktop)

path = "~D50238 / History.xml"
home_dir = os.path.expanduser(path)
print(home_dir)
#my_module_file = os.path.join(home_dir,"DESKTOP\D0238")



