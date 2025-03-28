import pytest

import domolibrary.client.DomoAuth as dmda
import os


@pytest.mark.asyncio
async def test_domo_auth_token_validation():

    # Create actual instance of DomoTokenAuth
    domo_auth = dmda.DomoTokenAuth(
        domo_access_token=os.environ['DOMO_ACCESS_TOKEN'],
        domo_instance=os.environ['DOMO_INSTANCE'])

    # Test the token validation
    result = await domo_auth.print_is_token(debug_api=True)
    assert result is True
