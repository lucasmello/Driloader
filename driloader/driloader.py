import sys
import os
from .downloader import Downloader
from .browsers import CHROMEDRIVER, GECKODRIVER, IEDRIVER
from .commands import Commands


def download_chrome_driver(path_to_download="default", version="autodetect"):
    return download_driver(path_to_download, version, CHROMEDRIVER)


def download_gecko_driver(path_to_download="default", version="autodetect"):
    return download_driver(path_to_download, version, GECKODRIVER)


def download_ie_driver(path_to_download="default", version="autodetect"):
    return download_driver(path_to_download, version, IEDRIVER)


def download_driver(path_to_download, version, browser):
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
