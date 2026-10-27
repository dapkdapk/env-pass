import json
import os
import subprocess
import tempfile
from unittest.mock import patch, MagicMock

import pytest

from app.main import main, getKeys, _clr


def test_clr_with_query_string():
    """Test _clr function removes query string."""
    url_with_query = "abc123?query=param"
    result = _clr(url_with_query)
    assert result == "abc123"


def test_clr_without_query_string():
    """Test _clr function without query string."""
    url_without_query = "abc123"
    result = _clr(url_without_query)
    assert result == "abc123"


def test_get_keys_simple():
    """Test getKeys function with simple dictionary."""
    obj = {
        "level1": {
            "level2": {
                "value": "test"
            }
        }
        }
    result = getKeys(obj)
    expected_key = "level1.level2.value"
    assert expected_key in result
    assert result[expected_key] == "test"


def test_get_keys_with_list():
    """Test getKeys function with list containing dictionaries."""
    obj = {
        "item": {
            "content": {
                "extra_fields": [
                    {
                        "name": "TEST_FIELD",
                        "content": {
                            "Text": "test_value"
                        }
                    }
                ]
            }
        }
    }
    result = getKeys(obj)
    # Check if the special handling for lists with name/content works
    assert "item.content.extra_fields[].TEST_FIELD" in result
    assert result["item.content.extra_fields[].TEST_FIELD"] == "test_value"


@patch('app.main.subprocess')
def test_main_no_login(mock_subprocess):
    """Test main function when not logged in."""
    # Mock subprocess responses - empty output means not logged in
    mock_info_process = MagicMock()
    mock_info_process.communicate.return_value = (b'', None)
    mock_subprocess.Popen.return_value = mock_info_process
    
    # Call main with test arguments
    test_args = [
        '--proton-pass-uri', 
        'moz-extension://test/share/S123/item/I456'
    ]
    
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(main, test_args)
    
    # Should exit with code 1 when not logged in
    assert result.exit_code == 1
    assert "pass-cli login not available" in result.output


@patch('app.main.subprocess')
def test_main_with_show_json_paths(mock_subprocess):
    """Test main function with show-json-paths flag."""
    # Mock subprocess responses
    mock_info_process = MagicMock()
    mock_info_process.communicate.return_value = (b'{"username": "test"}', None)
    
    mock_view_process = MagicMock()
    mock_view_process.communicate.return_value = (b'{"item":{"login":{"password":"test"}}}', None)
    
    # Configure subprocess.Popen to return different mocks based on the command
    def side_effect(cmd, **kwargs):
        if 'info' in cmd:
            return mock_info_process
        elif 'view' in cmd:
            return mock_view_process
        return MagicMock()
        
    mock_subprocess.Popen.side_effect = side_effect
    
    # Call main with show-json-paths flag
    test_args = [
        '--proton-pass-uri', 
        'moz-extension://test/share/S123/item/I456',
        '--show-json-paths'
    ]
    
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(main, test_args)
    
    # Should exit with code 1 when showing JSON paths
    assert result.exit_code == 1


def test_template_constants():
    """Test that template constants exist and are strings."""
    from app.main import TMPL_ENV_FILE, TMPL_EXPORT_ITEM, TMPL_EXPORT_ITEM_LIST
    assert isinstance(TMPL_ENV_FILE, str)
    assert isinstance(TMPL_EXPORT_ITEM, str)
    assert isinstance(TMPL_EXPORT_ITEM_LIST, str)
    assert len(TMPL_ENV_FILE) > 0
    assert len(TMPL_EXPORT_ITEM) > 0
    assert len(TMPL_EXPORT_ITEM_LIST) > 0


if __name__ == '__main__':
    pytest.main([__file__])