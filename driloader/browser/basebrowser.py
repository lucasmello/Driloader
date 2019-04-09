import os
import configparser
from abc import ABC, abstractmethod


class BaseBrowser(ABC):

    def __init__(self, browser_name):
        self.parser = configparser.ConfigParser()
        self.parser.read(os.path.join(os.path.dirname(__file__), 'browsers.ini'))
        self.section = self.parser[browser_name.upper()]
        self.pattern_search_regex = self.parser.get('GENERAL', 'PATTERN_SEARCH')

    @abstractmethod
    def get_latest_driver(self):
        raise NotImplementedError

    @abstractmethod
    def get_driver_matching_installed_version(self):
        raise NotImplementedError

    @abstractmethod
    def get_installed_version(self):
        raise NotImplementedError
