"""
AWS resource stubbing using botocore stub module
"""
# pylint: disable=import-error

from datetime import datetime

import boto3
from botocore.stub import Stubber, ANY

s3_client = boto3.client("s3")

list_buckets_stub_response = {
    "Buckets": [
        {
            "Name": "webface-preprod-assets",
            "CreationDate": datetime.now(),
        },
        {
            "Name": "webface-dev-assets",
            "CreationDate": datetime.now(),
        },
        {
            "Name": "webface-qa-assets",
            "CreationDate": datetime.now(),
        },
    ],
    "Owner": {
        "DisplayName": "Thanos",
        "ID": "1234567890",
    },
}

list_objects_v2_stub_response = {
    "IsTruncated": False,
    "Contents": [
        {
            "Key": "careers/image_name.format",
            "LastModified": datetime.now(),
            "ETag": "df203d64b094966f0e7a49d21ac25169",
            "Size": 202736,
            "StorageClass": "STANDARD",
        },
        {
            "Key": "careers/image_name.format",
            "LastModified": datetime.now(),
            "ETag": "df203d64b094966f0e7a49d21ac25169",
            "Size": 202736,
            "StorageClass": "STANDARD",
        },
    ],
    "Name": "webface-dev-assets",
    "Prefix": "careers",
    "MaxKeys": 1000,
    "EncodingType": "url",
    "KeyCount": 2,
}

with Stubber(s3_client) as s3_stubber:
    s3_stubber.add_response("list_buckets", list_buckets_stub_response, {})
    list_buckets_res = s3_client.list_buckets()

    expected_list_objects_v2_params = {"Bucket": ANY, "Prefix": ANY}
    s3_stubber.add_response(
        "list_objects_v2",
        list_objects_v2_stub_response,
        expected_list_objects_v2_params,
    )
    list_objects_v2_res = s3_client.list_objects_v2(
        Bucket="webface-dev-assets", Prefix="careers"
    )

    s3_stubber.assert_no_pending_responses()


print(f"List buckets response: {list_buckets_res}")
assert list_buckets_res == list_buckets_stub_response

print("")

print(f"List Objects response: {list_objects_v2_res}")
assert list_objects_v2_res == list_objects_v2_stub_response
