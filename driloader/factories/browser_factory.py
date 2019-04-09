from driloader.browser.basebrowser import BaseBrowser
from driloader.browser.chrome import Chrome
from driloader.browser.exceptions import BrowserNotSupportedError
from driloader.browser.firefox import Firefox
from driloader.browser.internet_explorer import IE


class BrowserFactory(BaseBrowser):

    def __init__(self, browser_name):
        self.browser_name = browser_name

    def get_latest_driver(self):
        if self.browser_name.upper() == 'CHROME':
            return Chrome().get_latest_driver()
        elif self.browser_name.upper() == 'FIREFOX':
            return Firefox().get_latest_driver()
        elif self.browser_name.upper() == 'IE':
            return IE().get_latest_driver()
        else:
            raise BrowserNotSupportedError('Sorry, but we currently not support your Browser.')

    def get_driver_matching_installed_version(self):
        if self.browser_name.upper() == 'CHROME':
            return Chrome().get_driver_matching_installed_version()
        elif self.browser_name.upper() == 'FIREFOX':
            return Firefox().get_driver_matching_installed_version()
        elif self.browser_name.upper() == 'IE':
            return IE().get_driver_matching_installed_version()
        else:
            raise BrowserNotSupportedError('Sorry, but we currently not support your Browser.')

    def get_installed_version(self):
        if self.browser_name.upper() == 'CHROME':
            return Chrome().get_installed_version()
        elif self.browser_name.upper() == 'FIREFOX':
            return Firefox().get_installed_version()
        elif self.browser_name.upper() == 'IE':
            return IE().get_installed_version()
        else:
            raise BrowserNotSupportedError('Sorry, but we currently not support your Browser.')
