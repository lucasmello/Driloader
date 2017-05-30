import json
import platform
import os
import zipfile

import requests
from configparser import ConfigParser
from browser_detection import BrowserDetection


class Downloader:

    def __init__(self):
        self.OS = platform.system()
        self.drivers_path = self._create_driver_folder()
        self.parser = ConfigParser()
        self.parser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'drivers_info.ini'))

    def _create_driver_folder(self):
        drivers_path = os.path.expanduser('~{0}Driloader{0}Drivers{0}'.format(os.sep))
        if self.OS == "Windows":
            if not os.path.exists(drivers_path):
                os.makedirs(drivers_path)
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(drivers_path, 2)  # This hides the folder in Windows.
            return drivers_path
        else:
            hidden_name = drivers_path.replace("Drivers", ".Drivers")  # This hides the folder in Linux
            if not os.path.exists(hidden_name):
                os.makedirs(hidden_name)
            return hidden_name

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
        if path_to_download == "default":
            self.drivers_path += driver_version
            if not os.path.exists(self.drivers_path):
                os.makedirs(self.drivers_path)
            full_path = self.drivers_path + os.sep + chrome_file
        else:
            full_path = path_to_download + os.sep + chrome_file
        self._download_file(download_url, full_path)
        self._unzip(full_path, self.drivers_path + driver_version, True)
        return self._get_path("CHROMEDRIVER")

    @staticmethod
    def _download_file(url, path_to_download):
        if not os.path.exists(path_to_download):
            response = requests.get(url, verify=False)
            with open(path_to_download, "wb") as f:
                f.write(response.content)

    @staticmethod
    def _unzip(zip_file, path_to_extract, delete_after_extract=False):
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
            os.subprocess.Popen("tar -zxvf %s -C %s" % (zip_file, zip_file.rpartition("/")[0]), shell=True).wait()
        if delete_after_extract:
            os.remove(zip_file)

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
            return "%s%s%s" % (self.drivers_path, os.sep, self.parser.get(section, "unzipped_win"))
        else:
            return "%s%s%s" % (self.drivers_path, os.sep, self.parser.get(section, "unzipped_linux"))
