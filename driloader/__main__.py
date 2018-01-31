#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=too-few-public-methods

"""Driloader Command Line Interface
   Using Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import argparse
import sys

from .browser_detection import BrowserDetection, BrowserDetectionError


class OutputType():
    """Output Type
    Enum Class to store the possible output types.
    Types:
        INFO: Any information non-error related.
        ERROR: Any error message.
    """
    INFO = 'INFO'
    ERROR = 'ERROR'


class CliError(Exception):
    """ CliError """

    def __init__(self, message, cause):
        """Init method
        Sets superclass arguments up.
        Sets the cause of exception up.
        """
        super(CliError, self).__init__(message)
        self.cause = cause

    def __str__(self):
        return 'Error: {}.\nCause: {}'.format(self.args[0], self.cause)


class DriloaderCommands():
    """A facade to BrowserDetection"""

    def __init__(self):
        """Init method"""
        self.detection = BrowserDetection()

    def get_google_chrome_version(self):
        """ Returns Google Chrome version.
        Args:
            self
        Returns:
            Returns an int with the browser version.
        Raises:
            CliError: Case something goes wrong when getting the browser version.
        """
        try:
            return self.detection.get_chrome_version()
        except BrowserDetectionError as err:
            raise CliError('Unable to get the Google Chrome version', str(err))

    def get_firefox_version(self):
        """ Returns Firefox version.
        Args:
            self
        Returns:
            Returns an int with the browser version.
        Raises:
            CliError: Case something goes wrong when getting the browser version.
        """
        try:
            return self.detection.get_firefox_version()
        except BrowserDetectionError as err:
            raise CliError('Unable to get the Firefox version', str(err))

    def get_internet_explorer_version(self):
        """ Returns Internet Explorer version.
        Args:
            self
        Returns:
            Returns an int with the browser version.
        Raises:
            CliError: Case something goes wrong when getting the browser version.
        """
        try:
            return self.detection.get_internet_explorer_version()
        except BrowserDetectionError as err:
            raise CliError('Unable to get the Internet Explorer version', str(err))

    def get_all_browsers_versions(self):
        """ Returns all browsers version.
        Args:
            self
        Returns:
            Returns an string with the browser version. Like:
            Internet Explorer: 11
            Firefox: 45
            Google Chrome: 58
        Raises:
            None
        """
        result_message = 'Firefox: {}\nGoogle Chrome: {}\nInternet Explorer: {}\n'

        try:
            ff_version = str(self.get_firefox_version())
        except CliError as error:
            ff_version = str(error)

        try:
            chrome_version = str(self.get_google_chrome_version())
        except CliError as error:
            chrome_version = str(error)

        try:
            ie_version = str(self.get_internet_explorer_version())
        except CliError as error:
            ie_version = str(error)

        return result_message.format(ff_version, chrome_version, ie_version)


def parse_args():
    """ Parse Arguments
    Parse arguments from stdin.
    Args:
    Returns:
        A string argument from stdin.
    Raises:
        None
    """

    parser = argparse.ArgumentParser(prog="driloader")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--firefox', '-f',
                        help='get Firefox version.',
                        action='store_true')

    action.add_argument('--chrome', '-c',
                        help='get Google Chrome version.',
                        action='store_true')

    action.add_argument('--internet-explorer', '-i',
                        help='get Internet Explorer version.',
                        action='store_true')

    action.add_argument('--all',
                        help='look for browsers an get their versions.',
                        action='store_true')

    args = parser.parse_args()

    for key, value in args.__dict__.items():
        if value is True:
            return key
    return None


def display_output(message, output_type=OutputType.INFO):
    """ Display Output
    Displays an output message to the correct file descriptor (STDIN or STDOUT) and exits
    the script based on the type sent as parameter.
    If output_type == OutputType.INFO sends the message to STDIN and exits with code 0.
    If output_type == OutputType.ERROR sends the message to STDERR and exits with code 1.
    Args:
        message: The message to be displayed.
        output_type: A type in OutputType class
    Returns:
        None
    Raises:
        None
    """

    if output_type == OutputType.INFO:
        std_descriptor = sys.stdout
        exit_code = 0
    else:
        std_descriptor = sys.stderr
        exit_code = 1

    message = str(message)
    if 'Cause' in message:
        message = message.replace('Cause', '\tCause')

    print(message, file=std_descriptor)
    sys.exit(exit_code)


def main():
    """ Main Function
    Responsible for:
        - call the parse_args() function and get the parameter sent from stdin.
        - instantiate the DriloaderCommands class and call its methods based
        on the argparser input.
    Args:
    Returns:
        None
    Raises:
        None
    """

    option = parse_args()
    commands = DriloaderCommands()
    options = {
        'chrome': commands.get_google_chrome_version,
        'firefox': commands.get_firefox_version,
        'internet_explorer': commands.get_internet_explorer_version,
        'all': commands.get_all_browsers_versions
    }
    message = ''

    try:
        result = options[option]()
        message = result

    except CliError as cli_error:
        display_output(str(cli_error), OutputType.ERROR)

    display_output(message, OutputType.INFO)


if __name__ == '__main__':
    main()
