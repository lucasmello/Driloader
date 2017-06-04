#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4


"""Driloadder Command Line Interface

   Using Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import sys
import argparse
from driloadder.browser_detection import BrowserDetection

class CliError(Exception):
    """ CliError """
    def __init__(self, message, cause):
        """Init method

        Sets superclass arguments up
        Sets the cause of exception up

        """
        super(CliError, self).__init__(message)
        self.cause = cause

    def __str__(self):
        return 'Error: {}.\nCause: {}'.format(self.args[0], self.cause)


class DriloadderCommands():
    """Class that accts as facade to BrowserDetection"""

    def __init__(self):
        """Init method

        Creates a new instance of BrowserDetection

        """

        self.browser_detection = BrowserDetection()

    def get_google_chrome_version(self):
        """ Returns Google Chrome version.

        Args:
            None

        Returns:
            Returns an int with the browser version.

        Raises:
            CliError: Case something goes wrong when getting the browser version

        """
        try:
            return self.browser_detection.get_chrome_version()
        except OSError as err:
            raise CliError('Unable to get Internet Explorer version', str(err))

    def get_firefox_version(self):
        """ Returns Firefox version.

        Args:
            None

        Returns:
            Returns an int with the browser version.

        Raises:
            CliError: Case something goes wrong when getting the browser version

        """
        try:
            return self.browser_detection.get_firefox_version()
        except OSError as err:
            raise CliError('Unable to get Internet Explorer version', str(err))

    def get_internet_explorer_version(self):
        """ Returns Internet Explorer version.

        Args:
            None

        Returns:
            Returns an int with the browser version.

        Raises:
            CliError: Case something goes wrong when getting the browser version

        """
        try:
            return self.browser_detection.get_internet_explorer_version()
        except OSError as err:
            raise CliError('Unable to get Internet Explorer version', str(err))


def get_python_version_error(python_version, acceptable_major, acceptable_minor):
    """ Returns Internet Explorer version.

    Args:
        python_version:
        acceptable_major:
        acceptable_minor:

    Returns:
        None

    Raises:
        CliError: Case something goes wrong when getting the browser version

    """
    message = 'Python {}.{} or later is required to run this script.'.format(acceptable_major, acceptable_minor)
    cause = 'Your current version is {}.{}.'.format(python_version[0], python_version[1])

    return message, cause


def check_python_version():
    acceptable_major = 3
    acceptable_minor = 6
    python_version = sys.version_info
    if python_version[0] >= acceptable_major:
        if python_version[1] >= acceptable_minor:
            return
        else:
            message, cause = get_python_version_error(python_version, acceptable_major, acceptable_minor)
            raise CliError(message, cause)
    else:
        message, cause = get_python_version_error(python_version, acceptable_major, acceptable_minor)
        raise CliError(message, cause)


def parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--verbose', '-v', help='Show more messages', action='store_true')
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
                        help='look for browsers an get their versions',
                        action='store_true')

    args = parser.parse_args()

    for key, value in args.__dict__.items():
        if value is True:
            return key


def display_outout(message, exit_code):

    if exit_code == 0:
        output_type = sys.stdout
    else:
        output_type = sys.stderr

    print(message, file=output_type)
    sys.exit(exit_code)


def main():
    try:
        check_python_version()
    except CliError as cli_error:
        display_outout(str(cli_error), 1)

    option = parse_args()
    commands = DriloadderCommands()
    options = {
        'chrome': commands.get_google_chrome_version,
        'firefox': commands.get_firefox_version,
        'internet_explorer': commands.get_internet_explorer_version
    }

    exit_code = 0

    try:
        result = options[option]()
        message = result

    except CliError as cli_error:
        display_outout(str(cli_error), 1)

    display_outout(message, exit_code)

if __name__ == '__main__':
    main()
