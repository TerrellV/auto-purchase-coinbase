from func.main import event_handler
import pytest
import json


@pytest.fixture
def fake_event():
    return {
        'sandbox_mode': True,
        'order': {
            'amount': 10,
            'product_id': 'btc-usd'
        }
    }


@pytest.fixture
def fake_context():
    return {
        "function_name": "sample-function-name",
        "function_version ": "0.1.1",
        "invoked_function_arn ": 'arn:aws:events:us-east-1:012',
        "memory_limit_in_mb ": "500",
        "aws_request_id ": "id",
        "log_group_name ": "na",
        "log_stream_name ": "na",
        "resources": [
            "arn:aws:events:us-east-1:12:rule/my-schedule"
        ]
    }


def test_event_handler(fake_event, fake_context):

    r = event_handler(fake_event, fake_context)

    assert isinstance(r, dict)
    assert json.dumps(r)
