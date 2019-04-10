from driloader.browser.chrome import Chrome
from driloader.browser.exceptions import BrowserNotSupportedError
from driloader.browser.firefox import Firefox
from driloader.browser.internet_explorer import IE


class BrowserFactory:

    def __init__(self, browser_name):
        self._browser_name = browser_name
        self.browser = self._get_browser()

    def _get_browser(self):
        if self._browser_name.upper() == 'CHROME':
            return Chrome()
        elif self._browser_name.upper() == 'FIREFOX':
            return Firefox()
        elif self._browser_name.upper() == 'IE':
            return IE()
        else:
            raise BrowserNotSupportedError('Sorry, but we currently not support your Browser.')
