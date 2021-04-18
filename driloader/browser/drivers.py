"""
Responsible to implement the class to control driver's info.
"""
import os

from driloader.utils.commands import Commands
from driloader.utils.file import FileHandler


class Driver:
    """
    Holds useful information about drivers.
    """

    def __init__(self, browser=''):
        self.drivers_path = None
        self._driver_version = ''
        self.browser = browser

    @property
    def version(self):
        """
        Returns the driver version.
        """
        return self._driver_version

    @version.setter
    def version(self, value):
        """
        Set the driver version.
        """
        self._driver_version = value

    def create_folder(self):
        """
        Creates a folder to put the drivers and hides it.
        :return: the folder path.
        """
        self.drivers_path = os.path.expanduser('~{0}Driloader{0}Drivers{0}'.format(os.sep))
        return FileHandler.create_folders(self.drivers_path, hidden=True)

    @staticmethod
    def exists(path_to_file):
        """
        Checks if the driver exists.
        :param path_to_file: the file to be checked.
        :return: True if file exists, otherwise False.
        """
        return os.path.isfile(path_to_file)

    def default_path(self):
        """
        Get the full unzipped file's path.
        :return: unzipped file's path.
        """
        return self.drivers_path

    @staticmethod
    def make_executable(file):
        """
        Makes the driver executable.
        """
        make_executable = 'chmod +x {}'.format(file)
        Commands.run(make_executable)
