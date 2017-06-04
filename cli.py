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


class DriloadderCommands():
    def __init__(self):
        self.bd = BrowserDetection()
        self.exit_stdout = 0
        self.exit_stderr = 1

    def get_google_chrome_version(self):
        return ((self.bd.get_chrome_version()), self.exit_stdout)

    def get_firefox_version(self):
        return (self.bd.get_firefox_version(), self.exit_stdout)


    def get_internet_explorer_version(self):
        try:
            return (self.bd.get_internet_explorer_version(), self.exit_stdout)
        except OSError as err:
            return (self.format_error_output('Unable to get Internet Explorer version. Cause: {}'.format(str(err))),
                    self.exit_stderr)

    @staticmethod
    def format_error_output(error):
        return "A error happend: {}".format(error)


def show_python_version_error_error(python_version, acceptable_major, acceptable_minor):
    print('Python {}.{} or later is required to run this script.\n'
          'Your current version is {}.{}.'.format(acceptable_major,
                                                  acceptable_minor,
                                                  python_version[0],
                                                  python_version[1]), file=sys.stderr)
    sys.exit(1)


def check_python_version():
    acceptable_major = 3
    acceptable_minor = 6
    python_version = sys.version_info
    if python_version[0] >= acceptable_major:
        if python_version[1] >= acceptable_minor:
            return
        else:
            show_python_version_error_error(python_version, acceptable_major, acceptable_minor)
    else:
        show_python_version_error_error(python_version, acceptable_major, acceptable_minor)


def parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--verbose', '-v', help='Show more messages', action='store_true')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--firefox', '-f', help='get Firefox version.', action='store_true')
    action.add_argument('--chrome', '-c', help='get Google Chrome version.', action='store_true')
    action.add_argument('--internet-explorer', '-i', help='get Internet Explorer version.', action='store_true')
    action.add_argument('--all', help='look for browsers an get their versions', action='store_true')
    args = parser.parse_args()

    for key, value in args.__dict__.items():
        if value is True:
            return key


def main():
    option = parse_args()
    commands = DriloadderCommands()
    options = {
        'chrome': commands.get_google_chrome_version,
        'firefox': commands.get_firefox_version,
        'internet_explorer': commands.get_internet_explorer_version
    }

    result = options[option]()
    message = result[0]
    exit_code = result[1]
    if exit_code == 1:
        output_type = sys.stderr
    else:
        output_type = sys.stdout

    print(message, file=output_type)
    sys.exit(exit_code)


if __name__ == '__main__':
    check_python_version()
    main()
