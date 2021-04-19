# pylint: disable=anomalous-backslash-in-string, too-many-locals,
# pylint: disable=multiple-statements

"""

Module that abstract operations to handle Internet Explorer versions.

"""

import os
import platform
import re
import xml.etree.ElementTree as ET

import requests

from driloader.browser.exceptions import BrowserDetectionError
from driloader.http.proxy import Proxy
from driloader.utils.commands import Commands
from .basebrowser import BaseBrowser
from .drivers import Driver
from ..http.operations import HttpOperations
from ..utils.file import FileHandler


class IE(BaseBrowser):
    """
    Implements all BaseBrowser methods to find the proper
    Internet Explorer version.
    """

    _find_version_32_regex = r'IEDriverServer_Win32_([\d]+\.[\d]+\.[\d])'
    _find_version_64_regex = r'IEDriverServer_x64_([\d]+\.[\d]+\.[\d])'

    def __init__(self, driver: Driver):
        super().__init__('IE')
        self.x64 = IE._is_windows_x64()
        self._driver = driver

    def _latest_driver(self):
        """
        Gets the latest ie driver version.
        :return: the latest ie driver version.
        """
        resp = requests.get(self._config.latest_release_url(),
                            proxies=Proxy().urls)
        xml_dl = ET.fromstring(resp.text)
        root = ET.ElementTree(xml_dl)
        tag = root.getroot().tag
        tag = tag.rpartition('}')[0] + tag.rpartition('}')[1]
        contents = root.findall(tag + 'Contents')
        last_version = 0
        version_str = '0.0.0'
        last_version_str = '0.0.0'
        if self.x64:
            pattern = IE._find_version_64_regex
        else:
            pattern = IE._find_version_32_regex
        os_type = 'x64' if self.x64 else 'Win32'
        for content in contents:
            key = content.find(tag + 'Key').text
            driver_section = 'IEDriverServer_{}_'.format(os_type) in key
            if driver_section:
                version_nbr = re.search(pattern, key)
                if version_nbr is not None:
                    version_str = version_nbr.group(1)
                try:
                    if version_str is not None:
                        version = float(version_str.rpartition('.')[0])
                    else:
                        version = 0
                except ValueError:
                    version = 0
                if version >= last_version:
                    last_version = version
                    last_version_str = version_str
        return last_version_str

    def _driver_matching_installed_version(self):
        # TODO: Version matcher for IE.
        return self._latest_driver()

    def installed_browser_version(self):
        """ Returns Internet Explorer version.
        Args:
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when
            getting browser version.
        """

        if os.name != "nt":
            raise BrowserDetectionError('Unable to retrieve IE version.',
                                        'System is not Windows.')

        cmd = ['reg', 'query',
               'HKEY_LOCAL_MACHINE\Software\Microsoft\Internet Explorer',
               '/v', 'svcVersion']

        try:
            output = Commands.run(cmd)
            reg = re.search(self._config.search_regex_pattern(), str(output))
            str_version = reg.group(0)
            int_version = int(str_version.partition(".")[0])
        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve IE version '
                                        'from system.', error) from error

        return int_version

    @staticmethod
    def _is_windows_x64():
        return platform.machine().endswith('64')

    def get_driver(self):
        """
                API to expose to client to download the driver and unzip it.
                """
        self._driver.version = self._driver_matching_installed_version()
        return self._download_and_unzip(HttpOperations(),
                                        self._driver, FileHandler())
