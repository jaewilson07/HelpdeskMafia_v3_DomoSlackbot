import domolibrary.client.DomoAuth as dmda
import os
import asyncio

domo_auth = dmda.DomoTokenAuth(
    domo_access_token=os.environ['DOMO_ACCESS_TOKEN'],
    domo_instance=os.environ['DOMO_INSTANCE'])

if __name__ == "__main__":
  asyncio.run(domo_auth.print_is_token(debug_api=True))
