"""
Responsible to return the abstract browser configs.
"""
from abc import ABC, abstractmethod


class BrowserConfigBase(ABC):
    """
    Holds abstract methods to be implemented in Browser Config classes.
    """

    @abstractmethod
    def base_url(self):
        """
        Return base_url.
        """
        raise NotImplementedError

    @abstractmethod
    def zipped_file_name(self, replace_version=''):
        """
        Return zipped_file_name.
        @param replace_version: if in browsers.ini there's a '{version}'
        due to dynamic versions with geckodriver.
        """
        raise NotImplementedError

    @abstractmethod
    def unzipped_file_name(self):
        """
        Return unzipped_file_name.
        """
        raise NotImplementedError

    @abstractmethod
    def latest_release_url(self):
        """
        Return latest_release_url.
        """
        raise NotImplementedError

    @abstractmethod
    def index_url(self):
        """
        Return index_url.
        """
        raise NotImplementedError

    @abstractmethod
    def versions_url(self):
        """
        Return versions_url.
        """
        raise NotImplementedError
