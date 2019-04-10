# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=no-member
# pylint: disable=import-error

"""
driloader.downloader
--------------------

Module which performs the driver download.
"""


import os
import platform

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from driloader.utils.file import FileHandler
from .factories.browser_factory import BrowserFactory
from .proxy import Proxy


class Downloader:

    """
    Contains methods to handle file downloading and some assertions.
    """

    def __init__(self, browser_name):
        self.os_name = platform.system()
        self.drivers_path = self._create_driver_folder()
        self.browser_factory = BrowserFactory(browser_name)

    @staticmethod
    def _create_driver_folder():
        """
        Creates a folder to put the drivers and hides it.
        :return: the folder path.
        """
        drivers_path = os.path.expanduser('~{0}Driloader{0}Drivers{0}'.format(os.sep))
        return FileHandler.create_folders(drivers_path, hidden=True)

    @staticmethod
    def download_file(url, path_to_download):
        """
        Downloads a file.
        :param url: download URL of the file.
        :param path_to_download: the path to download the file.
        """
        if not os.path.exists(path_to_download):
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(url, verify=False, proxies=Proxy().urls)
            path = path_to_download.rpartition(os.sep)[0]
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path_to_download, "wb") as file:
                file.write(response.content)

    @staticmethod
    def check_driver_exists(path_to_file):
        """
        Checks if the driver exists.
        :param path_to_file: the file to be checked.
        :return: True if file exists, otherwise False.
        """
        return os.path.isfile(path_to_file)

    def get_default_path(self):
        """
        Get the full unzipped file's path.
        :return: unzipped file's path.
        """
        return self.drivers_path
