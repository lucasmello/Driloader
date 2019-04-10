# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
driloader.driloader
-------------------

Module which abstracts the main Driloader functions.
"""


import os
import sys

from driloader.utils.file import FileHandler
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
    return download_driver(path_to_download, version, 'CHROME', proxy)


def download_gecko_driver(path_to_download="default", version="autodetect", proxy=None):
    """
    Downloads the gecko driver (Firefox).
    :param path_to_download: the path to put the file in.
    :param version: specify the gecko driver's version.
    :param proxy: proxy Dict. e.g {'http': '1.2.3.4', 'https': '5.6.7.8'}
    :return: the full path to the unzipped gecko driver.
    """
    return download_driver(path_to_download, version, 'FIREFOX', proxy)


def download_ie_driver(path_to_download="default", version="autodetect", proxy=None):
    """
    Downloads the Internet Explorer driver.
    :param path_to_download: the path to put the file in.
    :param version: specify the ie driver's version.
    :param proxy: proxy Dict. e.g {'http': '1.2.3.4', 'https': '5.6.7.8'}
    :return: the full path to the unzipped ie driver.
    """
    return download_driver(path_to_download, version, 'IE', proxy)


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
        driver_version = driver.browser_factory.get_driver_matching_installed_version()
    elif version == "latest":
        driver_version = driver.browser_factory.get_latest_driver()
    else:
        driver_version = version

    unzipped_path = os.path.join(driver.get_default_path(), browser,
                                 driver_version, driver.browser_factory.unzipped_file)

    download_url = "{}{}".format(driver.browser_factory.base_url, driver.browser_factory.zipped_file)
    download_url = download_url.replace("{version}", str(driver_version))

    p = os.path.join(driver.drivers_path, browser, driver_version)

    if path_to_download == "default":

        if not os.path.exists(driver.drivers_path):
            os.makedirs(driver.drivers_path)
        full_path = os.path.join(p, driver.browser_factory.zipped_file)
    else:
        full_path = os.path.join(path_to_download, driver.browser_factory.zipped_file)
        unzipped_path = os.path.join(path_to_download, driver.browser_factory.unzipped_file)

    full_path = full_path.replace('{version}', driver.browser_factory.get_driver_matching_installed_version())

    if driver.check_driver_exists(unzipped_path):
        return unzipped_path

    driver.download_file(download_url, full_path)
    FileHandler.unzip(full_path, p, True)
    if sys.platform == 'linux' and browser == 'CHROME':
        make_executable = 'chmod +x {}'.format(unzipped_path)
        Commands.run(make_executable)
    return unzipped_path
