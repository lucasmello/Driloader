"""
Responsible to resolve all URI paths.
"""
import os

from driloader.browser.drivers import Driver


class Paths:
    """
    Responsible to resolve all URI paths.
    """

    def __init__(self, root_path: str, base_browser, driver: Driver):
        self.path = os.path.join(root_path, driver.browser,
                                 driver.version)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.base_browser = base_browser
        self.driver = driver

    def unzipped_file_path(self):
        """
        Return the path the driver must be unzipped in.
        """
        return self.path

    def zipped_file_path(self, replace_version=''):
        """
        Return the path the driver must be saved in.
        @param replace_version: if in browsers.ini there's a '{version}'
        due to dynamic versions with geckodriver.
        """
        if replace_version:
            return os.path.join(self.path,
                                self.base_browser.config.zipped_file_name(
                                    replace_version=replace_version))
        return os.path.join(self.path,
                            self.base_browser.config.zipped_file_name())

    def download_url(self, replace_version=''):
        """
        Return a resolved url to download the driver.
        @param replace_version: if in browsers.ini there's a '{version}'
        due to dynamic versions with geckodriver.
        """
        return '{}{}'.format(self.base_browser.config.base_url().
                             replace('{version}', self.driver.version),
                             self.base_browser.config.zipped_file_name(
                                 replace_version=replace_version))
