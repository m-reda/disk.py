from diskpy import Disk, SettingException
import os

BASE = os.path.dirname(os.path.abspath(__file__))

disk = None


def test_disk():
    global disk

    try:
        disk = Disk('s3')
    except SettingException:
        assert False


def test_put_text():
    assert disk.put('test/filename.txt', 'some text')


def test_put_file():
    with open(BASE + '/post.txt', 'r') as f:
        put = disk.put('test/filename2.txt', f)
        f.close()
        assert put


def test_get():
    assert disk.get('test/filename.txt') == b'some text'


def test_get_and_save():
    assert disk.get('test/filename.txt', save_to=BASE + '/local_disk/saved.txt') != False


def test_copy():
    assert disk.copy('test/filename.txt', 'test/filename3.txt')


def test_move():
    assert disk.move('test/filename.txt', 'test/filename1.txt')


def test_exist():
    assert disk.exist('test/filename1.txt')
    assert disk.exist('test/filename2.txt')
    assert disk.exist('test/filename3.txt')


def test_set_permissions():
    assert disk.permissions('test/filename1.txt', acl='public-read')


def test_get_permissions():
    assert isinstance(disk.permissions('test/filename1.txt'), list)


def test_files_list():
    files = disk.files('test')
    expected = ['test/filename1.txt', 'test/filename2.txt', 'test/filename3.txt']

    assert files == expected


def test_delete_files():
    os.remove(BASE + '/local_disk/saved.txt')
    assert disk.delete('test/filename1.txt')
    assert disk.delete('test/filename2.txt')
    assert disk.delete('test/filename3.txt')


def test_dirs_list():
    assert disk.dirs('test') == ['test/sub_folder/']








