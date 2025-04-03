"""
This module provides authentication for interacting with Domo APIs.

It initializes a `DomoTokenAuth` object using environment variables for the
Domo access token and instance.
"""

import domolibrary.client.DomoAuth as dmda
import os

domo_auth = dmda.DomoTokenAuth(
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    domo_instance=os.environ["DOMO_INSTANCE"],
)
