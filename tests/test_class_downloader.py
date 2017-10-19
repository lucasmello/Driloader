import os
import random

import pytest
import pytest_mock

from requests import Response

from driloader.downloader import Downloader
from driloader.browsers import GECKODRIVER, CHROMEDRIVER, IEDRIVER


def test_download_driver_file(mocker):
    mock_file_content = str(random.random())
    mock_file_name = './test_driver_downloader.txt'

    mocker.patch.object(Response, 'content')
    Response.content = bytes(mock_file_content, 'UTF-8')

    downloader = Downloader(GECKODRIVER)
    downloader.download_file('http://test.com', mock_file_name)

    with open(mock_file_name, 'r') as file:
        file_content = file.read()
    file.close()
    os.remove(mock_file_name)

    assert file_content == mock_file_content
