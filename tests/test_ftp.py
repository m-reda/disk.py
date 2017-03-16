from diskpy import Disk, SettingException
import os

BASE = os.path.dirname(os.path.abspath(__file__))

disk = None


def test_disk():
    global disk

    try:
        disk = Disk('ftp')
    except SettingException:
        assert False


def test_put_text():
    assert disk.put('filename.txt', 'some text')


def test_put_file():
    with open(BASE + '/post.txt', 'rb') as f:
        put = disk.put('filename2.txt', f)
        f.close()
        assert put


def test_get():
    def callback(content):
        print(content)

    assert disk.get('filename.txt', callback=callback)


def test_get_and_save():
    assert disk.get('filename.txt', save_to=BASE + '/local_disk/saved.txt') != False


def test_copy():
    assert disk.copy('filename.txt', 'filename3.txt')


def test_move():
    assert disk.move('filename.txt', 'filename1.txt')


def test_exist():
    assert disk.exist('filename1.txt')
    assert disk.exist('filename2.txt')
    assert disk.exist('filename3.txt')


def test_set_permissions():
    assert disk.permissions('filename1.txt', chmod=777)


def test_get_permissions():
    # assert disk.permissions('filename1.txt') == '777'
    pass


def test_make_dir():
    assert disk.make_dir('folder')
    assert disk.make_dir('folder/sub_folder')


def test_files_list():
    files = disk.files()
    print(files)
    expected = ['filename1.txt', 'filename2.txt', 'filename3.txt', 'folder']

    assert files == expected


def test_delete_files():
    os.remove(BASE + '/local_disk/saved.txt')

    assert disk.delete('filename1.txt')
    assert disk.delete('filename2.txt')
    assert disk.delete('filename3.txt')


def test_delete_dir():
    assert disk.delete_dir('folder/sub_folder')
    assert disk.delete_dir('folder')








