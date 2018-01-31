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
import zipfile

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from driloader.commands import Commands

from .browsers import Browser
from .proxy import Proxy


class Downloader:

    """
    Contains methods to handle file downloading and some assertions.
    """

    def __init__(self, driver):
        self.os_name = platform.system()
        self.drivers_path = self._create_driver_folder()
        self.browser = Browser(driver, self.os_name)

    def _create_driver_folder(self):
        """
        Creates a folder to put the drivers and hides it.
        :return: the folder path.
        """
        drivers_path = os.path.expanduser('~{0}Driloader{0}Drivers{0}'.format(os.sep))
        if self.os_name == "Windows":
            if not os.path.exists(drivers_path):
                os.makedirs(drivers_path)
            import ctypes
            # This hides the folder in Windows.
            ctypes.windll.kernel32.SetFileAttributesW(drivers_path, 2)
            return drivers_path
        else:
            # This hides the folder in Linux
            hidden_name = drivers_path.replace("Drivers", ".Drivers")
            if not os.path.exists(hidden_name):
                os.makedirs(hidden_name)
            return hidden_name

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
    def unzip(zip_file, path_to_extract, delete_after_extract=False):
        """
        Extract a 'zip' or 'gz' file content to the same path as file is in.
        :param zip_file: file to be extracted.
        :param delete_after_extract: deletes original zipped file after it's extracted.
        :param path_to_extract: the path to extract the file.
        """
        if zip_file.endswith("zip"):
            zfile = zipfile.ZipFile(zip_file, "r")
            zfile.extractall(path_to_extract)
            zfile.close()
        if zip_file.endswith("gz"):
            Commands.run("tar -zxvf {} -C {}".format(zip_file, zip_file.rpartition("/")[0]))
        if delete_after_extract:
            os.remove(zip_file)

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
