import platform
import os
import zipfile
import requests
import subprocess
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .browsers import Browser


class Downloader:

    def __init__(self, driver):
        self.os_name = platform.system()
        self.drivers_path = self._create_driver_folder()
        self.browser = Browser(driver, self.os_name)

    def _create_driver_folder(self):
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
    def _download_file(url, path_to_download):
        if not os.path.exists(path_to_download):
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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
            subprocess.Popen("tar -zxvf %s -C %s" % (zip_file, zip_file.rpartition("/")[0]), shell=True).wait()
        if delete_after_extract:
            os.remove(zip_file)

    @staticmethod
    def _check_driver_exists(path_to_file):
        return os.path.isfile(path_to_file)

    def _get_path(self, section):
        """
        Get the full unzipped file's path.
        :param section: drivers_info.ini section.
        :return: unzipped file's path.
        """
        return "%s%s%s" % (self.drivers_path, os.sep, self.browser.file_name)
