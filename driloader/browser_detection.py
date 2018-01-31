# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=anomalous-backslash-in-string

"""
driloader.browser_detection
---------------------------

Module with functions to detect the browser version.
"""


import platform
import re
import subprocess

from .commands import Commands


class BrowserDetectionError(Exception):
    """ BrowserDetectionError """
    def __init__(self, message, cause):
        """Init method
        Sets superclass arguments up.
        Sets the cause of exception up.
        """
        super(BrowserDetectionError, self).__init__(message)
        self.cause = cause

    def __str__(self):
        return 'Error: {}.\nCause: {}'.format(self.args[0], self.cause)


class BrowserDetection:
    """ Provides methods to retrieve the browser's version """

    def __init__(self):
        """ Sets up the system information """

        self.os_name = platform.system()
        self.pattern = r"\d{1,2}[\,\.]{1}\d{1,2}"

    def get_internet_explorer_version(self):
        """ Returns Internet Explorer version.
        Args:
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting browser version.
        """

        if self.os_name != "Windows":
            raise BrowserDetectionError('Unable to retrieve IE version.', 'System is not Windows.')

        cmd = ['reg', 'query',
               'HKEY_LOCAL_MACHINE\Software\Microsoft\Internet Explorer', '/v', 'svcVersion']

        try:
            output = Commands.run(cmd)
            reg = re.search(self.pattern, str(output))
            str_version = reg.group(0)
            int_version = int(str_version.partition(".")[0])
        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve IE version from system.', error)

        return int_version

    def get_chrome_version(self):
        """ Returns Google Chrome version.
        Args:
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting browser version.
        """

        try:
            if self.os_name == "Linux":
                str_version = Commands.run("google-chrome --product-version")

            if self.os_name == "Windows":
                app = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
                cmd = ['wmic', 'datafile', 'where',
                       'name="{}"'.format(app), 'get', 'Version', '/value']

                result = Commands.run(cmd)
                res_reg = re.search(self.pattern, str(result))
                str_version = res_reg.group(0)

        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve Chrome version from system', error)

        int_version = int(str_version.partition('.')[0])
        return int_version

    def get_firefox_version(self):
        """ Returns Firefox version.
        Args:
            self
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting browser version.
        """

        try:

            if self.os_name == "Linux":
                output = subprocess.getoutput("firefox -v")
            elif self.os_name == "Windows":
                ff_path = self._find_firefox_exe_in_registry()
                output = Commands.run([ff_path, '-v', '|', 'more'])

            if output is not None:
                out_reg = re.search(self.pattern, str(output))
                str_version = out_reg.group(0)
                int_version = int(str_version.partition(".")[0])
                return int_version
            return None
        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve Firefox version from system', error)

    @staticmethod
    def _find_firefox_exe_in_registry():
        """ Finds firefox.exe file in Windows systems.
        Args:
        Returns:
            Returns an string with firefox.exe path.
        Raises:
            None
        """

        try:
            from _winreg import OpenKey, QueryValue, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER
        except ImportError:
            from winreg import OpenKey, QueryValue, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER

        import shlex

        keys = (r"SOFTWARE\Classes\FirefoxHTML\shell\open\command",
                r"SOFTWARE\Classes\Applications\firefox.exe\shell\open\command")

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
