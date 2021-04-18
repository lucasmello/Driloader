"""
Responsible to return the browser configs.
"""
import configparser
import os

from driloader.config.config_base import BrowserConfigBase


class BrowserConfig(BrowserConfigBase):
    """
    Parses the 'browsers.ini' file and return it's values.
    """

    def __init__(self, browser: str):
        self._browser_name = browser
        self._parser = configparser.ConfigParser()
        self._parser.read(os.path.join(os.path.dirname(__file__),
                                       'browsers.ini'))
        self._section = self._parser[browser.upper()]
        self._search_pattern_regex = self._parser.get('GENERAL',
                                                      'search_pattern')

    def base_url(self):
        """
        Return base_url.
        """
        return self._section['base_url']

    def zipped_file_name(self, replace_version=''):
        """
        Return zipped_file_name.
        @param replace_version: if in browsers.ini there's a '{version}'
        due to dynamic versions with geckodriver.
        """
        if os.name == 'nt':
            file = self._section['zip_file_win']
        else:
            file = self._section['zip_file_linux']
        if replace_version:
            file = file.replace('{version}', replace_version)
        return file

    def unzipped_file_name(self):
        """
        Return unzipped_file_name.
        """
        if os.name == 'nt':
            return self._section['unzipped_win']
        return self._section['unzipped_linux']

    def latest_release_url(self):
        """
        Return latest_release_url.
        """
        return self._section['latest_release_url']

    def index_url(self):
        """
        Return index_url.
        """
        return self._section['index_url']

    def versions_url(self):
        """
        Return versions_url.
        """
        return self._section['versions_url']

    def search_regex_pattern(self):
        """
        Return search_pattern from GENERAL section.
        """
        return self._parser['GENERAL']['search_pattern']
