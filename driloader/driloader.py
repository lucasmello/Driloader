# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
driloader.driloader
-------------------

Module which abstracts the main Driloader functions.
"""

from .browser.chrome import Chrome
from .browser.drivers import Driver
from .browser.firefox import Firefox
from .browser.internet_explorer import IE


def chrome():
    """
    Returns an instance of Chrome's class.
    """
    driver = Driver()
    driver.browser = 'chrome'
    return Chrome(driver)


def firefox():
    """
    Returns an instance of Firefox's class.
    """
    driver = Driver()
    driver.browser = 'firefox'
    return Firefox(driver)


def internet_explorer():
    """
    Returns an instance of Firefox's class.
    """
    driver = Driver()
    driver.browser = 'ie'
    return IE(driver)
