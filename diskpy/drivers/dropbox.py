from dropbox import Dropbox as Box
from dropbox.files import WriteMode, FolderMetadata
from dropbox.exceptions import *


class Dropbox:
    """ Dropbox class manage Dropbox storage

    Do most needed storage functions like put file, create directory.. eg.
    """
    setting = {
        'base': '/',
        'access_token': 'your_access_token'
    }

    def __init__(self, setting):
        """Init Dropbox object

        Receive setting from wrapper and set it as attribute.

        Args:
            setting (dict): base and access token in setting module, if is none will use default setting.

        Returns:
            Dropbox class object
        """
        self.setting.update(setting)
        self.base = (self.setting.get('base') + '/').lower()
        self.client = Box(self.setting.get('access_token'))
        self.client.users_get_current_account()

    def put(self, filename, content=None, overwrite=True):
        """Put file to the storage

        Create file in the storage and put the content on it, Content can be text, file handler or empty.

        Args:
            filename (str): the name of the file to create.
            content (optional[str|file]): the content to put in file.
            overwrite (optional[boolean]): overwrite if exist

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.put('filename.txt')
            disk.put('filename.txt', 'some text')
            disk.put('filename.txt', open('file.txt'))
            disk.put('filename.txt', open('file.txt'), overwrite=true)
        """
        if content is None:
            content = ''

        mode = WriteMode.overwrite if overwrite else WriteMode.add

        try:
            self.client.files_upload(content, self.base + filename, mode=mode)
            return True
        except ApiError:
            return False

    def get(self, filename, save_to=None):
        try:
            md, res = self.client.files_download(self.base + filename)

            if save_to is not None:
                with open(save_to, 'wb') as f:
                    f.write(res.content)
                    f.close()

            return res.content
        except ApiError:
            return False

    def delete(self, filename):
        try:
            self.client.files_delete(self.base + filename)
            return True
        except ApiError:
            return False

    def copy(self, filename, destination):
        try:
            self.client.files_copy(self.base + filename, self.base + destination)
            return True
        except ApiError:
            return False

    def move(self, filename, destination):
        try:
            self.client.files_move(self.base + filename, self.base + destination)
            return True
        except ApiError:
            return False

    def exist(self, filename):
        try:
            self.client.files_get_metadata(self.base + filename)
            return True
        except ApiError:
            return False

    def files(self, directory=None, prefix=None, suffix=None):
        directory = self.base[:-1] if directory is None else self.base + directory
        files = []
        try:
            files = [e for e in self.client.files_list_folder(directory).entries if not isinstance(e, FolderMetadata)]

            if prefix is not None:
                files = [f for f in files if f.name.startswith(prefix)]

            if suffix is not None:
                files = [f for f in files if f.name.endswith(suffix)]

        except ApiError:
            pass

        return files

    def dirs(self, directory=None, prefix=None, suffix=None):

        directory = self.base[:-1] if directory is None else self.base + directory
        files = []

        try:
            files = [e for e in self.client.files_list_folder(directory).entries if isinstance(e, FolderMetadata)]

            if prefix is not None:
                files = [f for f in files if f.name.startswith(prefix)]

            if suffix is not None:
                files = [f for f in files if f.name.endswith(suffix)]
        except ApiError:
            pass

        return files

    def make_dir(self, directory):
        try:
            self.client.files_create_folder(self.base + directory)
            return True
        except ApiError:
            return False

    def delete_dir(self, directory):
        return self.delete(directory)


