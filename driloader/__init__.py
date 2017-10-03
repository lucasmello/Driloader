# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
Driloader
---------

Selenium drivers downloader tool with standalone CLI support.

Selenium needs a specific driver to work with each browser. Every driver has a
version that works with specific browser versions, and it's really annoying
reading the changelogs to check if the current driver will work with the new
browser version. Plus, a lot of times a test crashes because the browser has
updated and the driver is not compatible anymore. That's why Driloader exists:
To make this process so much easier!

Driloader autodetect the browser version (it supports Chrome, Firefox and
Internet Explorer) and download the driver according to it's version.

usage:

 - Usage with Firefox

    >>> from driloader import driloader
    >>> from selenium.webdriver import Firefox
    >>>
    >>> driver_path = driloader.download_gecko_driver()
    >>> browser = Firefox(executable_path=driver_path)
    >>> browser.get("http://www.google.com")
    >>> browser.quit()

 - Usage with Chrome

    >>> from driloader import driloader
    >>> from selenium.webdriver import Chrome
    >>>
    >>> driver_path = driloader.download_chrome_driver()
    >>> browser = Chrome(executable_path=driver_path)
    >>> browser.get("http://www.google.com")
    >>> browser.quit()

 - Usage with Internet Explorer
    >>> from driloader import driloader
    >>> from selenium.webdriver import Ie
    >>>
    >>> driver_path = driloader.download_ie_driver()
    >>> browser = Ie(executable_path=driver_path)
    >>> browser.get("http://www.google.com")
    >>> browser.quit()
"""


from .driloader import download_chrome_driver, download_gecko_driver, download_ie_driver
