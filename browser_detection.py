import re
import subprocess
import sys
import os


class BrowserDetection:

    def __init__(self):
        self.OS = sys.platform
        self.pattern = "\d{1,2}[\,\.]{1}\d{1,2}"

    def get_chrome_version(self):
        if self.OS == "linux":
            return subprocess.getoutput("google-chrome --product-version")
        if self.OS == "win32":
            cmd = 'wmic datafile where name="C:\\\Program Files (x86)\\\Google\\\Chrome\\\Application\\\chrome.exe" get Version'
            result = subprocess.getoutput(cmd)
            res_reg = re.search(self.pattern, result)
            return res_reg.group(0)
            # wmic datafile where name="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" get Version /value