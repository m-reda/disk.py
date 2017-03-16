import os
from importlib import import_module


class SettingException(Exception):
    pass


class Disk:
    """Disk Class

    The wrapper for Local, S3, Dropbox and FTP.
    Passing data to driver and return respond"""
    setting = {}
    driver = None

    def __init__(self, disk=None, **kwargs):
        """Init disk object

        Load setting module, call driver module and pass setting.

        Args:
            disk (str): Name of disk in setting module, if is none will use default disk.
            **kwargs: Additional args will pass to driver

        Returns:
            Disk class object

        Raises:
            SettingException: Setting module not found or Driver not found.
        """
        setting_module = os.environ.get('DISKPY_SETTING')
        if setting_module is not None:
            self.setting = import_module(setting_module + '').STORAGE
            disk = self.setting.get('default') if disk is None else disk
            setting = self.setting.get(disk)

            if setting is not None:
                driver = setting.get('driver')

                if callable(driver):
                    self.driver = driver(setting, **kwargs)

            if self.driver is None:
                raise SettingException('Driver not found.')

        else:
            raise SettingException('Setting module not found.')

    def put(self, filename, content=None, **kwargs):
        return self.__call('put', filename, content, **kwargs)

    def get(self, filename, save_to=None, **kwargs):
        return self.__call('get', filename, save_to, **kwargs)

    def delete(self, filename, **kwargs):
        return self.__call('delete', filename, **kwargs)

    def copy(self, filename, destination, **kwargs):
        return self.__call('copy', filename, destination, **kwargs)

    def move(self, filename, destination, **kwargs):
        return self.__call('move', filename, destination, **kwargs)

    def exist(self, filename, **kwargs):
        return self.__call('exist', filename, **kwargs)

    def permissions(self, filename, **kwargs):
        return self.__call('permissions', filename, **kwargs)

    def files(self, directory=None, prefix=None, suffix=None, **kwargs):
        return self.__call('files', directory, prefix, suffix, **kwargs)

    def dirs(self, directory=None, prefix=None, suffix=None, **kwargs):
        return self.__call('dirs', directory, prefix, suffix, **kwargs)

    def make_dir(self, directory):
        return self.__call('make_dir', directory)

    def delete_dir(self, directory):
        return self.__call('delete_dir', directory)

    def __call(self, method, *args, **kwargs):
        if hasattr(self.driver, method):
            return getattr(self.driver, method)(*args, **kwargs)
        else:
            return False

