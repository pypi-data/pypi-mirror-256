import numpy as np
from camtest import load_setup, submit_setup
import pandas

# setup = load_setup(setup_id=85, site_id="CSL1", from_disk=True)
# setup = load_setup()
# print(setup.get_id(), setup.site_id)

def setup_fee_limits(setup=None, version=None, temp='ambient', confdir=None):
    """

    """
    import os
    from pathlib import Path

    # FIX THE INPUTS
    if setup is None:
        setup=load_setup()

    if confdir is None:
        confdir = Path(f'{os.getenv("PLATO_CONF_DATA_LOCATION")}/../../common/n-fee/')

    # GLOBAL SETTINGS

    # N vs F-FEE (string appearing in the HK name)
    fee = "NFEE"
    # Rounding of the output
    rounding = 3
    # Camera ID : taken from the setup
    camera = setup.camera.ID
    # reformatted version number
    sversion = f"v{str(version).zfill(2)}"

    # Generic HK entries to check
    hk_keys = ["CCD", "CLK", "AN1", "AN2", "AN3", "DIG"]

    # Observing modes
    modes = ["on_mode", "standby_mode", "full_image_mode_readout", "full_image_mode_integration"]
    # Current & Power strings
    ip = ["current", "power"]
    hvip = {"voltage": "V", "current": "I", "power": "P"}

    mode_keys = [f"voltage_{temp}"]
    for mode in modes:
        for observable in ip:
            mode_keys.append(f"{observable}_{mode}_{temp}")

    # LOAD THE CONFIGURATION FILE
    xlfile = f"{confdir}/sft_limits_fee_hk_{camera}_{sversion}.xlsx"
    pdf = pandas.read_excel(xlfile, sheet_name=temp, usecols="A:C", names=["key", "reference", "tolerance"])


    # FORMAT THE LIMITS ACCORDING TO THE INPUT CONFIGURATION FILE
    limits = {}

    for mode_key in mode_keys:

        index_start = pdf.key[pdf.key==mode_key].index.tolist()[0]

        vip = mode_key.split('_')[0]

        limits[mode_key] = {}
        limits[mode_key]["tolerance"] = pdf.tolerance[index_start]

        print(f"{mode_key:20s}  tolerance:{limits[mode_key]['tolerance']}")

        for i,akey in enumerate(hk_keys):
            key = f"GAEU_{hvip[vip]}_{akey}_{fee}"
            limits[mode_key][key] = [np.round(pdf.reference[index_start+i+1],rounding), np.round(pdf.tolerance[index_start+i+1],rounding)]
            print(f"{key} [{limits[mode_key][key][0]:6.3f},{limits[mode_key][key][1]:.3f}]")

    # ASSEMBLE THE RELEVANT PART OF THE SETUP
    hsetup = {}
    hsetup["voltages"] = limits[f"voltage_{temp}"]
    hsetup["currents"] = {}
    hsetup["powers"] = {}

    for mode in modes:
        hsetup["currents"][mode] = limits[f"current_{mode}_{temp}"]
        hsetup["powers"][mode] = limits[f"power_{mode}_{temp}"]

    return hsetup


