import json
from unittest.mock import MagicMock, patch

import pytest

from app_env_pass.libs.env_pass_cls import EnvPass
from app_env_pass.libs.proton_pass.env_proton_pass_cls import EnvProtonPass


def test_clear_string():
    """Test the _ClearString method removes query parameters correctly."""
    # Test with query parameters
    result = EnvPass._ClearString("abc123?query=param")
    assert result == "abc123"

    # Test without query parameters
    result = EnvPass._ClearString("abc123")
    assert result == "abc123"


def test_get_settings_with_uri():
    """Test GetSettings method with URI parameter."""
    uri = "https://example.com/share/abc123/item/def456?query=param"
    proton_pass_uri, share_id, item_id = EnvProtonPass.GetSettings(proton_pass_uri=uri)

    assert share_id == "abc123"
    assert item_id == "def456"


def test_get_settings_with_params():
    """Test GetSettings method with direct parameters."""
    proton_pass_uri, share_id, item_id = EnvProtonPass.GetSettings(
        proton_pass_share_id="abc123", proton_pass_item_id="def456"
    )

    assert share_id == "abc123"
    assert item_id == "def456"


@patch("jmespath.search")
@patch("app_env_pass.libs.env_pass_cls.EnvPass._GetKeys")
def test_get_env_names(mock_get_keys, mock_jmespath_search):
    """Test GetEnvNames method."""
    # Mock the subprocess call and jmespath search
    mock_get_keys.return_value = {"simple.key": "value1", "nested.object.key": "value2"}

    # Mock subprocess.Popen
    with patch("subprocess.Popen") as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b'{"dummy": "data"}', None)
        mock_popen.return_value = mock_process

        # Mock inquirer.prompt to return predefined values
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.side_effect = [
                {"values": ["simple.key = value1", "nested.object.key = value2"]},
                {"simple.key": "SIMPLE_VAR", "nested.object.key": "NESTED_VAR"},
            ]

            # Call the method
            result = EnvProtonPass.GetEnvNames("test_share", "test_item", None)

            # Assertions
            assert "SIMPLE_VAR" in result.values()
            assert "NESTED_VAR" in result.values()


def test_get_env_file_script():
    """Test GetEnvFileScript generates correct script."""
    env_names = {"simple.key": "SIMPLE_VAR", "nested.object.key": "NESTED_VAR"}
    share_id = "test_share"
    item_id = "test_item"

    result = EnvProtonPass.GetEnvFileScript(env_names, share_id, item_id)

    # Check that the result contains expected elements
    assert share_id in result
    assert item_id in result
    assert "SIMPLE_VAR" in result
    assert "NESTED_VAR" in result


@patch("subprocess.Popen")
def test_is_pass_cli_logged_in(mock_popen):
    """Test IsPassCLILogged method when logged in."""
    # Mock subprocess to simulate successful login
    mock_process = MagicMock()
    mock_process.communicate.return_value = (b'{"username": "test_user"}', None)
    mock_popen.return_value = mock_process

    result = EnvProtonPass.IsPassCLILogged()
    assert result is True


@patch("subprocess.Popen")
def test_is_pass_cli_logged_out(mock_popen):
    """Test IsPassCLILogged method when logged out."""
    # Mock subprocess to simulate no login
    mock_process = MagicMock()
    mock_process.communicate.return_value = (b"", None)
    mock_popen.return_value = mock_process

    result = EnvProtonPass.IsPassCLILogged()
    assert result is False


if __name__ == "__main__":
    pytest.main([__file__])
