from diskpy import Disk, SettingException
import os

BASE = os.path.dirname(os.path.abspath(__file__))

disk = None


def test_disk():
    global disk

    try:
        disk = Disk('local')
    except SettingException as e:
        assert False


def test_put_text():
    assert disk.put('filename.txt', 'some text')


def test_put_file():
    with open(BASE + '/post.txt', 'r') as f:
        put = disk.put('filename2.txt', f)
        f.close()
        assert put


def test_get():
    assert disk.get('filename.txt') == 'some text'


def test_get_and_save():
    assert disk.get('filename.txt', save_to=BASE + '/local_disk/filename3.txt') != False


def test_copy():
    assert disk.copy('filename.txt', 'filename4.txt')


def test_move():
    assert disk.move('filename.txt', 'filename1.txt')


def test_exist():
    assert disk.exist('filename1.txt')
    assert disk.exist('filename2.txt')
    assert disk.exist('filename3.txt')
    assert disk.exist('filename4.txt')


def test_set_permissions():
    assert disk.permissions('filename1.txt', chmod=777)


def test_get_permissions():
    assert disk.permissions('filename1.txt') == '777'


def test_files_list():
    files = disk.files()
    expected = ['filename1.txt', 'filename2.txt', 'filename3.txt', 'filename4.txt']

    assert files == expected


def test_delete_files():
    assert disk.delete('filename1.txt')
    assert disk.delete('filename2.txt')
    assert disk.delete('filename3.txt')
    assert disk.delete('filename4.txt')


def test_make_dir():
    assert disk.make_dir('folder')
    assert disk.make_dir('folder/sub_folder')


def test_dirs_list():
    assert disk.dirs('folder') == ['sub_folder']


def test_delete_dir():
    assert disk.delete_dir('folder')








