from diskpy.drivers import *

setting = {
    'default': 'disk_1',

    # Local driver setting
    'disk_1': {
        'driver': Local,
        'base': 'upload',
    },

    # S3 driver setting
    'disk_2': {
        'driver': S3,
        'bucket': 'bucket_name',
        'region': 'region_name',
        'access_key': 'your_access_key',
        'secret_key': 'your_secret_key'
    },

    # FTP driver setting
    'disk_3': {
        'driver': FTP,
        'base': '/www',
        'host': 'website.com',
        'port': '2121',
        'username': 'owner',
        'password': 'secret',
    },

    # Dropbox driver setting
    'disk_4': {
        'driver': Dropbox,
        'base': '/folder',
        'access_token': 'your_access_token'
    }
}