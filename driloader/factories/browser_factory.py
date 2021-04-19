# pylint: disable=too-few-public-methods

"""

driloader.factories.browser_factory

Module which abstracts the browser instantiations.

"""

from driloader.browser.chrome import Chrome
from driloader.browser.drivers import Driver
from driloader.browser.exceptions import BrowserNotSupportedError
from driloader.browser.firefox import Firefox
from driloader.browser.internet_explorer import IE


class BrowserFactory:

    """
    Provides the right instance based on browser name.
    """

    def __init__(self, browser_name):
        self._browser_name = browser_name
        self.browser = self._get_browser()

    def _get_browser(self):
        """
        Get browser's instance according to browser's name.
        :return:
        """
        if self._browser_name.upper() == 'CHROME':
            driver = Driver()
            driver.browser = 'chrome'
            return Chrome(driver)
        if self._browser_name.upper() == 'FIREFOX':
            driver = Driver()
            driver.browser = 'firefox'
            return Firefox(driver)
        if self._browser_name.upper() == 'IE':
            driver = Driver()
            driver.browser = 'ie'
            return IE(driver)
        raise BrowserNotSupportedError('Sorry, but we currently not'
                                       ' support your Browser.',
                                       'Browser is not supported.')
