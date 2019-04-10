"""
Module that abstract all common operations to find right browser versions.
"""

import os
import configparser
from abc import ABC, abstractmethod


class BaseBrowser(ABC):

    """
    Provides all common methods to detect best matches.
    """

    def __init__(self, browser_name):
        self.parser = configparser.ConfigParser()
        self.parser.read(os.path.join(os.path.dirname(__file__), 'browsers.ini'))
        self.section = self.parser[browser_name.upper()]
        self.search_pattern_regex = self.parser.get('GENERAL', 'search_pattern')
        self.base_url = self.parser.get(browser_name, 'base_url')
        self.zipped_file = self._get_zipped_file_name()
        self.unzipped_file = self._get_unzipped_file_name()

    def _get_zipped_file_name(self):
        """
        Reads the zipped file's name from browsers.ini.
        :return: zipped file name.
        """
        if os.name == 'nt':
            return self.section['zip_file_win']
        return self.section['zip_file_linux']

    def _get_unzipped_file_name(self):
        """
        Reads the unzipped file's name from browsers.ini.
        :return: unzipped file name.
        """
        if os.name == 'nt':
            return self.section['unzipped_win']
        return self.section['unzipped_linux']

    @abstractmethod
    def latest_driver(self):
        """"
        Returns the latest available driver.
        """
        raise NotImplementedError

    @abstractmethod
    def driver_matching_installed_version(self):
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
