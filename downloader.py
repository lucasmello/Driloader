import json
import platform
import os
from configparser import ConfigParser

import requests

from browser_detection import BrowserDetection


class Downloader:

    def __init__(self):
        self.OS = platform.system()
        self._create_driver_folder()
        self.parser = ConfigParser()
        self.parser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'drivers_info.ini'))

    def _create_driver_folder(self):
        self.drivers_path = os.path.expanduser('~{0}Driloader{0}Drivers{0}'.format(os.sep))
        if self.OS == "Windows":
            if not os.path.exists(self.drivers_path):
                os.makedirs(self.drivers_path)
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(self.drivers_path, 2)  # This hides the folder in Windows.
        else:
            hidden_name = self.drivers_path.replace("Drivers", ".Drivers")  # This hides the folder in Linux
            if not os.path.exists(hidden_name):
                os.makedirs(hidden_name)
            self.drivers_path = hidden_name

    def download_chrome_driver(self, path_to_download="default", version="autodetect"):
        section = "CHROMEDRIVER"
        if version == "autodetect":
            browser = BrowserDetection()
            chrome_version = browser.get_chrome_version()
        config = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'version_matcher.json')))
        chrome_json = config.get("CHROME")
        driver_version = ""
        for attr, value in chrome_json.items():
            r = range(int(value.get("from")), int(value.get("to")))
            if chrome_version in r:
                driver_version = attr
                break
        chrome_file = self._get_file(section)
        download_url = "{}{}".format(self.parser.get(section, "base_url").replace("{version}", str(driver_version)),
                                      chrome_file)
        self._download_file(download_url)
        pass

    def _download_file(self, url):
        response = requests.get(url, verify=False)
        pass

    def _get_file(self, section):
        """
        Get the zipped file, based in user os and drivers_info.ini.
        :param section: drivers_info.ini section.
        :return: zipped file's name.
        """
        if section == "IEDRIVER":
            return self.parser.get_value(section.upper(), "zip_file_win")
        return self.parser.get(section.upper(), "zip_file_win") if self.OS == "Windows" \
            else self.parser.get(section.upper(), "zip_file_linux")

    def _get_path(self, section):
        """
        Get the full unzipped file's path.
        :param section: drivers_info.ini section.
        :return: unzipped file's path.
        """
        if self.OS == "Windows" or section == "IEDRIVER":
            return "%s%s" % (self.drivers_path, self.parser.get_value(section, "unzipped_win"))
        else:
            return "%s%s" % (self.drivers_path, self.parser.get_value(section, "unzipped_linux"))
