# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Disabling the below pylint warnings in order to use long names convention to tests
# and because pytest and pytest_mock imports are used seamlessly.

# pylint: disable=invalid-name
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods



"""
tests.test_class_downloader
------------------

The test set for functions in driloader.downloader.Downloader
"""


import os
import random

import pytest
import pytest_mock

from requests import Response

from driloader.downloader import Downloader
from driloader.browsers import IEDRIVER


class TestDownloader:
    """ Test Downloader by mocking the requests calls """

    @staticmethod
    def test_download_driver_file(mocker):
        """ Test the download of a file by mocking the
            requests.Response object as a text file with a random number.

            The assertion consists in checking if the content saved by the tested
            function is a text file with the same random number.

            Using IEDRIVER and mocking the needed functions from driloader.browsers
            to ensure the mocking would take care of all real system information.

            This test takes usually longer than 1s, probably because of IO operations
            run in downloader.download_file().
        """

        mocked_response = str(random.random())
        mock_file_name = './test_driver_downloader.txt'

        mocker.patch.object(Response, 'content')
        Response.content = bytes(mocked_response, 'UTF-8')

        mocker.patch('platform.system', return_value='Windows')
        mocker.patch('driloader.browsers.Browser.__init__', return_value=None)
        mocker.patch('driloader.downloader.Downloader._create_driver_folder',
                     return_value='hidden_name')

        downloader = Downloader(IEDRIVER)
        downloader.download_file('http://test.com', mock_file_name)

        with open(mock_file_name, 'r') as file:
            file_content = file.read()
        file.close()
        os.remove(mock_file_name)

        assert file_content == mocked_response
