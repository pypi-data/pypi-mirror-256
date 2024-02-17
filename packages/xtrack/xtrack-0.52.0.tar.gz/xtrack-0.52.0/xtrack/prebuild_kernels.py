# copyright ################################# #
# This file is part of the Xobjects Package.  #
# Copyright (c) CERN, 2023.                   #
# ########################################### #
import os
import json
import logging
from pathlib import Path
from pprint import pformat
from typing import Iterator, Optional, Tuple

from .general import _print

import numpy as np

import xobjects as xo
import xpart as xp
import xtrack as xt

LOGGER = logging.getLogger(__name__)

XT_PREBUILT_KERNELS_LOCATION = Path(xt.__file__).parent / 'prebuilt_kernels'

BEAM_ELEMENTS_INIT_DEFAULTS = {
    'Bend': {
        'length': 1.,
    },
    'Quadrupole': {
        'length': 1.,
    },
    'Solenoid': {
        'length': 1.,
    },
    'BeamBeamBiGaussian2D': {
        'other_beam_Sigma_11': 1.,
        'other_beam_Sigma_33': 1.,
        'other_beam_num_particles': 0.,
        'other_beam_q0': 1.,
        'other_beam_beta0': 1.,
    },
    'BeamBeamBiGaussian3D': {
        'slices_other_beam_zeta_center': np.array([0]),
        'slices_other_beam_num_particles': np.array([0]),
        'phi': 0.,
        'alpha': 0,
        'other_beam_q0': 1.,
        'slices_other_beam_Sigma_11': np.array([1]),
        'slices_other_beam_Sigma_12': np.array([0]),
        'slices_other_beam_Sigma_22': np.array([0]),
        'slices_other_beam_Sigma_33': np.array([1]),
        'slices_other_beam_Sigma_34': np.array([0]),
        'slices_other_beam_Sigma_44': np.array([0]),
    },
    'LimitPolygon': {
        'x_vertices': np.array([0, 1, 1, 0]),
        'y_vertices': np.array([0, 0, 1, 1]),
    },
}

# SpaceChargeBiGaussian is not included for now (different issues -
# circular import, incompatible compilation flags)
# try:
#     from xfields import LongitudinalProfileQGaussian

#     BEAM_ELEMENTS_INIT_DEFAULTS['SpaceChargeBiGaussian'] = {
#         'longitudinal_profile': LongitudinalProfileQGaussian(
#             number_of_particles=0, sigma_z=1),
#     }
# except ModuleNotFoundError:
#     LOGGER.warning('Prebuilding kernels might fail, as xfields is not '
#                    'installed.')


def get_element_class_by_name(name: str) -> type:
    # from xtrack.monitors import generate_monitor_class
    # monitor_cls = generate_monitor_class(xp.Particles)
    monitor_cls = xt.ParticlesMonitor

    try:
        from xfields import element_classes as xf_element_classes
    except ModuleNotFoundError:
        xf_element_classes = ()

    element_classes = xt.element_classes + xf_element_classes + (monitor_cls,)

    for cls in element_classes:
        if cls.__name__ == name:
            return cls

    raise ValueError(f'No element class with name {name} available.')


def save_kernel_metadata(
        module_name: str,
        config: dict,
        kernel_element_classes,
):
    out_file = XT_PREBUILT_KERNELS_LOCATION / f'{module_name}.json'

    try:
        import xfields
        xf_version = xfields.__version__
    except ModuleNotFoundError:
        xf_version = None

    kernel_metadata = {
        'config': config.data,
        'classes': [cls._DressingClass.__name__ for cls in kernel_element_classes],
        'versions': {
            'xtrack': xt.__version__,
            'xfields': xf_version,
            'xobjects': xo.__version__,
        }
    }

    with out_file.open('w') as fd:
        json.dump(kernel_metadata, fd, indent=4)


def enumerate_kernels() -> Iterator[Tuple[str, dict]]:
    """
    Iterate over the prebuilt kernels compatible with the current version of
    xsuite. The first element of the tuple is the name of the kernel module
    and the second is a dictionary with the kernel metadata.
    """
    for metadata_file in XT_PREBUILT_KERNELS_LOCATION.glob('*.json'):
        if metadata_file.stem.startswith('_'):
            continue

        with metadata_file.open('r') as fd:
            kernel_metadata = json.load(fd)

        try:
            import xfields
            xf_version = xfields.__version__
        except ModuleNotFoundError:
            xf_version = None

        if kernel_metadata['versions']['xtrack'] != xt.__version__:
            continue

        if kernel_metadata['versions']['xobjects'] != xo.__version__:
            continue

        if (kernel_metadata['versions']['xfields'] != xf_version
                and xf_version is not None):
            continue

        yield metadata_file.stem, kernel_metadata


def get_suitable_kernel(
        config: dict,
        line_element_classes,
        verbose=False,
) -> Optional[Tuple[str, list]]:
    """
    Given a configuration and a list of element classes, return a tuple with
    the name of a suitable prebuilt kernel module together with the list of
    element classes that were used to build it. Set `verbose` to True, to
    obtain a justification of the choice (or lack thereof) on standard output.
    """

    env_var = os.environ.get("XSUITE_PREBUILT_KERNELS")
    if env_var and env_var == '0':
        if verbose:
            _print('Skipping the search for a suitable kernel, as the '
                  'environment variable XSUITE_PREBUILT_KERNELS == "0".')
        return

    requested_class_names = [
        cls._DressingClass.__name__ for cls in line_element_classes
    ]

    for module_name, kernel_metadata in enumerate_kernels():
        if verbose:
            _print(f"==> Considering the precompiled kernel `{module_name}`...")

        available_classes_names = kernel_metadata['classes']
        if kernel_metadata['config'] != config:
            if verbose:
                lhs = kernel_metadata['config']
                rhs = config
                config_diff = {kk: (lhs.get(kk), rhs.get(kk))
                               for kk in set(lhs.keys()) | set(rhs.keys())
                               if lhs.get(kk) != rhs.get(kk)}
                _print(f'The kernel `{module_name}` is unsuitable. Its config '
                      f'(left) and the requested one (right) differ at the '
                      f'following keys:\n'
                      f'{pformat(config_diff)}')
                _print(f'Skipping class compatibility check for `{module_name}`.')

            continue

        if verbose:
            _print(f'The kernel `{module_name}` has the right config.')

        if set(requested_class_names) <= set(available_classes_names):
            available_classes = [
                get_element_class_by_name(class_name)
                for class_name in available_classes_names
            ]
            _print(f'Found suitable prebuilt kernel `{module_name}`.')
            return module_name, available_classes
        elif verbose:
            class_diff = set(requested_class_names) - set(available_classes_names)
            _print(f'The kernel `{module_name}` is unsuitable. It does not '
                  f'provide the following requested classes: '
                  f'{", ".join(class_diff)}.')

    if verbose:
        _print('==> No suitable precompiled kernel found.')


def regenerate_kernels():
    """
    Use the kernel definitions in the `kernel_definitions.py` file to
    regenerate kernel shared objects using the current version of xsuite.
    """
    from xtrack.prebuilt_kernels.kernel_definitions import kernel_definitions

    for module_name, metadata in kernel_definitions.items():
        config = metadata['config']
        element_classes = metadata['classes']

        elements = []
        for cls in element_classes:
            if cls.__name__ in BEAM_ELEMENTS_INIT_DEFAULTS:
                element = cls(**BEAM_ELEMENTS_INIT_DEFAULTS[cls.__name__])
            else:
                element = cls()
            elements.append(element)

        line = xt.Line(elements=elements)
        tracker = xt.Tracker(line=line, compile=False)
        tracker.config.clear()
        tracker.config.update(config)
        tracker._build_kernel(
            module_name=module_name,
            containing_dir=XT_PREBUILT_KERNELS_LOCATION,
            compile='force',
        )

        kernel_classes = tracker._tracker_data_base.kernel_element_classes
        save_kernel_metadata(
            module_name=module_name,
            config=tracker.config,
            kernel_element_classes=kernel_classes,
        )


def clear_kernels(verbose=False):
    for file in XT_PREBUILT_KERNELS_LOCATION.iterdir():
        if file.name.startswith('_'):
            continue
        if file.suffix not in ('.c', '.so', '.json'):
            continue
        file.unlink()

        if verbose:
            print(f'Removed `{file}`.')


if __name__ == '__main__':
    regenerate_kernels()
