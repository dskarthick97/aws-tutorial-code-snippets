
import boto3
from botocore import exceptions

session = boto3.Session(profile_name='karthick-learner')
s3_client = session.client('s3')


class AssetMigration:

    def __init__(self, bucket, prefix=''):
        self._bucket = bucket
        self.prefix = prefix

    @property
    def bucket(self):
        return self._bucket

    def _list_objects(self, delimiter=''):
        """
        Lists out all the objects in a bucket.

        :param delimiter string: character used to group keys.
            Ex. '/' - will fetch the objects which has no '/'.
        :return objects list: list of objects.
        """
        return s3_client.list_objects_v2(
            Bucket=self.bucket, Prefix=self.prefix, Delimiter=delimiter)

    def get_keys(self, exclude_folders=False):
        """
        Extract the keys from the _list_objects response.

        :param exclude_folders boolean: both files and folders are fetched
            by default.
        :return assets_key generator: list of assets keys
        """
        if exclude_folders:
            res = self._list_objects('/')
        else:
            res = self._list_objects()

        contents = res.get('Contents')
        assets_key =  [content.get('Key') for content in contents \
            if (content.get('Size') > 0)]

        return assets_key
