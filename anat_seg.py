#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Perform anatomical segmentation of structural adult, pediatric, and neonatal (T2w) neuroimages.

Command line options override default settings.
"""
import sys
import argparse

from typing import Any, Dict, List, Tuple

from anat_seg.seg import segmentation
from anat_seg import __version__
from anat_seg.utils.commandio.commandio.workdir import WorkDir
from anat_seg.utils.commandio.commandio.logutil import LogFile


def main() -> None:
    proc()
    return None


def proc() -> List[str]:
    args, parser = arg_parser()

    # Print help message in the case of no arguments
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        args: Dict[str, Any] = vars(args)

    # Set defaults
    defaults: Dict[str, Any] = {
        'image': args.get('image'),
        'out': args.get('out'),
        'frac_int': args.get('frac_int'),
        'N4': args.get('N4'),
        'nobias': args.get('no_bias'),
        'intype': args.get('intype'),
        'classes': args.get('classes'),
        'priors': args.get('priors'),
        'neonate': args.get('neonate'),
        'log': args.get('log'),
    }

    if defaults.get('neonate'):

        if defaults.get('frac_int') is None:
            defaults['frac_int'] = 0.3

        if defaults.get('intype') is None:
            defaults['intype'] = 2

        if defaults.get('classes') is None:
            defaults['classes'] = 5
    else:

        if defaults.get('frac_int') is None:
            defaults['frac_int'] = 0.5

        if defaults.get('intype') is None:
            defaults['intype'] = 1

        if defaults.get('classes') is None:
            defaults['classes'] = 3

    with WorkDir(defaults.get('out')) as od:
        _log_file: str = od.join('anat_seg.log')
        log_file: LogFile = LogFile(_log_file)
        defaults['log'] = log_file
        log_file.log(f"anat_seg v{__version__}")

    seg_list: List[str] = segmentation(**defaults)
    return seg_list


def arg_parser() -> Tuple[
    argparse.ArgumentParser.parse_args, argparse.ArgumentParser
]:
    """CLI Argument parser.
    
    Returns:
        Tuple of ``argparse`` objects.
    """
    # Init parser
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=55, width=100
        ),
    )

    # Parse Arguments
    # Required Arguments
    reqoptions = parser.add_argument_group("Required arguments")

    reqoptions.add_argument(
        "-i",
        "--image",
        type=str,
        dest="image",
        metavar="<NIFTI>",
        required=True,
        help="Input structural T1w (or T2w in the case of neonates,) image file.",
    )

    reqoptions.add_argument(
        "-o",
        "--output-dir",
        type=str,
        dest="out",
        metavar="<DIR>",
        required=True,
        help="Output directory path.",
    )

    # Optional Arguments
    optoptions = parser.add_argument_group("Optional arguments")

    optoptions.add_argument(
        "-f",
        "--frac-int",
        type=float,
        dest="frac_int",
        metavar="<FLOAT>",
        default=None,
        required=False,
        help="Fractional intensity for brain extraction. [default: 0.5]",
    )

    optoptions.add_argument(
        "--N4",
        action="store_true",
        dest="N4",
        default=False,
        required=False,
        help="Perform N4 bias correction instead of FSL's bias correction (Recommended) [default: False].",
    )

    optoptions.add_argument(
        "--no-bias",
        action="store_true",
        dest="no_bias",
        default=False,
        required=False,
        help="Do not perform bias correction [default: False].",
    )

    optoptions.add_argument(
        "-t",
        "--type",
        type=int,
        dest="intype",
        metavar="<INT>",
        default=None,
        required=False,
        help="Input image type - 1: T1w, 2: T2w, 3: PD. [default: 1]",
    )

    optoptions.add_argument(
        "-c",
        "--classes",
        type=int,
        dest="classes",
        metavar="<INT>",
        default=None,
        required=False,
        help="Number of tissue classes. [default: 3]",
    )

    optoptions.add_argument(
        "-p",
        "--priors",
        type=str,
        dest="priors",
        metavar="<NIFTI>",
        default=None,
        required=False,
        action='append',
        help="Alternative prior images. [Repeatable] NOTE: Inputs should correspond to segmented: GM, WM, and CSF - in subject's structural native space.",
    )

    optoptions.add_argument(
        "--neonate",
        action="store_true",
        dest="neonate",
        default=False,
        required=False,
        help="If specified, settings are changed to accomodate neonatal T2w images such as lowering the fractional intensity, and changing the segmentation settings. \
            Other comamnd line settings will override these settings if specified. NOTE: This segmentation output is sub-optimal at best. Use with supreme caution. [default: False].",
    )

    args: argparse.ArgumentParser.parse_args = parser.parse_args()
    return args, parser


if __name__ == "__main__":
    main()
