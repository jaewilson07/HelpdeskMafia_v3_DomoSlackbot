
import pytest
from unittest.mock import Mock, patch
import domolibrary.client.DomoAuth as dmda
from listeners.commands.question_command import trigger_domo_llms_workflow

@pytest.mark.asyncio
async def test_domo_auth_token_validation():
    # Mock DomoAuth instance
    mock_domo_auth = Mock(spec=dmda.DomoAuth)
    mock_domo_auth.print_is_token.return_value = True
    
    with patch('domolibrary.client.DomoAuth.DomoAuth') as mock_auth_class:
        mock_auth_class.return_value = mock_domo_auth
        
       
        # Execute the function
        with patch('os.environ', {'DOMO_ACCESS_TOKEN': 'test_token', 'DOMO_INSTANCE': 'test_instance'}):
            await trigger_domo_llms_workflow(**test_params)
            
        # Verify the token validation was called
        mock_domo_auth.print_is_token.assert_called_once()
