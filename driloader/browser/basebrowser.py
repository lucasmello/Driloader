"""
Module that abstract all common operations to find right browser versions.
"""

from abc import ABC, abstractmethod

from driloader.browser.drivers import Driver
from driloader.config.paths import Paths
from driloader.http.operations import HttpOperations
from driloader.http.proxy import Proxy
from driloader.config.browser_config import BrowserConfig
from driloader.utils.file import FileHandler


class BaseBrowser(ABC):

    """
    Provides all common methods to detect best matches.
    """

    def __init__(self, browser_name):
        self._config = BrowserConfig(browser_name)

    @abstractmethod
    def _latest_driver(self):
        """"
        Returns the latest available driver.
        """
        raise NotImplementedError

    @abstractmethod
    def _driver_matching_installed_version(self):
        """
        Best matching between browser version and driver.
        """
        raise NotImplementedError

    @abstractmethod
    def installed_browser_version(self):
        """
        Detects the browser version.
        """
        raise NotImplementedError

    def get_driver(self):
        """
        API to download and unzip the driver.
        """
        raise NotImplementedError

    def _download_and_unzip(self, http: HttpOperations, driver: Driver,
                            file: FileHandler, replace_version=False):
        """
        Downloads and unzip the driver.
        """
        paths = Paths(driver.create_folder(), self, driver)
        unzipped_file_path = paths.unzipped_file_path()
        if replace_version:
            zipped_file_path = paths.zipped_file_path(
                replace_version=driver.version)
            download_url = paths.download_url(
                replace_version=driver.version)
        else:
            zipped_file_path = paths.zipped_file_path(
                replace_version=driver.version)
            download_url = paths.download_url()
        if not driver.exists(unzipped_file_path):
            response = http.get(download_url, verify=False,
                                proxies=Proxy().urls)
            file.write_content(zipped_file_path, response.content)
            FileHandler.unzip(zipped_file_path, unzipped_file_path,
                              delete_after_extract=True)
        if not paths.unzipped_file_path().endswith('.exe'):
            driver.make_executable(unzipped_file_path)
        return unzipped_file_path

    @property
    def config(self):
        """
        Return the config parser.
        """
        return self._config
