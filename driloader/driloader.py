# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
driloader.driloader
-------------------

Module which abstracts the main Driloader functions.
"""


import os
import sys

from .browsers import CHROMEDRIVER, GECKODRIVER, IEDRIVER
from .commands import Commands
from .downloader import Downloader
from .proxy import Proxy


def download_chrome_driver(path_to_download="default", version="autodetect", proxy=None):
    """
    Downloads the chrome driver.
    :param path_to_download: the path to put the file in.
    :param version: specify the chrome driver's version.
    :param proxy: proxy Dict. e.g {'http': '1.2.3.4', 'https': '5.6.7.8'}
    :return: the full path to the unzipped chrome driver.
    """
    return download_driver(path_to_download, version, CHROMEDRIVER, proxy)


def download_gecko_driver(path_to_download="default", version="autodetect", proxy=None):
    """
    Downloads the gecko driver (Firefox).
    :param path_to_download: the path to put the file in.
    :param version: specify the gecko driver's version.
    :param proxy: proxy Dict. e.g {'http': '1.2.3.4', 'https': '5.6.7.8'}
    :return: the full path to the unzipped gecko driver.
    """
    return download_driver(path_to_download, version, GECKODRIVER, proxy)


def download_ie_driver(path_to_download="default", version="autodetect", proxy=None):
    """
    Downloads the Internet Explorer driver.
    :param path_to_download: the path to put the file in.
    :param version: specify the ie driver's version.
    :param proxy: proxy Dict. e.g {'http': '1.2.3.4', 'https': '5.6.7.8'}
    :return: the full path to the unzipped ie driver.
    """
    return download_driver(path_to_download, version, IEDRIVER, proxy)


def download_driver(path_to_download, version, browser, proxy):
    """
    Downloads the driver according to browser parameter.
    :param path_to_download: the path to put the file in.
    :param version: the driver version.
    :param browser: the browser to download it's specific driver.
    :param proxy: proxy Dict. e.g {'http': '1.2.3.4:8080', 'https': '5.6.7.8:8080'}
    :return: the full unzipped driver's path.
    """
    if proxy:
        Proxy(proxy)
    driver = Downloader(browser)

    if version == "autodetect":
        driver_version = driver.browser.version_supported
    elif version == "latest":
        driver_version = driver.browser.version_latest
    else:
        driver_version = version

    unzipped_path = "{0}{1}{2}{3}{2}{4}".format(driver.get_default_path(), driver.browser.driver,
                                                os.sep, driver_version, driver.browser.file_name)

    file_name_zipped = driver.browser.file_name_zip
    file_name_zipped = file_name_zipped.replace('{version}', str(driver_version))

    download_url = "{}{}".format(driver.browser.base_url, file_name_zipped)
    download_url = download_url.replace("{version}", str(driver_version))

    if path_to_download == "default":

        driver.drivers_path += "{}{}{}".\
            format(str(driver.browser.driver), os.sep, str(driver_version))

        if not os.path.exists(driver.drivers_path):
            os.makedirs(driver.drivers_path)
        full_path = driver.drivers_path + os.sep + file_name_zipped
    else:
        full_path = path_to_download + os.sep + file_name_zipped
        unzipped_path = "{}{}{}".format(path_to_download, os.sep, driver.browser.file_name)

    if driver.check_driver_exists(unzipped_path):
        return unzipped_path

    driver.download_file(download_url, full_path)
    driver.unzip(full_path, driver.drivers_path, True)
    if sys.platform == "linux" and browser == CHROMEDRIVER:
        make_executable = "chmod +x {}{}{}".format(driver.drivers_path, os.sep, "chromedriver")
        Commands.run(make_executable)
    return unzipped_path
