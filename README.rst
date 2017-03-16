disk.py 
=======
``Weekend Project - WIP``

Python module to manage files and directories from **Local** File System, **S3**, **Dropbox** and **FTP**.

.. contents::
   :depth: 2
   :backlinks: top
   :local:

------

Drivers
-------
- Local
- S3
- Dropbox
- FTP

------

Using 
-----
::

    from storage import Storage

    disk = Disk()
    disk = Disk('disk_1')


------

Put File
^^^^^^^^

Local / S3 / Dropbox / FTP
""""""""""""""""""""""""""
::

	disk.put('filename.txt', 'file body content')
	disk.put('filename.txt', open('source_file.txt'))

S3
"""
::

	disk.put('filename.txt', 'file body content', acl='public-read')

------

Get File
^^^^^^^^
Local / S3 / Dropbox
""""""""""""""""""""
::

	disk.get('filename.txt')
	disk.get('filename.txt', save_to='local_file.txt')


FTP
"""
::

	disk.get('filename.txt', save_to='local_file.txt')

	def callback(content):
    	print(content)
	disk.get('filename.txt', callback=callback)


------

Delete File
^^^^^^^^^^^
Local / S3 / Dropbox / FTP
""""""""""""""""""""""""""
::

	disk.delete('filename.txt')


------

Copy File
^^^^^^^^^
Local / S3 / Dropbox / FTP
""""""""""""""""""""""""""
::

	disk.copy('filename.txt', 'copy_here.txt')


S3
"""
::

	disk.copy('filename.txt', 'copy_here.txt', acl='public-read')


------

Move File
^^^^^^^^^
Local / S3 / Dropbox / FTP
""""""""""""""""""""""""""
::

	disk.move('filename.txt', 'to_here.txt')


------

Exist File
^^^^^^^^^^
Local / S3 / Dropbox / FTP
""""""""""""""""""""""""""
::

	disk.exist('filename.txt')


------

Get Permissions
^^^^^^^^^^^^^^^
Local / S3 / FTP
""""""""""""""""
::

	disk.permissions('filename.txt')


------

Set Permissions
^^^^^^^^^^^^^^^
Local / FTP
"""""""""""
::

	disk.permissions('filename.txt', chmod=777)

S3
"""
::

	disk.permissions('filename.txt', acl='public-read')


------

List Files
^^^^^^^^^^
Local / S3 / Dropbox / FTP
""""""""""""""""""""""""""
::

	disk.files()
	disk.files('dir/subdir')
	disk.files('dir', prefix='log_', suffix='.txt')


------

List Directories
^^^^^^^^^^^^^^^^
Local / S3 / Dropbox
""""""""""""""""""""
::

	disk.dirs()
	disk.dirs('dir/subdir')
	disk.dirs('dir', prefix='imgs_', suffix='text')

------

Create Directory
^^^^^^^^^^^^^^^^
Local / Dropbox / FTP
"""""""""""""""""""""
::

	disk.make_dir('folder/sub_folder')


------

Delete Directory
^^^^^^^^^^^^^^^^
Local / Dropbox / FTP
"""""""""""""""""""""
::

	disk.delete_dir('folder')


------

Return Value
------------
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| Method/Driver  | Local                | S3                   | Dropbox              | FTP                  |
+================+======================+======================+======================+======================+
| put( )         | Boolean              | Boolean              | Boolean              | Boolean              |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| get( )         | Str \| False         | Str \| False         | Str \| False         | Boolean              |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| delete( )      | Boolean              | Boolean              | Boolean              | Boolean              |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| copy( )        | Boolean              | Boolean              | Boolean              | Boolean              |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| move( )        | Boolean              | Boolean              | Boolean              | Boolean              |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| exist( )       | Boolean              | Boolean              | Boolean              | Boolean              |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| permissions( ) | Str \| Boolean       | List \| Boolean      | ``n/a``              | Str \| Boolean       |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| files( )       | List                 | List                 | List                 | List                 |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| dirs( )        | List                 | List                 | List                 | ``n/a``              |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| make_dir( )    | Boolean              | ``n/a``              | Boolean              | Boolean              |
+----------------+----------------------+----------------------+----------------------+----------------------+ 
| delete_dir( )  | Boolean              | ``n/a``              | Boolean              | Boolean              |
+----------------+----------------------+----------------------+----------------------+----------------------+ 

------

Setting
^^^^^^^
Define Model
""""""""""""
::

	import os
	os.environ.setdefault('DISKPY_SETTING', 'diskpy_setting')


Setting File
""""""""""""
diskpy_setting.py
::

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

