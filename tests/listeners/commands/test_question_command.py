
import pytest
from unittest.mock import patch
import domolibrary.client.DomoAuth as dmda

@pytest.mark.asyncio
async def test_domo_auth_token_validation():
    with patch('os.environ', {'DOMO_ACCESS_TOKEN': 'test_token', 'DOMO_INSTANCE': 'test_instance'}):
        # Create actual instance of DomoTokenAuth
        domo_auth = dmda.DomoTokenAuth(
            domo_access_token='test_token',
            domo_instance='test_instance'
        )
        
        # Test the token validation
        result = await domo_auth.print_is_token()
        assert result is True
