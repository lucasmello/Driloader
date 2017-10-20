# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Disabling the below pylint warnings in order to use long names convention in the tests
# and because some entities are used seamlessly instead of being directly called.

# pylint: disable=invalid-name
# pylint: disable=unused-import


"""
tests.test_class_commands
------------------

The test set for functions in driloader.commands.Commands
"""


import pytest
import pytest_mock

from driloader.commands import CommandError, Commands


class TestCommands:
    """ Test Commands by mocking the subprocess calls """

    @staticmethod
    def test_call_subprocess_check_output_with_a_valid_command(mocker):
        """Test calls like subprocess.check_ouput('valiad_command') """

        mocker.patch('subprocess.check_output', return_value=b'cmd_output')
        output = Commands.run("a_valid_command")
        assert output == 'cmd_output'

    @staticmethod
    def test_raises_exception_on_running_non_existing_command_with_check_output(mocker):
        """Test calls like subprocess.check_ouput('invaliad_command')
           where the CommandError exception should be thrown.
        """

        mocker.patch('subprocess.check_output', return_value=None)
        with pytest.raises(CommandError):
            Commands.run('not_existing_command')

    @staticmethod
    def test_raises_exception_on_running_non_existing_command_with_run(mocker):
        """Test calls like subprocess.run('invaliad_command')
           where the CommandError exception should be thrown.

           For versions < 3.6, the subprocess,run function doesn't exists, so
           the mock creates this function by using `create=True`.
        """

        mocker.patch('subprocess.run', return_value=None, create=True)
        with pytest.raises(CommandError):
            Commands.run('not_existing_command')
