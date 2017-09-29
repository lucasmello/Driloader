import pytest
import pytest_mock

from driloader.commands import CommandError, Commands


def test_commands_call_to_subprocess_check_output_with_a_valid_command(mocker):
    mocker.patch('subprocess.check_output', return_value=b'cmd_output')
    output = Commands.run("a_valid_command")
    assert output == 'cmd_output'

def test_raises_exception_on_running_non_existing_command_with_check_output(mocker):
    mocker.patch('subprocess.check_output', return_value=None)
    with pytest.raises(CommandError):
        Commands.run('not_existing_command')

def test_raises_exception_on_running_non_existing_command_with_run(mocker):
    mocker.patch('subprocess.run', return_value=None, create=True)
    with pytest.raises(CommandError):
        Commands.run('not_existing_command')
