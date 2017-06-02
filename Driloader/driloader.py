import os
from .downloader import Downloader
from .browsers import CHROMEDRIVER, GECKODRIVER, IEDRIVER


def download_chrome_driver(path_to_download="default", version="autodetect"):
    download_driver(path_to_download, version, CHROMEDRIVER)


def download_gecko_driver(path_to_download="default", version="autodetect"):
    download_driver(path_to_download, version, GECKODRIVER)


def download_ie_driver(path_to_download="default", version="autodetect"):
    download_driver(path_to_download, version, IEDRIVER)


def download_driver(path_to_download, version, browser):
    driver = Downloader(browser)

    if version == "autodetect":
        driver_version = driver.browser.version_suported
    elif version == "latest":
        driver_version = driver.browser.version_latest
    else:
        driver_version = version

    file_name = driver.browser.file_name_zip
    file_name = file_name.replace('{version}', driver_version)

    download_url = "{}{}".format(driver.browser.base_url, file_name)
    download_url = download_url.replace("{version}", str(driver_version))

    print('dl ' + download_url)
    print('fl ' + file_name)

    if path_to_download == "default":
        driver.drivers_path += str(driver_version)
        if not os.path.exists(driver.drivers_path):
            os.makedirs(driver.drivers_path)
        full_path = driver.drivers_path + os.sep + file_name
    else:
        full_path = path_to_download + os.sep + file_name

    print('full_path' + full_path)
    print('driver' + driver.drivers_path)

    driver._download_file(download_url, full_path)
    driver._unzip(full_path, driver.drivers_path, True)
    return driver._get_path(driver.browser.driver)
