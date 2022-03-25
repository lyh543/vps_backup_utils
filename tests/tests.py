from vps_backup_utils import VPSBackupUtils

if __name__ == '__main__':
    vps_backup_utils = VPSBackupUtils('.')
    vps_backup_utils.remove_old_backup(7)