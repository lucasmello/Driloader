"""

Module that abstract operations to handle Chrome versions.

"""

import os
import re

import requests

from driloader.browser.exceptions import \
    BrowserDetectionError, BrowserNotSupportedError
from driloader.http.proxy import Proxy
from driloader.utils.commands import Commands, CommandError
from .basebrowser import BaseBrowser
from .drivers import Driver
from ..http.operations import HttpOperations
from ..utils.file import FileHandler


class Chrome(BaseBrowser):

    """
    Implements all BaseBrowser methods to find the proper Chrome version.
    """

    _installed_version = None
    __default_path_win = r'C:\\Program Files (x86)\\Google\\Chrome' \
                         r'\\Application\\chrome.exe'
    __chrome_launch_unix = 'google-chrome'
    __chrome_launch_fallback_unix = 'google-chrome-stable'
    __browser_name = 'chrome'
    __chrome_version_regex = r'----------ChromeDriver v((?:\d+\.?)+)'\
                             r' \((?:\d+-?)+\)----------\n' \
                             r'Supports Chrome v((?:\d+-?)+)'

    def __init__(self, driver: Driver):
        super().__init__('CHROME')
        self._driver = driver
        self._install_path = None

    def binary(self, value):
        """
        Sets the path. If not set, it will try the default.
        """
        self._install_path = value
        return self

    def _mount_chrome_dict(self):
        """
        Creates the file that matches the version with installed chrome.
        """
        installed_version = self.installed_browser_version()
        if installed_version >= 70:
            return None
        if installed_version >= 43:
            versions_url = self._config.versions_url().replace('{version}',
                                                               '2.46')
        elif installed_version >= 29:
            versions_url = self._config.versions_url().replace('{version}',
                                                               '2.9')
        else:
            raise BrowserNotSupportedError('Sorry, but we don\'t support'
                                           'Chrome versions below 29.',
                                           'Browser not supported')

        chrome_json = {}

        resp = requests.get(versions_url, proxies=Proxy().urls)
        result = re.findall(Chrome.__chrome_version_regex, resp.text)

        for obj in result:
            _from = obj[1].rpartition('-')[0]
            _to = obj[1].rpartition('-')[2]
            chrome_json[obj[0]] = {'from': _from, 'to': _to}
        return chrome_json

    def _latest_driver(self):
        """
        Gets the latest chrome driver version.
        :return: the latest chrome driver version.
        """
        resp = requests.get(self._config.latest_release_url(),
                            proxies=Proxy().urls)
        reg = re.search(re.compile(self._config.search_regex_pattern()),
                        resp.text)
        return str(reg.group(0))

    def _driver_matching_installed_version(self):
        """
        Gets the right version to the installed version.
        :return: the right version to work with installed browser.
        """

        if not self._mount_chrome_dict():
            return self._get_latest_driver_version_from_chrome_version(
                self.installed_browser_version())

        for attr, value in self._mount_chrome_dict().items():
            version_range = range(int(value.get('from')),
                                  int(value.get('to')) + 1)
            if self.installed_browser_version() in version_range:
                return attr
        return None

    def _get_latest_driver_version_from_chrome_version(self, installed_version):
        """
        Some browser versions may have more than one available. This method
        assures it will get always the last driver version.
        """
        http = HttpOperations()
        index_page = http.get_html(self._config.index_url())
        index_page.html.render(sleep=3)
        tr_elements = index_page.html.find('body > table tr')
        version_matched_list = []
        for line in tr_elements:
            try:
                current_version = line.find('td a')[0].text
                if current_version.split('.')[0] == str(installed_version):
                    version_matched_list.append(current_version)
            except IndexError:
                pass
        if version_matched_list:
            return version_matched_list[-1]
        return None

    def installed_browser_version(self):
        """ Returns Google Chrome version.
        Args:
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting
            browser version.
        """
        if self._installed_version is None:
            try:
                if os.name == "nt":
                    # Here we assume the user installed Chrome
                    # in default directory
                    if not self._install_path:
                        app = self.__default_path_win
                    else:
                        app = self._install_path
                    cmd = ['wmic', 'datafile', 'where',
                           'name="{}"'.format(app), 'get', 'Version', '/value']

                    result = Commands.run(cmd)
                    res_reg = re.search(self._config.search_regex_pattern(),
                                        str(result))
                    str_version = res_reg.group(0)
                else:
                    if self._install_path:
                        str_version = Commands.run('{} --product-version'.
                                                   format(self._install_path))
                    else:
                        try:
                            str_version = Commands.run(
                                '{} --product-version'.format(
                                    self.__chrome_launch_unix))
                        except CommandError:
                            str_version = Commands.run(
                                '{} --product-version'.format(
                                    self.__chrome_launch_fallback_unix))

            except Exception as error:
                raise BrowserDetectionError('Unable to retrieve Chrome '
                                            'version from system', error) from error

            int_version = int(str_version.partition('.')[0])
            self._installed_version = int_version
            return int_version
        return self._installed_version

    def get_driver(self):
        """
        API to expose to client to download the driver and unzip it.
        """
        self._driver.version = self._driver_matching_installed_version()
        return self._download_and_unzip(HttpOperations(),
                                        self._driver, FileHandler())
