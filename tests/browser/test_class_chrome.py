import os
import shutil
import zipfile
from random import random

import pytest
from requests import Response
from requests_html import HTMLResponse, HTML, Element

from driloader.browser.chrome import Chrome
from driloader.browser.drivers import Driver


class TestChrome:

    @staticmethod
    @pytest.fixture()
    def mock_system(mocker):
        """ Fixture to mock the main functions Downloader class
        depends on in order to avoid mocke them in every new test.
        """
        mocker.patch('platform.system', return_value='Windows')
        mocker.patch('driloader.browser.drivers.Driver.create_folder',
                     return_value='./')
        mocker.patch.object(Response, 'content')
        Response.content = bytes(str(random()), 'UTF-8')
        # mocker.patch('driloader.browser.Browser.__init__', return_value=None)

    @staticmethod
    def test_installed_version_without_setting_path(mocker):
        mocker.patch('driloader.utils.commands.Commands.run',
                     return_value='1')
        chrome = Chrome(Driver('chrome'))
        assert chrome.installed_browser_version() == 1

    @staticmethod
    def test_installed_version_setting_path(mocker):
        mocker.patch('driloader.utils.commands.Commands.run',
                     return_value='2')
        chrome = Chrome(Driver('chrome')).binary('/mock/path')
        assert chrome.installed_browser_version() == 2


    @staticmethod
    def test_get_driver(mocker):
        driver = Driver()
        driver.browser = 'chrome'
        driver.version = '123mock'
        driver.drivers_path = '../'
        mocker.patch.object(HTML, 'find')

        mocker.patch('driloader.browser.chrome.Chrome._get_latest_driver_version_from_chrome_version',
                     return_value='123mock')
        mocker.patch('driloader.config.paths.Paths.zipped_file_path',
                     return_value='./chrome/{}/chromedriver.zip'.format(driver.version))
        mocker.patch('driloader.utils.file.FileHandler.write_content',
                     side_effect=TestChrome._zip_file_mock(driver))
        mocker.patch('driloader.http.operations.HttpOperations.get',
                     return_value=Response())
        Chrome(driver).get_driver()
        shutil.rmtree('./chrome/', ignore_errors=True)

    @staticmethod
    def _zip_file_mock(driver):
        shutil.rmtree('./chrome/', ignore_errors=True)
        os.makedirs('./chrome/{}'.format(driver.version))
        zip_mock = zipfile.ZipFile('./chrome/{}/chromedriver.zip'.format(driver.version), 'w')
        zip_mock.write('./chrome/{}/chromedriver.zip'.format(driver.version))
        zip_mock.close()
