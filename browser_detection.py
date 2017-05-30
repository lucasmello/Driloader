import re
import subprocess
import sys


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

    def get_firefox_version(self):
        ff_path = self._find_firefox_exe_in_registry()
        if self.OS == "linux":
            output = subprocess.getoutput("firefox -v")
        elif self.OS == "win32":
            output = subprocess.getoutput('"{}" -v | more'.format(ff_path))
        if output is not None:
            out_reg = re.search(self.pattern, output)
            return out_reg.group(0)


    def _find_firefox_exe_in_registry(self):
        try:
            from _winreg import OpenKey, QueryValue, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER
        except ImportError:
            from winreg import OpenKey, QueryValue, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER
        import shlex
        keys = (r"SOFTWARE\Classes\FirefoxHTML\shell\open\command",
                r"SOFTWARE\Classes\Applications\firefox.exe\shell\open\command")
        command = ""
        for path in keys:
            try:
                key = OpenKey(HKEY_LOCAL_MACHINE, path)
                command = QueryValue(key, "")
                break
            except OSError:
                try:
                    key = OpenKey(HKEY_CURRENT_USER, path)
                    command = QueryValue(key, "")
                    break
                except OSError:
                    pass
        else:
            return ""

        if not command:
            return ""

        return shlex.split(command)[0]