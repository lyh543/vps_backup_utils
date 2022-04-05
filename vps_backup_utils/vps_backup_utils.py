import logging
import os
import time
from datetime import datetime, timedelta
from typing import List

# todo: test tar, rsync and pg_dump
from .command import mysqldump, gzip, tar, rsync
from .common import PathLikeStr


class VPSBackupUtils:
    def __init__(self, backup_dest: PathLikeStr):
        logging.basicConfig(format='[%(levelname)-8s] %(asctime)s %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.backup_dest = backup_dest
        # Getting current DateTime to create the separate backup folder like "20180817-123433".
        datetime = time.strftime('%Y%m%d-%H%M%S')
        self.backup_dest_today = os.path.join(self.backup_dest, datetime)
        self.logger.info(f'backup dest today: {self.backup_dest_today}')
        os.makedirs(self.backup_dest_today, exist_ok=True)

    def mysqldump_backup(self,
                         backup_prefix: str,
                         host='localhost',
                         port='3306',
                         user='root',
                         password='password',
                         databases: List[str] = None,
                         gzipped=True):
        """
        backup MySQL data with mysqldump.
        need `mysqldump` and `gzip` (if gzip == true) in PATH.
        notice: backup all databases if 'databases == None'.
        """

        def dump_and_gzip(filename: str, db: str = '', all_databases: bool = True):
            output_filename = os.path.join(self.backup_dest_today, filename)
            mysqldump(host=host, port=port, user=user, password=password, db=db, all_databases=all_databases,
                      output_filename=output_filename)
            if gzipped:
                gzip(output_filename)

        if databases is None:
            dump_and_gzip(f'{backup_prefix}.sql', db='', all_databases=True)
        else:
            for db in databases:
                dump_and_gzip(f'{backup_prefix}_{db}.sql', db=db, all_databases=False)
        self.logger.info(f'{backup_prefix}: MySQL data backup finished')

    def tar_backup(self,
                   backup_prefix: str,
                   src_folder: str,
                   gzipped=True):
        """
        copy webapp data directory.
        need `tar` in PATH.
        """
        tar(src_folder, os.path.join(self.backup_dest_today, f'{backup_prefix}.tar'), gzipped=gzipped)
        self.logger.info(f'{backup_prefix}: {src_folder} data backup finished')

    def remove_old_backups(self, days_to_keep: int = 7):
        """
        remove old backup folders.
        """
        with os.scandir(self.backup_dest) as dir_entries:
            for entry in dir_entries:
                info = entry.stat()
                filename: str = entry.name
                last_modified = datetime.fromtimestamp(info.st_mtime)
                if last_modified < datetime.now() - timedelta(days=days_to_keep):
                    os.remove(os.path.join(self.backup_dest, filename))
                    self.logger.info(f'{filename} removed, since it is older than {days_to_keep} days')

    def rsync_backups_to_remote(self,
                                host: str,
                                user: str,
                                remote_backup_path: str,
                                port='22',
                                delete_mode=True):
        """
        sync backup folder to remote server.
        need `rsync` in PATH, and ssh key configured.
        """
        rsync(local_path=self.backup_dest_today, host=host, user=user, remote_path=remote_backup_path, port=port,
              delete_mode=delete_mode)
        self.logger.info(f'rsync to {user}@{host}:{remote_backup_path} finished')
