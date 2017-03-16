from diskpy import Disk, SettingException
from diskpy.drivers import Local


def test_driver():
    try:
        disk = Disk()
    except SettingException:
        assert False

    assert isinstance(disk.driver, Local)
