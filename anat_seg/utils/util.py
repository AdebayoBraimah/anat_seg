# -*- coding: utf-8 -*-
"""Utility module.
"""
import os
from typing import Optional, Tuple, Union

from anat_seg import ATLASDIR

from commandio.commandio.command import Command
from commandio.commandio.logutil import LogFile
from commandio.commandio.workdir import WorkDir


def extract(file: str, /, log: Optional[Union[LogFile, str]] = None) -> None:
    """Extracts compressed file.

    Args:
        file: Input file (position only argument).
        log: Log file. Defaults to None.

    Raises:
        RuntimeError: Exception that is raised if the file extension cannot be used to identify uncompression application/program.

    Returns:
        None
    """
    if file.endswith('.tar.bz2') or file.endswith('.tbz2'):
        cmd: str = f"tar -xvjf {file}"
    elif file.endswith('.tar.gz') or file.endswith('.tgz'):
        cmd: str = f"tar -xvzf {file}"
    elif file.endswith('.bz2'):
        cmd: str = f"bunzip2 {file}"
    elif file.endswith('.rar'):
        cmd: str = f"unrar {file}"
    elif file.endswith('.gz'):
        cmd: str = f"gunzip {file}"
    elif file.endswith('.tar'):
        cmd: str = f"tar -xvf {file}"
    elif file.endswith('.zip'):
        cmd: str = f"unzip {file}"
    elif file.endswith('.7z'):
        cmd: str = f"7z {file}"
    else:
        raise RuntimeError(f"Unable to extract/uncompress file: {file}")

    uncompress: Command = Command(cmd)
    uncompress.check_dependency()
    uncompress.run(log=log)

    return None


def get_UNC_neonate_atlas() -> Tuple[str, str, str, str, str]:
    unc_atlas_dir: str = os.path.join(ATLASDIR, "UNC_infant_atlas_2020")

    if os.path.exists(unc_atlas_dir):
        with WorkDir(src=unc_atlas_dir) as ud:
            template: str = ud.join(
                'atlas', 'templates', 'infant-neo-withSkull.nii.gz'
            )
            template_brain: str = ud.join(
                'atlas', 'templates', 'infant-neo-withCerebellum.nii.gz'
            )
            gm: str = ud.join('atlas', 'templates', 'infant-neo-seg-gm.nii.gz')
            wm: str = ud.join('atlas', 'templates', 'infant-neo-seg-wm.nii.gz')
            csf: str = ud.join(
                'atlas', 'templates', 'infant-neo-seg-csf.nii.gz'
            )
        return template, template_brain, gm, wm, csf
    else:
        unc_zip_file: str = os.path.join(ATLASDIR, 'UNC.tar.gz')
        extract(unc_zip_file)
        get_UNC_neonate_atlas()
