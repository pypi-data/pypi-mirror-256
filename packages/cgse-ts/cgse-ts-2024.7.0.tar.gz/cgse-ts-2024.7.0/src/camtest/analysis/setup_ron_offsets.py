"""
Reads the config file on r.o.n. and offsets & adds the proper ccd.limits in the setup

The camera ID is identified from the setup, and automatically linked to the right block of data in the config file

2023.06.13 PR
"""


import os
import numpy as np
import yaml
from camtest import load_setup, submit_setup

# setup = load_setup(45)
# print(setup.get_id())

# R.O.N & OFFSETS -- setup.camera.ccd.limits
# ----------------------------------------------------------------------------------------------------------------------

def read_limits_from_yaml_file(filepath: str) -> dict:
    """
   Read a yaml config file containing the offset and readout noise limits

    Args:
        filepath (str, optional): path to the config file. Defaults to 'offset_and_noise_limits.yaml'.

    Returns:
        dict: dictionary containing the offset and readout limits for all cameras (available)
    """
    with open(filepath, 'r') as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)

    return data

def setup_ccd_limits(setup=None, version=None, temp='ambient', confdir=None):
    """
    camera = "brigand"
    fm_id = "FM1"
    """

    from pathlib import Path
    from camtest.analysis import convenience as cv

    if setup is None:
        setup=load_setup()

    if confdir is None:
        confdir = Path(f'{os.getenv("PLATO_CONF_DATA_LOCATION")}/../../common/ccd/')

    camera = setup.camera.ID
    fm_id = cv.cam_name(name=camera).upper()
    fm_id_nozero = fm_id
    if fm_id[2]=='0':
        fm_id_nozero = fm_id[:2]+fm_id[3]

    sversion = f"v{str(version).zfill(2)}"
    inputfile = f"{confdir}/analogue_chain_limits_{temp}_{sversion}.yaml"

    limits_all = read_limits_from_yaml_file(inputfile)
    print(limits_all.keys())

    if limits_all['version']['version'] != version:
        print(f"CRITICAL: file version ({limits_all['version']['version']}) doesn't match the requested version ({version})")
        raise Exception("Version doesn't match")
    if limits_all['version']['temp'] != temp:
        print(f"CRITICAL: file temperature ({limits_all['version']['temp']}) doesn't match the requested temperature ({temp})")
        raise Exception("Temperature doesn't match")

    # Select 1 camera
    if camera in limits_all:
        cam_id = camera
    elif fm_id in limits_all:
        cam_id = fm_id
    elif fm_id_nozero in limits_all:
        cam_id = fm_id_nozero
    else:
        print(f"CRITICAL: CAMERA NOT FOUND, either by camera.ID of 'FM_ID'. Input: {camera} - {fm_id}")
        raise Exception("Camera not found in the input file (use e.g. brigand or FM1)")

    limits = {}
    limits['offsets'] = limits_all[cam_id]['ccd']['limits']['offset']
    limits['noise'] = limits_all[cam_id]['ccd']['limits']['noise']

    return limits

