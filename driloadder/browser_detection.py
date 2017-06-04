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

class BrowserDetection:
    """ Provides methods to retrieve the browser's version """

    def __init__(self):
        """ Sets up the system information """

        self.os_name = platform.system()
        self.pattern = r"\d{1,2}[\,\.]{1}\d{1,2}"

    def get_internet_explorer_version(self):
        """ Returns Internet Explorer version.

        Args:
            None

        Returns:
            Returns an int with the browser version.

        Raises:
            None

        TODO (jonathadv): Add exceptions handling.

        """

        if self.os_name != "Windows":
            raise EnvironmentError("System is not Windows.")

        cmd = 'reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Internet Explorer" /v svcVersion'
        output = self._run_command(cmd)
        reg = re.search(self.pattern, output)
        str_version = reg.group(0)
        int_version = int(str_version.partition(".")[0])

        return int_version

    def get_chrome_version(self):
        """ Returns Google Chrome version.

        Args:
            None

        Returns:
            Returns an int with the browser version.

        Raises:
            None

        TODO (jonathadv): Add exceptions handling.

        """

        if self.os_name == "Linux":
            str_version = self._run_command("google-chrome --product-version")

        if self.os_name == "Windows":
            cmd = 'wmic datafile where name="C:\\\Program Files (x86)\\\Google\
            \\\Chrome\\\Application\\\chrome.exe" get Version'
            result = self._run_command(cmd)
            res_reg = re.search(self.pattern, result)
            str_version = res_reg.group(0)

        int_version = int(str_version.partition(b'.')[0])
        return int_version

    def get_firefox_version(self):
        """ Returns Firefox version.

        Args:
            None

        Returns:
            Returns an int with the browser version.

        Raises:
            None

        TODO (jonathadv): Add exceptions handling.

        """

        if self.os_name == "Linux":
            output = subprocess.getoutput("firefox -v")
        elif self.os_name == "Windows":
            ff_path = self._find_firefox_exe_in_registry()
            output = self._run_command('"{}" -v | more'.format(ff_path))

        if output is not None:
            out_reg = re.search(self.pattern, output)
            str_version = out_reg.group(0)
            int_version = int(str_version.partition(".")[0])
            return int_version

    @staticmethod
    def _find_firefox_exe_in_registry():
        """ Finds firefox.exe file in Windows systems.

        Args:
            None

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
        command = ""
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
            command: A command line string. For example: "ls -l" and "firefox".

        Returns:
            Returns an string with the command stdout.

        Raises:
            Exception: The command was not found.
            Exception: The command was found but failed.

        TODO (jonathadv): Create specific exceptions.

        """

        try:
            cmd_result = subprocess.run(command.split(), stdout=subprocess.PIPE)

            if cmd_result.returncode == 0:
                return cmd_result.stdout
            else:
                raise Exception("Command \"{}\" failed!".format(command))

        except FileNotFoundError:
            raise Exception("Command \"{}\" not found!".format(command))
