import os
import configparser
from abc import ABC, abstractmethod


class BaseBrowser(ABC):

    def __init__(self, browser_name):
        self.parser = configparser.ConfigParser()
        self.parser.read(os.path.join(os.path.dirname(__file__), 'browsers.ini'))
        self.section = self.parser[browser_name.upper()]
        self.search_pattern_regex = self.parser.get('GENERAL', 'search_pattern')
        self.base_url = self.parser.get(browser_name, 'base_url')
        self.zipped_file = self._get_zipped_file_name()
        self.unzipped_file = self._get_unzipped_file_name()

    def _get_zipped_file_name(self):
        if os.name == 'nt':
            return self.section['zip_file_win']
        else:
            return self.section['zip_file_linux']

    def _get_unzipped_file_name(self):
        if os.name == 'nt':
            return self.section['unzipped_win']
        else:
            return self.section['unzipped_linux']

    @abstractmethod
    def get_latest_driver(self):
        raise NotImplementedError

    @abstractmethod
    def get_driver_matching_installed_version(self):
        raise NotImplementedError

    @abstractmethod
    def get_installed_version(self):
        raise NotImplementedError
