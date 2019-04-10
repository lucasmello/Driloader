import os
import re
import requests

from driloader.browser.exceptions import BrowserDetectionError
from driloader.proxy import Proxy
from .basebrowser import BaseBrowser
from ..commands import Commands


class Chrome(BaseBrowser):

    __instance = None
    __chrome_version_regex = r'----------ChromeDriver v((?:\d+\.?)+)'\
                             r' \((?:\d+-?)+\)----------\n' \
                             r'Supports Chrome v((?:\d+-?)+)'

    def __init__(self):
        super().__init__('CHROME')
        self._versions_url = self.section['versions_url']
        self._latest_release_url = self.section['latest_release_url']
        self.version_installed = self.get_installed_version()
        self.version_dict = self._mount_chrome_dict()

    def __new__(cls, *args, **kwargs):
        if Chrome.__instance is None:
            Chrome.__instance = object.__new__(cls)
        return Chrome.__instance

    def _mount_chrome_dict(self):
        """
        Creates the file that matches the version with installed chrome.
        """

        versions_url = self._versions_url.replace('{version}', str(self.get_latest_driver()))

        chrome_json = {}

        resp = requests.get(versions_url, proxies=Proxy().urls)
        result = re.findall(Chrome.__chrome_version_regex, resp.text)

        for obj in result:
            _from = obj[1].rpartition('-')[0]
            _to = obj[1].rpartition('-')[2]
            chrome_json[obj[0]] = {'from': _from, 'to': _to}
        return chrome_json

    def get_latest_driver(self):
        """
        Gets the latest chrome driver version.
        :return: the latest chrome driver version.
        """
        resp = requests.get(self._latest_release_url, proxies=Proxy().urls)
        reg = re.search(re.compile(self.search_pattern_regex), resp.text)
        return str(reg.group(0))

    def get_driver_matching_installed_version(self):
        """
        Gets the right version to the installed version.
        :return: the right version to work with installed browser.        """

        for attr, value in self.version_dict.items():
            version_range = range(int(value.get('from')), int(value.get('to')) + 1)
            if self.version_installed in version_range:
                return attr
        return None

    def get_installed_version(self):
        """ Returns Google Chrome version.
        Args:
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting browser version.
        """

        try:
            if os.name == "nt":
                # Here we assume the user installed Chrome in default directory
                # TODO: Make sure we find a Chrome installed in system and not rely on default dir
                app = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
                cmd = ['wmic', 'datafile', 'where',
                       'name="{}"'.format(app), 'get', 'Version', '/value']

                result = Commands.run(cmd)
                res_reg = re.search(self.search_pattern_regex, str(result))
                str_version = res_reg.group(0)

            else:
                str_version = Commands.run("google-chrome --product-version")

        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve Chrome version from system', error)

        int_version = int(str_version.partition('.')[0])
        return int_version
