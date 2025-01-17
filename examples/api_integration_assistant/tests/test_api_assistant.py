import pytest
import asyncio
from api_assistant import APIIntegrationAssistant, APIInfo, APIEndpoint
from unittest.mock import patch, MagicMock

@pytest.fixture
def api_assistant():
    return APIIntegrationAssistant("test-api-key")

@pytest.mark.asyncio
async def test_discover_api(api_assistant):
    mock_response = {
        'extract': {
            'endpoints': [
                {
                    'path': '/v1/users',
                    'method': 'GET',
                    'auth_required': True,
                    'rate_limit': '100/hour'
                }
            ],
            'auth_method': 'Bearer Token',
            'base_url': 'https://api.example.com'
        }
    }
    
    with patch.object(api_assistant.app, 'scrapeUrl', return_value=mock_response):
        result = await api_assistant.discover_api("https://api.example.com/docs")
        assert isinstance(result, APIInfo)
        assert len(result.endpoints) == 1
        assert result.auth_method == "Bearer Token"

@pytest.mark.asyncio
async def test_monitor_api(api_assistant):
    url = "https://api.example.com"
    
    # Start monitoring
    await api_assistant.monitor_api(url)
    assert url in api_assistant.monitoring
    assert api_assistant.monitoring[url]['status'] == 'active'
    
    # Get stats
    stats = api_assistant.get_monitoring_stats(url)
    assert 'last_check' in stats
    assert 'average_response_time' in stats
    
    # Stop monitoring
    await api_assistant.stop_monitoring(url)
    assert api_assistant.monitoring[url]['status'] == 'stopped'

@pytest.mark.asyncio
async def test_error_handling(api_assistant):
    with pytest.raises(ValueError):
        api_assistant.get_monitoring_stats("nonexistent-url")