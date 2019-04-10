import os
import re
import requests
import xml.etree.ElementTree as ET

from driloader.browser.exceptions import BrowserDetectionError
from driloader.commands import Commands
from driloader.proxy import Proxy
from .basebrowser import BaseBrowser


class IE(BaseBrowser):

    def __init__(self):
        super().__init__('IE')

    def get_latest_driver(self):
        """
        Gets the latest ie driver version.
        :return: the latest ie driver version.
        """
        resp = requests.get(self.section.get('RELEASES_URL'), proxies=Proxy().urls)
        xml_dl = ET.fromstring(resp.text)
        root = ET.ElementTree(xml_dl)
        tag = root.getroot().tag
        tag = tag.rpartition('}')[0] + tag.rpartition('}')[1]
        contents = root.findall(tag + 'Contents')
        last_version = 0
        for content in contents:
            version_str = content.find(tag + 'Key').text[:4]
            version_nbr = re.search(self.search_pattern_regex, version_str)
            if version_nbr is not None:
                version_str = version_nbr.group(0)
            try:
                version = float(version_str) if version_str is not None else 0
            except ValueError:
                version = 0
            if version > last_version:
                last_version = version
        # TODO: return the string version, because it can be 3.9.0, for instance.
        return str(last_version)

    def get_driver_matching_installed_version(self):
        # TODO: Version matcher for IE.
        return self.get_latest_driver()

    def get_installed_version(self):
        """ Returns Internet Explorer version.
        Args:
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting browser version.
        """

        if os.name != "nt":
            raise BrowserDetectionError('Unable to retrieve IE version.', 'System is not Windows.')

        cmd = ['reg', 'query',
               'HKEY_LOCAL_MACHINE\Software\Microsoft\Internet Explorer', '/v', 'svcVersion']

        try:
            output = Commands.run(cmd)
            reg = re.search(self.search_pattern_regex, str(output))
            str_version = reg.group(0)
            int_version = int(str_version.partition(".")[0])
        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve IE version from system.', error)

        return int_version
