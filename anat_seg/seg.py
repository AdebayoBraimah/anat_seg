# -*- coding: utf-8 -*-
"""Brain image segmentation module.

This module is a wrapper for several of ``FSL``'s and ``ANTs``' executables.
"""
import os
from typing import Dict, List, Optional, Tuple, Union

from utils.commandio.commandio.logutil import LogFile
from utils.commandio.commandio.tmpfile import TmpFile
from utils.commandio.commandio.workdir import WorkDir
from utils.commandio.commandio.util import timeops
from utils.niio import NiiFile
from utils.util import get_UNC_neonate_atlas

from biascorr import biascorr
from fsl.bet import bet
from fsl.fast import fast
from fsl.flirt import flirt
from fsl.fnirt import fnirt
from fsl.applywarp import applywarp
from fsl.convertwarp import convertwarp
from fsl.fslmaths import fslmaths


# Globlally define (temporary) log file object
# NOTE: Not the best practice in this scenario, but
#   it gets the job done.
with TmpFile(tmp_dir=os.getcwd(), ext=".log") as tmpf:
    log: LogFile = LogFile(log_file=tmpf.src)
    tmpf.remove()


@timeops(log=log)
def segmentation(
    image: str,
    out: str,
    frac_int: float = 0.5,
    N4: bool = False,
    nobias: bool = False,
    intype: int = 1,
    classes: int = 3,
    priors: List[str] = None,
    neonate: bool = False,
    log: Union[str, LogFile] = None,
) -> Union[List[str], Tuple[str, str, str, str]]:
    """_summary_

    _extended_summary_

    Args:
        image: Input neonatal T2w image.
        out: Output directory.
        frac_int: Fractional intensity threshold (0->1); smaller values give larger brain outline estimates. RECOMMENDED: 0.3 (for neonates). Defaults to 0.5.
        N4: Perform N4 bias field correction, otherwise perform FSL's bias field correction. Defaults to False.
        nobias: Do not perform bias field correction. Defaults to False.
        intype: Input image type. Defaults to 1.
            * ``1``: T1w
            * ``2``: T2w
            * ``3``: PD - Proton Density
        classes: Number of tissue classes. Defaults to 3.
        priors: Alternative prior images input as a list (e.g. [ 'csf.nii.gz', 'gm.nii.gz', 'wm.nii.gz' ]).
        neonate: Uses atlas-based segmentation (intended for neonates). Defaults to False.
        log: Log file path OR ``LogFile`` object. Defaults to None.

    Returns:
        Either a list of files OR a tuple that correspond to segmentation outputs.
    """
    if neonate:
        segs: Tuple[str, str, str, str] = _neo_seg(
            image=image,
            out=out,
            frac_int=frac_int,
            N4=N4,
            nobias=nobias,
            intype=intype,
            classes=classes,
            log=log,
        )
        return segs
    else:
        segs: List[str] = _seg(
            image=image,
            out=out,
            frac_int=frac_int,
            N4=N4,
            nobias=nobias,
            intype=intype,
            classes=classes,
            priors=priors,
            log=log,
        )
        return segs


def _seg(
    image: str,
    out: str,
    frac_int: float = 0.5,
    N4: bool = False,
    nobias: bool = False,
    intype: int = 1,
    classes: int = 3,
    priors: List[str] = None,
    log: Optional[Union[str, LogFile]] = None,
) -> List[str]:
    """Helper function that performs segmentation of neuroimages into CSF, gray matter, and white matter.

    The segmentation software uses ``FSL``'s ``FAST``.

    Args:
        image: Input neonatal T2w image.
        out: Output directory.
        frac_int: Fractional intensity threshold (0->1); smaller values give larger brain outline estimates. Defaults to 0.5.
        N4: Perform N4 bias field correction, otherwise perform FSL's bias field correction. Defaults to False.
        nobias: Do not perform bias field correction. Defaults to False.
        intype: Input image type. Defaults to 1.
            * ``1``: T1w
            * ``2``: T2w
            * ``3``: PD - Proton Density
        classes: Number of tissue classes. Defaults to 3.
        priors: Alternative prior images input as a list (e.g. [ 'csf.nii.gz', 'gm.nii.gz', 'wm.nii.gz' ]).
        log: Log file path OR ``LogFile`` object. Defaults to None.

    Returns:
        List of files that correspond to segmentation outputs.
    """
    # Output working directory
    outdir: str = os.path.abspath(out)

    # TODO: Configure to use list of input images.
    #   * Multi-channel segmentation would likely yield
    #       better/more consistent results.
    with WorkDir(src=outdir) as od:
        # Bias correct image
        if nobias:
            restore: str = image
        else:
            restore, _ = biascorr(
                image=image, out=od.join('anat'), N4=N4, log=log
            )

        # Mask brain
        brain, _ = bet(
            image=restore,
            out=od.join('anat_brain.nii.gz'),
            frac_int=frac_int,
            mask=True,
            log=log,
        )

        seg_list: List[str] = fast(
            images=brain,
            out=od.join('fast_segmentation'),
            intype=int(intype),
            classes=int(classes),
            priors=priors,
            log=log,
        )

        return seg_list


def _neo_seg(
    image: str,
    out: str,
    frac_int: float = 0.3,
    N4: bool = False,
    nobias: bool = False,
    intype: int = 2,
    classes: int = 5,
    log: Optional[Union[str, LogFile]] = None,
) -> Tuple[str, str, str, str]:
    """Helper function that performs atlas-based segmentation of neonatal neuroimages into CSF, gray matter, and white matter.

    The atlas used is the UNC neonatal structural atlas. The segmentation software uses ``FSL``'s ``FAST``.
    The defaults of this helper function are intended exclusively for neonates.

    Args:
        image: Input neonatal T2w image.
        out: Output directory.
        frac_int: Fractional intensity threshold (0->1); smaller values give larger brain outline estimates. RECOMMENDED: 0.3 (for neonates). Defaults to 0.3.
        N4: Perform N4 bias field correction, otherwise perform FSL's bias field correction. Defaults to False.
        nobias: Do not perform bias field correction. Defaults to False.
        intype: Input image type. Defaults to 2.
            * ``1``: T1w
            * ``2``: T2w
            * ``3``: PD - Proton Density
        classes: Number of tissue classes. Defaults to 5.
        log: Log file path OR ``LogFile`` object. Defaults to None.

    Returns:
        Tuple of strings that correspond to: CSF, GM, WM and mixeltype NIFTI-1 image files.
    """
    # Output working directory
    outdir: str = os.path.abspath(out)

    # TODO: Configure to use list of input images.
    #   * Multi-channel segmentation would likely yield
    #       better/more consistent results.
    with WorkDir(src=outdir) as od:
        # Bias correct image
        if nobias:
            restore: str = image
        else:
            restore, _ = biascorr(
                image=image, out=od.join('anat'), N4=N4, log=log
            )

        # Mask brain
        brain, _ = bet(
            image=restore,
            out=od.join('anat_brain.nii.gz'),
            frac_int=frac_int,
            mask=True,
            log=log,
        )

        # Compute transforms

        ## Get neonatal template files
        (
            template,
            template_brain,
            template_gm,
            template_wm,
            template_csf,
        ) = get_UNC_neonate_atlas()

        ## Compute (affine) linear transforms
        _, lin_xfm_mat = flirt(
            image=template_brain,
            ref=brain,
            out=od.join('template-to-native_space-native_xfm-linear.nii.gz'),
            omat=True,
            dof=12,
            log=log,
        )

        ## Compute non-linear transforms
        _, nonlin_xfm_fout, _ = fnirt(
            image=template,
            ref=restore,
            aff=lin_xfm_mat,
            out=od.join(
                'template-to-native_space-native_xfm-nonlinear.nii.gz'
            ),
            iout=True,
            fout=True,
            cout=True,
            log=log,
        )

        ## Convert warps and incorporate linear transforms
        nonlin_xfm_warp: str = convertwarp(
            warp=nonlin_xfm_fout,
            out=od.join('template-to-native_space-native_xfm-nonlinear_warp'),
            ref=restore,
            rel=True,
            log=log,
        )

        ## Apply non-linear transforms to template files
        tissues: Dict[str, str] = {
            "gm": {
                "template": template_gm,
                "xfm": od.join(
                    'template-to-native_space-native_xfm-nonlinear_tissue-gm.nii.gz'
                ),
            },
            "wm": {
                "template": template_wm,
                "xfm": od.join(
                    'template-to-native_space-native_xfm-nonlinear_tissue-wm.nii.gz'
                ),
            },
            "csf": {
                "template": template_csf,
                "xfm": od.join(
                    'template-to-native_space-native_xfm-nonlinear_tissue-csf.nii.gz'
                ),
            },
        }

        for tissue in tissues.keys():
            _: str = applywarp(
                image=tissues.get(tissue).get('template'),
                ref=brain,
                out=tissues.get(tissue).get('xfm'),
                warp=nonlin_xfm_warp,
                rel=True,
                log=log,
            )

        ## Perform brain tissue segmentation
        seg_list: List[str] = fast(
            images=brain,
            out=od.join('fast_segmentation'),
            intype=int(intype),
            classes=int(classes),
            priors=[
                tissues.get('csf').get('template'),
                tissues.get('gm').get('template'),
                tissues.get('wm').get('template'),
            ],
            log=log,
        )

        ## Rename and construct files
        #
        # NOTE:
        #   The files used here are consistent with what
        #   has been seen through trial and error.
        pve0, pve1, pve2, pve3, _, mixel = seg_list

        ### CSF
        with NiiFile(src=pve0, assert_exists=True, validate_nifti=True) as pv:
            csf: str = od.join(
                'fast_segmentation_space-native_tissue-csf.nii.gz'
            )
            _: str = pv.move(csf)
            log.log(f"Moving {pv.abspath()} to {csf}")

        ### GM
        with NiiFile(src=pve3, assert_exists=True, validate_nifti=True) as pv:
            gm: str = fslmaths(pv.abspath()).fmean().run(
                out=od.join('fast_segmentation_space-native_tissue-gm.nii.gz'),
                log=log,
            )

        ### WM
        with NiiFile(src=pve1, assert_exists=True, validate_nifti=True) as pv1:
            with NiiFile(
                src=pve2, assert_exists=True, validate_nifti=True
            ) as pv2:
                wm: str = fslmaths(pv1.abspath()).add(
                    pv2.abspath()
                ).fmedian().run(
                    out=od.join(
                        'fast_segmentation_space-native_tissue-wm.nii.gz'
                    ),
                    log=log,
                )

        return csf, gm, wm, mixel

