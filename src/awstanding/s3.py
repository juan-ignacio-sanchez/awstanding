import boto3

_s3_client = boto3.client('s3')


class Bucket(object):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def download(self, path, to, **boto_args):
        response = _s3_client.get_object(
            Bucket=self.bucket_name,
            Key=path,
            **boto_args
        )
        if response.get('Body'):
            with open(to, 'wb') as destination:
                for line in response.get('Body'):
                    destination.write(line)

    def upload(self, path, to, **boto_args):
        with open(path, 'rb') as source:
            _s3_client.put_object(
                Bucket=self.bucket_name,
                Key=to,
                Body=source,
                **boto_args,
            )