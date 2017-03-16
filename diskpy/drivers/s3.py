from boto3 import client
from botocore.exceptions import ClientError

# ACL='private'|'public-read'|'public-read-write'|'authenticated-read'|'aws-exec-read'


class S3:
    """ S3 class manage S3 storage.

    Do most needed storage functions like put file, create directory.. eg.
    """
    setting = {
        'bucket': 'bucket_name',
        'region': 'region_name',
        'access_key': 'your_access_key',
        'secret_key': 'your_secret_key'
    }

    def __init__(self, setting, bucket=None):
        """Init S3 object

        Receive setting from wrapper and set it as attribute.

        Args:
            setting (dict): setting module, if is none will use default disk.
            bucket (optional[str]): bucket name if is none will use default setting.

        Returns:
            S3 class object
        """
        self.setting.update(setting)
        self.client = client(
            's3',
            region_name=self.setting.get('region'),
            aws_access_key_id=self.setting.get('access_key'),
            aws_secret_access_key=self.setting.get('secret_key'),
        )

        self.bucket_name = self.setting.get('bucket') if bucket is None else bucket

    def put(self, filename, content=None, acl='private', **kwargs):
        """Put file to the storage

        Create file in the storage and put the content on it, Content can be text, file handler or empty.

        Args:
            filename (str): the name of the file to create.
            content (optional[str|file]): the content to put in file.
            acl (optional[str]): can be private, public-read, public-read-write, authenticated-read, aws-exec-read
            **kwargs

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.put('filename.txt')
            disk.put('filename.txt', 'some text')
            disk.put('filename.txt', open('file.txt'))
            disk.put('filename.txt', open('img.png'), acl='public-read')
        """
        content = '' if content is None else content
        content = content.read() if hasattr(content, 'read') else content

        try:
            self.client.put_object(Bucket=self.bucket_name, Key=filename, Body=content, ACL=acl, **kwargs)
            return True
        except ClientError:
            return False

    def get(self, filename, save_to=None, **kwargs):
        try:
            file = self.client.get_object(Bucket=self.bucket_name, Key=filename, **kwargs)['Body'].read()

            if save_to is not None:
                with open(save_to, 'wb') as f:
                    f.write(file)
                    f.close()

            return file
        except ClientError:
            return False

    def delete(self, filename, **kwargs):
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=filename, **kwargs)
            return True
        except ClientError:
            return False

    def copy(self, filename, destination, acl='private', **kwargs):
        try:
            self.client.copy_object(Bucket=self.bucket_name, Key=destination, ACL=acl,
                                    CopySource={'Bucket': self.bucket_name, 'Key': filename}, **kwargs)
            return True
        except ClientError:
            return False

    def move(self, filename, destination, acl='private'):
        try:
            if self.copy(filename, destination, acl=acl):
                self.delete(filename)
                return True
        except ClientError:
            pass

        return False

    def exist(self, filename, **kwargs):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=filename, **kwargs)
            return True
        except ClientError:
            return False

    def permissions(self, filename, acl=None, **kwargs):
        try:
            if acl is None:
                request = self.client.get_object_acl(Bucket=self.bucket_name, Key=filename, **kwargs)
                return request['Grants'] if 'Grants' in request else False
            else:
                self.client.put_object_acl(Bucket=self.bucket_name, Key=filename, ACL=acl, **kwargs)

            return True
        except ClientError:
            return False

    def files(self, directory=None, prefix=None, suffix=None, **kwargs):
        directory = '' if directory is None else directory
        prefix = directory if prefix is None else directory + '/' + prefix

        files = []

        try:
            request = self.client.list_objects(Bucket=self.bucket_name, Prefix=prefix, **kwargs)

            if 'Contents' in request:
                for f in request['Contents']:
                    key = f.get('Key')

                    if not key.endswith('/') and (suffix is None or key.endswith(suffix)):
                        files.append(key)
        except ClientError:
            pass

        return files

    def dirs(self, directory, prefix=None, suffix=None, **kwargs):
        directory = '' if directory is None else directory + '/'
        prefix = directory if prefix is None else directory + prefix

        dirs = []

        try:
            request = self.client.list_objects(Bucket=self.bucket_name, Prefix=prefix, Delimiter='/', **kwargs)

            if 'CommonPrefixes' in request:
                request = request['CommonPrefixes']
                for d in request:
                    key = d.get('Prefix')

                    if suffix is None or key.endswith(suffix):
                        dirs.append(key)
        except ClientError:
            pass

        return dirs


