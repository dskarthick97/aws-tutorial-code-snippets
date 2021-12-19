"""
Stub functions that are used by the Amazon S3 unit tests.

When tests are run against an actual AWS account, the stubber class does not
set up stubs and passes all calls through to the Boto3 client.
"""

import io
import json
from botocore.stub import ANY

from base_stubber import BaseStubber


class S3Stubber(BaseStubber):
    """
    A class that implements a variety of stub functions that are used by the
    Amazon S3 unit tests.

    The stubbed functions all expect certain parameters to be passed to them as
    part of the tests, and will raise errors when the actual parameters differ from
    the expected.
    """

    def __init__(self, client, use_stubs=True):
        """
        Initializes the object with a specific client and configures it for
        stubbing or AWS passthrough.

        :param client: A Boto3 S3 client.
        :param use_stubs: When True, use stubs to intercept requests. Otherwise,
            pass requests through to AWS.
        """
        super().__init__(client, use_stubs)

    def stub_get_object(
        self,
        bucket_name,
        object_key,
        object_data=None,
        version_id=None,
        error_code=None,
    ):
        """Stub the get_object function. When the object data is a string,
        treat it as a file name, open the file, and read it as bytes."""

        expected_params = {"Bucket": bucket_name, "Key": object_key}
        if object_data:
            if isinstance(object_data, bytes):
                data = object_data
            else:
                with open(object_data, "rb") as file:
                    data = file.read()
            response = {"Body": io.BytesIO(data)}
        else:
            response = {}
        if version_id:
            response["VersionId"] = version_id

        self._stub_bifurcator(
            "get_object",
            expected_params=expected_params,
            response=response,
            error_code=error_code,
        )
