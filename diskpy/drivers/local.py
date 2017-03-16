import os


class Local:
    """ Local class manage local filesystem

    Do most needed storage functions like put file, create directory.. eg.
    """
    setting = {
        'base': 'files'
    }

    def __init__(self, setting):
        """Init Local object

        Receive setting from wrapper and set it as attribute.

        Args:
            setting (dict): Name of disk in setting module, if is none will use default setting.

        Returns:
            Local class object
        """
        self.setting.update(setting)

    def put(self, filename, content=None):
        """Put file to the storage

        Create file in the storage and put the content on it, Content can be text, file handler or empty.

        Args:
            filename (str): the name of the file to create.
            content (optional[str|file]): the content to put in file.

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.put('filename.txt')
            disk.put('filename.txt', 'some text')
            disk.put('filename.txt', open('file.txt'))
        """
        try:
            with open(self.__base(filename), 'w') as f:
                if content is not None:
                    if hasattr(content, 'read'):
                        content = content.read()

                    f.write(content)
                f.close()
            return True
        except OSError as e:
            print('Put:', e)

        return False

    def get(self, filename, save_to=None):
        """Get file from the storage

        Return the content of the file.

        Args:
            filename (str): the name of the file to get.
            save_to (optional[str]): file path to save copy of the file there.

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.get('filename.txt')
            disk.get('filename.txt', save_to='path/to/file.txt')
        """
        try:
            with open(self.__base(filename)) as file:
                if save_to is not None:
                    with open(save_to, 'w') as f:
                        f.write(file.read())
                        f.close()

                return file.read()
        except OSError as e:
            print('Get:', e)

        return False

    def delete(self, filename):
        """Delete file from the storage

        Return the content of the file.

        Args:
            filename (str): the name of the file to delete.

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.delete('filename.txt')
        """
        try:
            os.remove(self.__base(filename))
            return True
        except OSError as e:
            print('Delete:', e)
            return False

    def copy(self, filename, destination):
        """Copy file from the storage

        Return the content of the file.

        Args:
            filename (str): the name of the file to copy.
            destination (str): the name of the new file.

        Returns:
            bool: True if successful, False otherwise.

        Examples:
             ``disk.copy('filename.txt', 'copy_of_filename.txt')``
        """
        try:
            with open(self.__base(filename)) as f:
                self.put(destination, f.read())
                f.close()
                return True
        except OSError as e:
            print('Copy:', e)

        return False

    def move(self, filename, destination):
        """Move file from the storage

        Return the content of the file.

        Args:
            filename (str): the name of the file to copy.
            destination (str): the name of the new file.

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.move('filename.txt', 'move/file/here.txt')
        """
        try:
            os.rename(self.__base(filename), self.__base(destination))
            return True
        except OSError as e:
            print('Move:', e)
            return False

    def exist(self, filename):
        """File exist

        Check if file exist in storage.

        Args:
            filename (str): the name of the file to copy.

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.exist('filename.txt')
        """
        return os.path.exists(self.__base(filename))

    def permissions(self, filename, chmod=None):
        """File Permissions

        Get file permissions or set new permissions.

        Args:
            filename (str): the name of the file to copy.
            chmod (optional[int]): the name of the file to copy.

        Returns:
            str: if successful get the permissions
            bool: True if successful set new permissions, False otherwise.

        Examples:
            # Get permissions
            disk.permissions('filename.txt')
            # Set permissions
            disk.permissions('filename.txt', chmod=777)
        """
        filename = self.__base(filename)
        try:
            if chmod is None:
                # Get the file's permissions
                return str(oct(os.stat(filename).st_mode)[5:])
            else:
                # Set new permissions to the file
                os.chmod(filename, int(str(chmod), 8))
                return True
        except OSError as e:
            print('Permissions:', e)

        return False

    def files(self, directory=None, prefix=None, suffix=None):
        """Files List

        Get all files inside the selected folder

        Args:
            directory (optional[str]): the folder to look in it.
            prefix (optional[str]): a str files names start with.
            suffix (optional[str]): a str files names ends with.

        Returns:
            list: a list of folder's files.

        Examples:
            # Root folder
            disk.files()

            # Sub folder
            disk.files('sub_folder')

            # Filters
            disk.files('sub_folder', prefix='log', suffix='.txt')
        """
        directory = '.' if directory is None else directory
        directory = self.__base(directory)

        files = []

        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(directory + '/' + f)]

            if prefix is not None:
                files = [f for f in files if f.startswith(prefix)]

            if suffix is not None:
                files = [f for f in files if f.endswith(suffix)]
        except OSError as e:
            print('Files:', e)

        return files

    def dirs(self, directory=None, prefix=None, suffix=None):
        """Directories List

        Get all Directories inside the selected folder

        Args:
            directory (optional[str]): the folder to look in it.
            prefix (optional[str]): a str directories names start with.
            suffix (optional[str]): a str directories names ends with.

        Returns:
            list: a list of folder's directories.

        Examples:
            # Root folder
            disk.directories()

            # Sub folder
            disk.directories('sub_folder')

            # Filters
            disk.dirs('sub_folder', prefix='imgs', suffix='text')
        """
        directory = '.' if directory is None else directory
        directory = self.__base(directory)

        dirs = []

        try:
            dirs = [d for d in os.listdir(directory) if os.path.isdir(directory + '/' + d)]

            if prefix is not None:
                dirs = [d for d in dirs if d.startswith(prefix)]

            if suffix is not None:
                dirs = [d for d in dirs if d.endswith(suffix)]
        except OSError as e:
            print('Dirs:', e)

        return dirs

    def make_dir(self, directory):
        """Make New Directory

        Create new directory inside root folder or sub folder.

        Args:
            directory (str): the folder to create in it.

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.make_dir('new_dir')
        """
        try:
            directory = self.__base(directory)
            if not os.path.exists(directory):
                os.makedirs(directory)
            return True
        except OSError as e:
            print('Create Directory:', e)

        return False

    def delete_dir(self, directory):
        """Delete Directory

        Delete old directory from root folder or sub folder.

        Args:
            directory (str): the folder to create in it.

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            disk.make_dir('old_dir/sub')
            disk.make_dir('old_dir')
        """
        try:
            directory = self.__base(directory)

            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            os.rmdir(directory)

            return True
        except OSError as e:
            print('Delete Directory:', e)
            return False

    def __base(self, filename):
        """Set Full Path

        Attache base path to filename

        Args:
            filename (str): the folder to create in it.

        Returns:
            str: Full path to the file.

        Examples:
            disk.__base('old_dir/sub')
        """
        base = self.setting.get('base')

        if isinstance(base, str):
            return base + '/' + filename
