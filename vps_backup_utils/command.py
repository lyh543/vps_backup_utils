"""
This module convert Python functions to shell commands.
"""

import logging
import os
from pipes import quote
from typing import List, Union

from .common import PathLikeStr

logger = logging.getLogger(__name__)


def run_command(cmd: PathLikeStr):
    logger.info(f"Executing: {cmd}")
    if os.system(cmd) != 0:
        raise Exception(f"Command {cmd} failed")


def gzip(target: PathLikeStr):
    gzip_cmd = f"gzip -f {quote(target)}"
    run_command(gzip_cmd)


def tar(target: PathLikeStr = 'file.tar',
        src: Union[PathLikeStr, List[PathLikeStr]] = '.',
        gzipped=True):
    """
    tar folder
    will add '.gz' to filename if gzipped
    """
    src_joined = " ".join(map(quote, src))
    if gzipped:
        tar_cmd = f"tar -czf {quote(target + '.gz')} {src_joined}"
    else:
        tar_cmd = f"tar -cf {quote(target)} {src_joined}"
    run_command(tar_cmd)


def rsync(local_path: PathLikeStr,
          host: str,
          user: str,
          remote_path: PathLikeStr,
          port: str,
          is_upload = True,
          delete_mode = True):
    """
    sync backup folder to remote server
    need `rsync` in PATH, and ssh key configured
    """
    _local_path = quote(local_path)
    _remote_path = f"{user}@{host}:{quote(remote_path)} --port {port}"
    if is_upload:
        paths = f"{_local_path} {_remote_path}"
    else:
        paths = f"{_remote_path} {_local_path}"
    rsync_cmd = f"""rsync \\
        --archive \\
        --verbose \\
        --human-readable \\
        {'--delete' if delete_mode else ''} \\
        {paths}"""
    run_command(rsync_cmd)


def mysqldump(host: str,
              port: str,
              user: str,
              password: str,
              db: str,
              all_databases: bool,
              output_filename: PathLikeStr):
    _db = '--all-databases' if all_databases else db
    dump_cmd = f"""mysqldump \\
        -h {host} \\
        -P {port} \\
        -u {user} \\
        -p{password} \\
        {_db} \\
        > {quote(output_filename)}"""
    run_command(dump_cmd)


def pg_dump(host: str,
            port: str,
            db: str,
            all_databases: bool,
            output_filename: PathLikeStr):
    _cli = "pg_dumpall" if all_databases else f"pg_dump {db}"
    dump_cmd = f"""{_cli} \\
        -h {host} \\
        -p {port} \\
        {db} \\
        > {quote(output_filename)}"""
    run_command(dump_cmd)