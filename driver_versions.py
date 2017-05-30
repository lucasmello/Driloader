import json
import os

import requests
import xml.etree.ElementTree as ET
import re


class DriverVersions:

    def __init__(self):
        self.pattern = "\d{1,2}[\,\.]{1}\d{1,2}"
        self._mount_chrome_json()

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
            version_nbr = re.search(self.pattern, version_str)
            if version_nbr is not None:
                version_str = version_nbr.group(0)
            try:
                version = float(version_str) if version_str is not None else 0
            except Exception:
                version = 0
            if version > last_version:
                last_version = version
        return last_version

    def get_latest_chrome_driver_version(self):
        resp = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        reg = re.search(self.pattern, resp.text)
        return float(reg.group(0))

    def get_latest_gecko_driver_version(self):
        resp = requests.get("https://github.com/mozilla/geckodriver/releases/latest")
        reg = re.search(self.pattern, resp.url.rpartition("/")[2])
        return float(reg.group(0))

    def _mount_chrome_json(self):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'version_matcher.json'), "a+") as conf:
            resp = requests.get("https://chromedriver.storage.googleapis.com/2.29/notes.txt")
            r = re.findall("----------ChromeDriver v((?:\d+\.?)+) \((?:\d+-?)+\)----------\nSupports Chrome v((?:\d+-?)+)",
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
