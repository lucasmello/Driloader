# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=too-few-public-methods

"""
driloader.commands
------------------

Abstraction for all external command calls.
"""


import subprocess


class CommandError(Exception):
    """ Custom exception class for Command """
    pass


class Commands:
    """ A class to abstract all external commands calls.

    The function run() abstracts the complexity of calling
    subprocess.run() in versions >= 3.6  and subprocess.check_output() in versions < 3.6

    """

    @staticmethod
    def run(command):
        """ Run command.
        Runs any command sent as parameter and returns its stdout
        in case of success.
        Args:
            command: Can be a string or string list containing a command line.
            For example: "ls -l" and "firefox" or ['ls', '-l'] and ['firefox']
        Returns:
            Returns an string with the command stdout.
        Raises:
            CommandError: The command was not found.
            CommandError: The command was found but failed.
        """
        if isinstance(command, str):
            command_array = command.split(" ")
        else:
            command_array = command

        try:
            try:
                cmd_result = subprocess.run(command_array, stdout=subprocess.PIPE)
            except AttributeError:
                cmd_result = subprocess.check_output(command_array)

            if (hasattr(cmd_result, "returncode") and cmd_result.returncode == 0) \
                    or cmd_result is not None:
                result = None
                stdout = cmd_result.stdout if hasattr(cmd_result, "stdout") else cmd_result
                if isinstance(stdout, bytes):
                    result = stdout.decode('utf-8')
                else:
                    result = stdout

                return result
            else:
                raise CommandError('Command "{}" failed!'.format(''.join(command)))

        except FileNotFoundError:
            raise CommandError('Command "{}" not found!'.format(''.join(command)))
