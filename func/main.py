import os
from cbp_client import AuthAPI
from func.secrets_manager import get_secrets


def event_handler(event, context):

    sandbox_mode = event['sandbox_mode']
    purchase_amount = event['order']['amount']
    product_to_purchase = event['order']['product_id']

    all_secrets = get_secrets()
    secrets = (all_secrets.sandbox
               if sandbox_mode
               else all_secrets.live)

    creds = {key: val
             for (key, val) in secrets._asdict().items()
             if key in ['api_key', 'secret', 'passphrase']}

    api = AuthAPI(credentials=creds, sandbox_mode=sandbox_mode)

    r = api.market_buy(
        funds=purchase_amount,
        product_id=product_to_purchase
    )

    return r.json()
