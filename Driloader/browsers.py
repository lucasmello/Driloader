from configparser import ConfigParser
import os
import json
import requests
import xml.etree.ElementTree as ET
import re

from .browser_detection import BrowserDetection

GECKODRIVER = "GECKODRIVER"
CHROMEDRIVER = "CHROMEDRIVER"
IEDRIVER = "IEDRIVER"
PATTERN_SEARCH = "\d{1,2}[\,\.]{1}\d{1,2}"

GECKO_LATEST_VERSION_URL = "https://github.com/mozilla/geckodriver/releases/" \
                           "latest"

CHROME_VERSIONS_URL = "https://chromedriver.storage.googleapis.com/" \
                      "{version}/notes.txt"

CHROME_SUPORTEDS_VERSIONS = "----------ChromeDriver v((?:\d+\.?)+)"\
                            " \((?:\d+-?)+\)----------\n" \
                            "Supports Chrome v((?:\d+-?)+)"


class Browser:
    def __init__(self, driver, os_name):
        self.driver = driver
        self.base_url = getConfig(self.driver, 'base_url')
        self.version_instaled = self.get_isntaled_version()

        self.version_latest = self.get_latest()
        self.version_suported = self.get_suported()

        if os_name == 'Windows':
            self.file_name = getConfig(self.driver, 'unzipped_win')
            self.file_name_zip = getConfig(self.driver, 'zip_file_win')
        else:
            self.file_name = getConfig(self.driver, 'unzipped_linux')
            self.file_name_zip = getConfig(self.driver, 'zip_file_linux')

    def get_latest(self):
        if self.driver == GECKODRIVER:
            return self.get_latest_gecko_driver_version()
        if self.driver == CHROMEDRIVER:
            return self.get_latest_chrome_driver_version()
        if self.driver == IEDRIVER:
            return self.get_latest_ie_driver_version()

    def get_suported(self):
        if self.driver == GECKODRIVER:
            return self.version_latest
        if self.driver == CHROMEDRIVER:
            return self.get_suported_chrome_driver_version()
        if self.driver == IEDRIVER:
            return self.version_latest

    def get_isntaled_version(self):
        browser = BrowserDetection()
        if self.driver == GECKODRIVER:
            return browser.get_firefox_version()
        if self.driver == CHROMEDRIVER:
            return browser.get_chrome_version()
        if self.driver == IEDRIVER:
            return browser.get_internet_explorer_version()

# IE DRIVER SECTION
    def get_latest_ie_driver_version(self):
        resp = requests.get("http://selenium-release.storage.googleapis.com/")

        xml_dl = ET.fromstring(resp.text)
        root = ET.ElementTree(xml_dl)
        tag = root._root.tag
        tag = tag.rpartition("}")[0] + tag.rpartition("}")[1]
        contents = root.findall(tag + "Contents")
        last_version = 0
        for content in contents:
            version_str = content.find(tag + "Key").text[:4]
            version_nbr = re.search(PATTERN_SEARCH, version_str)
            if version_nbr is not None:
                version_str = version_nbr.group(0)
            try:
                version = float(version_str) if version_str is not None else 0
            except Exception:
                version = 0
            if version > last_version:
                last_version = version
        return last_version

# CHROME DRIVER SECTION
    def get_latest_chrome_driver_version(self):
        resp = requests.get("https://chromedriver.storage.googleapis.com/"
                            "LATEST_RELEASE")

        reg = re.search(PATTERN_SEARCH, resp.text)
        return float(reg.group(0))

    def get_suported_chrome_driver_version(self):
        chrome_json_versions_path = os.path.join(os.path.abspath
                                                 (os.path.dirname(__file__)),
                                                 'version_matcher.json')

        if os.path.isfile(chrome_json_versions_path) is not True:
            self._mount_chrome_json()

        config = json.load(open(chrome_json_versions_path))
        chrome_json = config.get("CHROME")

        if str(self.version_latest) not in chrome_json.keys():
            self._mount_chrome_json()
            config = json.load(open(chrome_json_versions_path))
            chrome_json = config.get("CHROME")

        for attr, value in chrome_json.items():
            r = range(int(value.get("from")), int(value.get("to")) + 1)
            if self.version_instaled in r:
                return attr

# GECKO DRIVER SECTION
    def get_latest_gecko_driver_version(self):
        resp = requests.get(GECKO_LATEST_VERSION_URL)
        reg = re.search('\d{1,2}[\d.]+', resp.url.rpartition("/")[2])
        return reg.group(0)

    def _mount_chrome_json(self):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               'version_matcher.json'), "w+") as conf:

            notes_url = CHROME_VERSIONS_URL \
                .replace('{version}', str(self.version_latest))

            resp = requests.get(notes_url)
            r = re.findall(CHROME_SUPORTEDS_VERSIONS,
                           resp.text)
            chrome_json = {}
            json_file = {"CHROME": {}}
            for obj in r:
                _from = obj[1].rpartition("-")[0]
                _to = obj[1].rpartition("-")[2]
                chrome_json[obj[0]] = {"from": _from, "to": _to}
                json_file["CHROME"] = chrome_json
            json.dump(json_file, conf)
            conf.close()


def getConfig(*args):
    config = ConfigParser()
    path = os.path.dirname(__file__)
    file = 'drivers_info.ini'
    file_path = os.path.join(path, file)
    config.read(file_path)
    try:
        return config.get(*args)
    except Exception:
        return None


def getSection(section):
    config = ConfigParser()
    path = os.path.dirname(__file__)
    file = 'drivers_info.ini'
    file_path = os.path.join(path, file)
    config.read(file_path)
    try:
        return config[section]
    except Exception:
        return None
