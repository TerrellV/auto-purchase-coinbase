import os
from cbp_client import AuthAPI
from func.secrets_manager import secrets


def event_handler(event, context):

    sandbox_mode = event['sandbox_mode']
    purchase_amount = event['order']['amount']
    product_to_purchase = event['order']['product_id']

    s = secrets()
    creds = s.sandbox._asdict() if sandbox_mode else s.live._asdict()

    api = AuthAPI(credentials=creds, sandbox_mode=sandbox_mode)

    r = api.market_buy(
        funds=purchase_amount,
        product_id=product_to_purchase
    )

    return r.json()
