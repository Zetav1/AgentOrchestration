import pytest
from unittest.mock import patch, MagicMock
from src.sdk.client import OrchestratorClient


class TestOrchestratorClient:
    def setup_method(self):
        self.client = OrchestratorClient(base_url="https://api.test.io", api_key="test-key")

    @patch("src.sdk.client.urlopen")
    def test_register_agent_valid_config(self, mock_urlopen):
        # Mock successful API call
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"status": "success", "agent_id": "123"}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Test with dict
        res = self.client.register_agent("agent-test", "worker.processor", {"key": "val"})
        assert res["status"] == "success"
        assert res["agent_id"] == "123"

        # Test with None (should map to empty dict)
        res = self.client.register_agent("agent-test", "worker.processor", None)
        assert res["status"] == "success"

    def test_register_agent_invalid_config_type(self):
        # Passing string should raise TypeError
        with pytest.raises(TypeError) as excinfo:
            self.client.register_agent("agent-test", "worker.processor", "invalid_string_config")
        assert "must be a dictionary-like object" in str(excinfo.value)

        # Passing list should raise TypeError
        with pytest.raises(TypeError) as excinfo:
            self.client.register_agent("agent-test", "worker.processor", ["invalid", "list"])
        assert "must be a dictionary-like object" in str(excinfo.value)
