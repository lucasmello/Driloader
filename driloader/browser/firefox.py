# pylint: disable=import-outside-toplevel
"""

Module that abstract operations to handle Chrome versions.

"""

import os
import re

import requests

from driloader.http.proxy import Proxy
from driloader.utils.commands import Commands
from .basebrowser import BaseBrowser
from .drivers import Driver
from .exceptions import BrowserDetectionError
from ..http.operations import HttpOperations
from ..utils.file import FileHandler


class Firefox(BaseBrowser):
    """
    Implements all BaseBrowser methods to find the proper Firefox version.
    """

    def __init__(self, driver: Driver):
        super().__init__('FIREFOX')
        self.driver = driver
        self.driver.version = self._latest_driver()

    def _latest_driver(self):
        """
       Gets the latest gecko driver version.
       :return: the latest gecko driver version.
       """
        resp = requests.get(self._config.latest_release_url(),
                            proxies=Proxy().urls)
        reg = re.search(r'\d{1,2}[\d.]+', resp.url.rpartition('/')[2])
        return reg.group(0)

    def _driver_matching_installed_version(self):
        # TODO: get the right Firefox version
        return self._latest_driver()

    def installed_browser_version(self):
        """ Returns Firefox version.
        Args:
            self
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting
            browser version.
        """

        try:
            if os.name == 'nt':
                ff_path = self._find_firefox_exe_in_registry()
                output = Commands.run([ff_path, '-v', '|', 'more'])
            else:
                output = Commands.get_command_output('firefox -v')

            if output is not None:
                out_reg = re.search(self._config.search_regex_pattern(),
                                    str(output))
                str_version = out_reg.group(0)
                int_version = int(str_version.partition(".")[0])
                return int_version
            return None
        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve Firefox version '
                                        'from system', error) from error

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

    def get_driver(self):
        return self._download_and_unzip(HttpOperations(), self.driver,
                                        FileHandler(), replace_version=True)
