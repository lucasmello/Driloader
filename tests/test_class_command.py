import pytest
import pytest_mock
from driloader.commands import Commands, CommandError

def test_commands_call_to_subprocess_check_output(mocker):
    mocker.patch('subprocess.check_output', return_value=b'49')
    cmd = 'google-chrome --product-version'
    output = Commands.run(cmd)
    assert output == '49'

def test_commands_call_to_subprocess_run(mocker):
    mocker.patch('subprocess.run', return_value=None, create=True)
    with pytest.raises(CommandError):
        Commands.run('not_existing_command')

