import json
from unittest.mock import MagicMock, patch

import pytest

from app.libs.env_pass_cls import EnvPass


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
    proton_pass_uri, share_id, item_id = EnvPass.GetSettings(proton_pass_uri=uri)

    assert share_id == "abc123"
    assert item_id == "def456"


def test_get_settings_with_params():
    """Test GetSettings method with direct parameters."""
    proton_pass_uri, share_id, item_id = EnvPass.GetSettings(
        proton_pass_share_id="abc123", proton_pass_item_id="def456"
    )

    assert share_id == "abc123"
    assert item_id == "def456"


@patch("jmespath.search")
def test_get_keys_simple_dict(mock_jmespath_search):
    """Test _GetKeys method with a simple dictionary."""
    # Mock jmespath.search to return string values
    mock_jmespath_search.side_effect = lambda path, obj: (
        path.split(".")[-1] if isinstance(path.split(".")[-1], str) else None
    )

    obj = {"key1": "value1", "key2": "value2"}

    result = EnvPass._GetKeys(obj)

    # Should contain the keys with their values
    assert "key1" in result
    assert "key2" in result


def test_get_env_file_script():
    """Test GetEnvFileScript generates correct script."""
    env_names = {"simple.key": "SIMPLE_VAR", "nested.object.key": "NESTED_VAR"}
    share_id = "test_share"
    item_id = "test_item"

    result = EnvPass.GetEnvFileScript(env_names, share_id, item_id)

    # Check that the result contains expected elements
    assert share_id in result
    assert item_id in result
    assert "SIMPLE_VAR" in result
    assert "NESTED_VAR" in result


if __name__ == "__main__":
    pytest.main([__file__])
