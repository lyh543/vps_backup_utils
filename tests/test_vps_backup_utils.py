import os
from pathlib import PosixPath

from vps_backup_utils import VPSBackupUtils


def test_init_function(tmp_path: PosixPath):
    assert len(os.listdir(tmp_path)) == 0
    backuper = VPSBackupUtils(tmp_path)
    assert len(os.listdir(tmp_path)) == 1


def test_mysqldump_backup(tmp_path: PosixPath):
    backuper = VPSBackupUtils(tmp_path)
    backuper.mysqldump_backup(backup_prefix='pytest',
                              host='mysql',
                              port=3306,
                              user='root',
                              password='password',
                              databases=None,
                              gzipped=False)
    assert len(os.listdir(tmp_path)) == 1
    sqlfile = os.path.join(tmp_path, os.listdir(tmp_path)[0], 'pytest.sql')
    assert os.path.getsize(sqlfile) > 0
    with open(sqlfile, 'r') as f:
        sql = f.read()
        # assert database is exported correctly
        assert sql.find('-- Current Database: `mysql`') > 0
    backuper.mysqldump_backup(backup_prefix='pytest',
                              host='mysql',
                              port=3306,
                              user='mysql_user',
                              password='mysql_password',
                              databases=None,
                              gzipped=True)
    gzfile = os.path.join(tmp_path, os.listdir(tmp_path)[0], 'pytest.sql.gz')
    assert os.path.getsize(gzfile) > 0
