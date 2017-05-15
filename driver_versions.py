import requests
import xml.etree.ElementTree as ET
import re

class DriverVersions:

    @staticmethod
    def get_latest_ie_driver_version():
        resp = requests.get("http://selenium-release.storage.googleapis.com/")

        xml_dl = ET.fromstring(resp.text)
        root = ET.ElementTree(xml_dl)
        tag = root._root.tag
        tag = tag.rpartition("}")[0] + tag.rpartition("}")[1]
        contents = root.findall(tag + "Contents")
        last_version = 0
        for content in contents:
            version_str = content.find(tag + "Key").text[:4]
            version_nbr = re.search("\d{1,2}[\,\.]{1}\d{1,2}", version_str)
            if version_nbr is not None:
                version_str = version_nbr.group(0)
            try:
                version = float(version_str) if version_str is not None else 0
            except:
                version = 0
            if version > last_version:
                last_version = version
        return last_version
