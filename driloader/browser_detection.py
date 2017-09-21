# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=anomalous-backslash-in-string

"""Browser Detection
   Using Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import re
import subprocess
import platform
import sys


class BrowserDetectionError(Exception):
    """ BrowserDetectionError """
    def __init__(self, message, cause):
        """Init method
        Sets superclass arguments up.
        Sets the cause of exception up.
        """
        super(BrowserDetectionError, self).__init__(message)
        self.cause = cause

    def __str__(self):
        return 'Error: {}.\nCause: {}'.format(self.args[0], self.cause)


class BrowserDetection:
    """ Provides methods to retrieve the browser's version """

    def __init__(self):
        """ Sets up the system information """

        self.os_name = platform.system()
        self.pattern = r"\d{1,2}[\,\.]{1}\d{1,2}"

    def get_internet_explorer_version(self):
        """ Returns Internet Explorer version.
        Args:
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting browser version.
        """

        if self.os_name != "Windows":
            raise BrowserDetectionError('Unable to retrieve IE version.', 'System is not Windows.')

        cmd = ['reg', 'query',
               'HKEY_LOCAL_MACHINE\Software\Microsoft\Internet Explorer', '/v', 'svcVersion']

        try:
            output = self._run_command(cmd)
            reg = re.search(self.pattern, str(output))
            str_version = reg.group(0)
            int_version = int(str_version.partition(".")[0])
        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve IE version from system.', error)

        return int_version

    def get_chrome_version(self):
        """ Returns Google Chrome version.
        Args:
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting browser version.
        """

        try:
            if self.os_name == "Linux":
                str_version = self._run_command("google-chrome --product-version")

            if self.os_name == "Windows":
                app = 'C:\\\Program Files (x86)\\\Google\\\Chrome\\\Application\\\chrome.exe"'
                cmd = ['wmic', 'datafile', 'where',
                       'name="{}'.format(app), 'get', 'Version', '/value']

                result = self._run_command(cmd)
                res_reg = re.search(self.pattern, str(result))
                str_version = res_reg.group(0)

        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve Chrome version from system', error)

        int_version = int(str_version.partition('.')[0])
        return int_version

    def get_firefox_version(self):
        """ Returns Firefox version.
        Args:
            self
        Returns:
            Returns an int with the browser version.
        Raises:
            BrowserDetectionError: Case something goes wrong when getting browser version.
        """

        try:

            if self.os_name == "Linux":
                output = subprocess.getoutput("firefox -v")
            elif self.os_name == "Windows":
                ff_path = self._find_firefox_exe_in_registry()
                output = self._run_command([ff_path, '-v', '|', 'more'])

            if output is not None:
                out_reg = re.search(self.pattern, str(output))
                str_version = out_reg.group(0)
                int_version = int(str_version.partition(".")[0])
                return int_version

        except Exception as error:
            raise BrowserDetectionError('Unable to retrieve Firefox version from system', error)

    @staticmethod
    def _find_firefox_exe_in_registry():
        """ Finds firefox.exe file in Windows systems.
        Args:
        Returns:
            Returns an string with firefox.exe path.
        Raises:
            None
        """

        try:
            from _winreg import OpenKey, QueryValue, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER
        except ImportError:
            from winreg import OpenKey, QueryValue, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER

        import shlex

        keys = (r"SOFTWARE\Classes\FirefoxHTML\shell\open\command",
                r"SOFTWARE\Classes\Applications\firefox.exe\shell\open\command")

        for path in keys:
            try:
                key = OpenKey(HKEY_LOCAL_MACHINE, path)
                command = QueryValue(key, "")
                break
            except OSError:
                try:
                    key = OpenKey(HKEY_CURRENT_USER, path)
                    command = QueryValue(key, "")
                    break
                except OSError:
                    pass
        else:
            return ""

        if not command:
            return ""

        return shlex.split(command)[0]

    @staticmethod
    def _run_command(command):
        """ Run command.
        Runs any command sent as parameter and returns its stdout
        in case of success.
        Args:
            command: Can be a string or string list containing a command line.
            For example: "ls -l" and "firefox" or ['ls', '-l'] and ['firefox']
        Returns:
            Returns an string with the command stdout.
        Raises:
            Exception: The command was not found.
            Exception: The command was found but failed.
        TODO (jonathadv): Create specific exceptions.
        """
        if isinstance(command, str):
            command_array = command.split(" ")
        else:
            command_array = command

        try:
            if int(sys.version[0]) == 3 and int(sys.version[2]) < 5:
                cmd_result = subprocess.check_output(command_array)
            else:
                cmd_result = subprocess.run(command_array, stdout=subprocess.PIPE)

            if (hasattr(cmd_result, "returncode") and cmd_result.returncode == 0)\
                    or cmd_result is not None:
                result = None
                stdout = cmd_result.stdout if hasattr(cmd_result, "stdout") else cmd_result
                if isinstance(stdout, bytes):
                    result = stdout.decode('utf-8')
                else:
                    result = stdout

                return result
            else:
                raise Exception("Command \"{}\" failed!".format(" ".join(command)))

        except FileNotFoundError:
            raise Exception("Command \"{}\" not found!".format(" ".join(command)))