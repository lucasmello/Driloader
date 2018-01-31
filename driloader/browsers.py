# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=too-many-instance-attributes

"""
driloader.browsers
---------------------------

Module to abstract browser information.
"""


import json
import os
import re
import xml.etree.ElementTree as ET
from configparser import ConfigParser, NoSectionError

import requests

from .browser_detection import BrowserDetection
from .proxy import Proxy

GECKODRIVER = 'GECKODRIVER'
CHROMEDRIVER = 'CHROMEDRIVER'
IEDRIVER = 'IEDRIVER'
PATTERN_SEARCH = r'\d{1,2}[\,\.]{1}\d{1,2}'

GECKO_LATEST_VERSION_URL = 'https://github.com/mozilla/geckodriver/releases/' \
                           'latest'

CHROME_VERSIONS_URL = 'https://chromedriver.storage.googleapis.com/' \
                      '{version}/notes.txt'

CHROME_SUPPORTED_VERSIONS = r'----------ChromeDriver v((?:\d+\.?)+)'\
                            r' \((?:\d+-?)+\)----------\n' \
                            r'Supports Chrome v((?:\d+-?)+)'


class Browser:
    """Abstracts the browser information based on OS and driver."""
    def __init__(self, driver, os_name):
        self.driver = driver
        self.base_url = get_config(self.driver, 'base_url')
        self.version_installed = self.get_installed_version()
        self.version_matcher_path = self.get_chrome_version_matcher_path()
        self.version_latest = self.get_latest()
        self.version_supported = self.get_supported()

        if os_name == 'Windows':
            self.file_name = get_config(self.driver, 'unzipped_win')
            self.file_name_zip = get_config(self.driver, 'zip_file_win')
        else:
            self.file_name = get_config(self.driver, 'unzipped_linux')
            self.file_name_zip = get_config(self.driver, 'zip_file_linux')

    @staticmethod
    def get_chrome_version_matcher_path():
        """
        Gets or creates the version_matcher file to put the chrome driver versions.
        :return: the full file's path.
        """
        json_path = os.path.expanduser('~{0}Driloader{0}Configs{0}'.format(os.sep))
        if not os.path.exists(json_path):
            os.makedirs(json_path)
        return os.path.join(json_path, 'version_matcher.json')

    def get_latest(self):
        """
        Gets the latest version of the driver.
        :return: the latest version of the driver.
        """
        if self.driver == GECKODRIVER:
            return self.get_latest_gecko_driver()
        if self.driver == CHROMEDRIVER:
            return self.get_latest_chrome_driver()
        if self.driver == IEDRIVER:
            return self.get_latest_ie_driver()
        else:
            raise ValueError("Driver value must be {} or {} or {}".format(
                GECKODRIVER, CHROMEDRIVER, IEDRIVER
            ))

    def get_supported(self):
        """
        Gets the supported version of the driver.
        :return: the supported version.
        """
        if self.driver == GECKODRIVER:
            return self.version_latest
        if self.driver == CHROMEDRIVER:
            return self.get_supported_chrome_driver()
        if self.driver == IEDRIVER:
            return self.version_latest
        else:
            raise ValueError("Driver value must be {} or {} or {}".format(
                GECKODRIVER, CHROMEDRIVER, IEDRIVER
            ))

    def get_installed_version(self):
        """
        Gets the installed version.
        :return: the installed version.
        """
        browser = BrowserDetection()
        if self.driver == GECKODRIVER:
            return browser.get_firefox_version()
        if self.driver == CHROMEDRIVER:
            return browser.get_chrome_version()
        if self.driver == IEDRIVER:
            return browser.get_internet_explorer_version()
        else:
            raise ValueError("Driver value must be {} or {} or {}".format(
                GECKODRIVER, CHROMEDRIVER, IEDRIVER
            ))

# IE DRIVER SECTION
    @staticmethod
    def get_latest_ie_driver():
        """
        Gets the latest ie driver version.
        :return: the latest ie driver version.
        """
        resp = requests.get('http://selenium-release.storage.googleapis.com/',
                            proxies=Proxy().urls)
        xml_dl = ET.fromstring(resp.text)
        root = ET.ElementTree(xml_dl)
        tag = root.getroot().tag
        tag = tag.rpartition('}')[0] + tag.rpartition('}')[1]
        contents = root.findall(tag + 'Contents')
        last_version = 0
        for content in contents:
            version_str = content.find(tag + 'Key').text[:4]
            version_nbr = re.search(PATTERN_SEARCH, version_str)
            if version_nbr is not None:
                version_str = version_nbr.group(0)
            try:
                version = float(version_str) if version_str is not None else 0
            except ValueError:
                version = 0
            if version > last_version:
                last_version = version
        return last_version

# CHROME DRIVER SECTION
    @staticmethod
    def get_latest_chrome_driver():
        """
        Gets the latest chrome driver version.
        :return: the latest chrome driver version.
        """
        resp = requests.get('https://chromedriver.storage.googleapis.com/'
                            'LATEST_RELEASE', proxies=Proxy().urls)
        reg = re.search(PATTERN_SEARCH, resp.text)
        return float(reg.group(0))

    def get_supported_chrome_driver(self):
        """
        Gets the right version to the installed version.
        :return: the right version to work with installed browser.
        """
        if os.path.exists(self.version_matcher_path):
            os.remove(self.version_matcher_path)
        self._mount_chrome_json()

        config = json.load(open(self.version_matcher_path))
        chrome_json = config.get('CHROME')
        for attr, value in chrome_json.items():
            version_range = range(int(value.get('from')), int(value.get('to')) + 1)
            if self.version_installed in version_range:
                return attr
        return None

# GECKO DRIVER SECTION
    @staticmethod
    def get_latest_gecko_driver():
        """
        Gets the latest gecko driver version.
        :return: the latest gecko driver version.
        """
        resp = requests.get(GECKO_LATEST_VERSION_URL, proxies=Proxy().urls)
        reg = re.search(r'\d{1,2}[\d.]+', resp.url.rpartition('/')[2])
        return reg.group(0)

    def _mount_chrome_json(self):
        """
        Creates the file that matches the version with installed chrome.
        """
        with open(self.version_matcher_path, 'w+') as conf:

            chrome_json = {}
            json_file = {'CHROME': {}}

            notes_url = CHROME_VERSIONS_URL \
                .replace('{version}', str(self.version_latest))

            resp = requests.get(notes_url, proxies=Proxy().urls)
            result = re.findall(CHROME_SUPPORTED_VERSIONS, resp.text)

            for obj in result:
                _from = obj[1].rpartition('-')[0]
                _to = obj[1].rpartition('-')[2]
                chrome_json[obj[0]] = {'from': _from, 'to': _to}
                json_file['CHROME'] = chrome_json
            json.dump(json_file, conf)
            conf.close()


def get_config(section, option):
    """
    Get the config from drivers_info.ini file.
    :param section: the file's section.
    :param option: the option to get the value from.
    :return: the option's value.
    """
    config = ConfigParser()
    path = os.path.dirname(__file__)
    file = 'drivers_info.ini'
    file_path = os.path.join(path, file)
    config.read(file_path)
    try:
        return config.get(section, option)
    except NoSectionError:
        return None


def get_section(section):
    """
    Gets the entire section of drivers_info.ini file.
    :param section: the file's section.
    :return: the entire section.
    """
    config = ConfigParser()
    path = os.path.dirname(__file__)
    file = 'drivers_info.ini'
    file_path = os.path.join(path, file)
    config.read(file_path)

    try:
        return config[section]
    except KeyError:
        return None
