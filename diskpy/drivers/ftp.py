from ftplib import FTP as CLIENT, Error


class FTP:
    """ FTP class manage FTP storage.

    Do most needed storage functions like put file, create directory.. eg.
    """
    downloaded = ''
    setting = {
        'base': '/',
        'host': 'website.com',
        'port': '2121',
        'username': 'user',
        'password': 'secret',
    }

    def __init__(self, setting):
        """Init FTP object

        Receive setting from wrapper and set it as attribute.

        Args:
            setting (dict): setting module, if is none will use default setting.

        Returns:
            FTP class object
        """
        # TODO : SFTP
        # TODO : Handling the difference between ascii and binary
        self.setting.update(setting)
        self.client = CLIENT(self.setting.get('host'))
        self.client.login(self.setting.get('username'), self.setting.get('password'))
        self.client.cwd(self.setting.get('base'))

    def put(self, filename, content=None, binary=False):
        """Put file to the storage

        Create file in the storage and put the content on it, Content can be text, file handler or empty.

        Args:
            filename (str): the name of the file to create.
            content (optional[str|file]): the content to put in file.
            binary (optional[boolean]): use binary mode

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.put('filename.txt')
            disk.put('filename.txt', 'some text')
            disk.put('filename.txt', open('file.txt'))
            disk.put('filename.txt', open('img.png'), binary=true)
        """
        if not hasattr(content, 'read'):
            import io
            content = io.BytesIO(content.encode())

        try:
            if binary:
                self.client.storbinary("STOR " + filename, content, len(content))
            else:
                self.client.storlines("STOR " + filename, content)
            return True
        except Error as e:
            print('Put:', e)
            return False

    def get(self, filename, save_to=None, callback=None, binary=False):
        try:
            save_file = open(save_to, 'wb' if binary else 'w') if save_to is not None else None

            def done(content):
                if callable(callback):
                    callback(content)

                if save_file is not None:
                    save_file.write(content)

            if binary:
                self.client.retrbinary("RETR " + filename, done)
            else:
                self.client.retrlines("RETR " + filename, done)

            return True

        except Error as e:
            print('Get:', e)
            return False

    def delete(self, filename):
        try:
            self.client.delete(filename)
            return True
        except Error as e:
            print('Delete:', e)
            return False

    def copy(self, filename, destination, binary=False):
        try:
            def callback(content):
                self.downloaded += content + '\n'

            self.get(filename, callback=callback, binary=binary)
            return self.put(destination, content=self.downloaded, binary=binary)
        except Error as e:
            print('Copy:', e)
            return False

    def move(self, filename, destination):
        try:
            self.client.rename(filename, destination)
            return True
        except Error as e:
            print('Move:', e)
            return False

    def exist(self, filename):
        try:
            self.client.size(filename)
            return True
        except Error as e:
            print('Exist:', e)
            return False

    def permissions(self, filename, chmod=None):
        try:
            if chmod is None:
                # TODO : Get permissions
                return ''
            else:
                self.client.sendcmd('SITE CHMOD ' + str(chmod) + ' ' + filename)
                return True

        except Error as e:
            print('Permissions:', e)
            return False

    def files(self, directory, prefix, suffix):
        files = []

        try:
            if directory is not None:
                self.client.cwd(directory)

            files = [f for f in self.client.nlst() if f != '.' and f != '..']

            if prefix is not None:
                files = [f for f in files if f.name.startswith(prefix)]

            if suffix is not None:
                files = [f for f in files if f.name.endswith(suffix)]

        except Error as e:
            print('Files List:', e)

        finally:
            self.client.cwd(self.setting.get('base'))

        return files

    def make_dir(self, directory):
        try:
            self.client.mkd(directory)
            return True
        except Error as e:
            print('Make Dir:', e)
            return False

    def delete_dir(self, directory):
        # TODO : 550 Can't remove directory: Directory not empty
        try:
            self.client.rmd(directory)
            return True
        except Error as e:
            print('Delete Dir:', e)
            return False
