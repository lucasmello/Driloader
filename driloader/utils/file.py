# pylint: disable=import-outside-toplevel
"""
driloader.utils.file
--------------------

Module to abstract file related operations.

"""


import os
import zipfile

from driloader.utils.commands import Commands


class FileHandler:

    """
    Handles file operations.
    """

    @staticmethod
    def create_folders(folder_path, hidden=False):
        """
        Creates folders recursively.
        :param folder_path: the folder path.
        :param hidden: if the last created folder should be hidden.
        :return: the full folder path.
        """
        if hidden:
            if os.name == 'nt':
                import ctypes
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                ctypes.windll.kernel32.SetFileAttributesW(folder_path, 2)
            else:
                folder_path = folder_path.replace("Drivers", ".Drivers")
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
        return folder_path

    @staticmethod
    def unzip(zip_file, path_to_extract, delete_after_extract=False):
        """
        Extract a 'zip' or 'gz' file content to the same path as file is in.
        :param zip_file: file to be extracted.
        :param delete_after_extract: deletes original zipped file after it's extracted.
        :param path_to_extract: the path to extract the file.
        """
        if zip_file.endswith("zip"):
            zfile = zipfile.ZipFile(zip_file, "r")
            zfile.extractall(path_to_extract)
            zfile.close()
        elif zip_file.endswith("gz"):
            Commands.run("tar -zxvf {} -C {}".format(zip_file, zip_file.rpartition("/")[0]))
        if delete_after_extract:
            os.remove(zip_file)

    @staticmethod
    def write_content(path, content):
        """
        Writes the response's content to disk.
        """
        with open(path, "wb") as file:
            file.write(content)
