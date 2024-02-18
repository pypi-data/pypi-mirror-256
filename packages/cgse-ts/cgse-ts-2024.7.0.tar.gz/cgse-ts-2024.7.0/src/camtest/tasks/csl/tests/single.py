import os
from pathlib import Path

from gui_executor.exec import exec_ui, Directory

UI_MODULE_DISPLAY_NAME = "1 — Single position measurement"

ICON_PATH = Path(__file__).parent.parent.resolve() / "icons/"
DATA_PATH = Path(os.environ.get("PLATO_DATA_STORAGE_LOCATION"))


"""
# SINGLE CUBE ACQUISITION - NO PARAMETER (Bolting)
@exec_ui(display_name="CommandFixed",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def command_single_position():
    #  Image acquisition with fixed parameters, no pointing.
    # 
    # The parameters for the image acquisition are the following:
    #     * num_cycles=3,
    #     * row_start=4000,
    #     * row_end=4509,
    #     * rows_final_dump=4510,
    #     * ccd_order=[3, 3, 3, 3],
    #     * ccd_side="F",
    #     * exposure_time=0.2
    
    import camtest
    from camtest.commanding.cam_aat_050_single_no_pointing import single_no_pointing

    camtest.execute(single_no_pointing)
"""

# SINGLE CUBE ACQUISITION - PARAMETRIZED
@exec_ui(display_name="CommandFlexible",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def command_single_position_pointing(
    theta: float = 8.3,
    phi: float = 12.,
    num_cycles: int = 10,
    exposure_time: float = 0.2,
    n_rows: int = 500,
    attenuation: float = 0.00413,
):
    """ Image acquisition with a single pointing.

    Args:
        - theta: Boresight angle [degrees].
        - phi: Azimuth angle [degrees].
        - num_cycles: Number of exposures to acquire at each FOV position.
        - exposure_time: Exposure time [s].
        - n_rows: Number of rows to read (in partial-readout mode) around the visited position.
        - attenuation: Attenuation factor for the OGSE.
    """

    import camtest
    from camtest.commanding.cam_single_cube_int_sync import cam_single_cube_int_sync

    camtest.execute(cam_single_cube_int_sync, theta=theta, phi=phi, num_cycles=num_cycles, exposure_time=exposure_time, n_rows=n_rows, attenuation=attenuation)


# SINGLE CUBE ACQUISITION - EXPLORE GHOST
@exec_ui(display_name="CommandGhost",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def command_single_position_pointing_ghost(
    theta: float = 8.3,
    phi: float = 12,
    num_cycles: int = 5,
    exposure_time: float = 0.2,
    n_rows: int = 1000,
    attenuation: float = 0.00413,
    num_cycles_ghost: int = 10,
    exposure_time_ghost: float = 1.,
    attenuation_ghost: float = 1.,
):
    """ Image acquisition with a single pointing + data acquisition to explore potential ghosts.

    Args:
        - theta: Boresight angle [degrees].
        - phi: Azimuth angle [degrees].
        - num_cycles: Number of exposures to acquire data at the commanded FOV position.
        - exposure_time: Exposure time to acquire data at the commanded FOV position [s].
        - n_rows: Number of rows to read (in partial-readout mode) around the visited position.
        - attenuation: Attenuation factor for the OGSE to acquire data at the commanded FOV position.
        - num_cycles_ghost: Number of exposures to acquire at the position of the ghosts.
        - exposure_time_ghost: Exposure time to acquire data at the ghost positions [s].
        - attenuation_ghosts: Attenuation factor for the OGSE to acquire data at the ghost positions.
    """

    import camtest
    from camtest.commanding.cam_aat_050_single_ghost import cam_single_cube_int_sync_ghost

    camtest.execute(cam_single_cube_int_sync_ghost, theta=theta, phi=phi, num_cycles=num_cycles, exposure_time=exposure_time, n_rows=n_rows, attenuation=attenuation, num_cycles_ghost=num_cycles_ghost, exposure_time_ghost=exposure_time_ghost, attenuation_ghost=attenuation_ghost)


# ANALYSIS SINGLE CUBE ACQUISITION (invalid for 'ghost' script)
@exec_ui(display_name="Analyse",
         icons=(ICON_PATH / "analysis.svg", ICON_PATH / "analysis-selected.svg"))
def analyse_single_position(
        data_dir: Directory = DATA_PATH / "obs",
        obsid: int = 840,
        theta: float = 8.3,
        ref_size: float = 24.00,
):
    """ Analysis of a single-position observation.

    Args:
        - data_dir: Folder where the input data is (usually the 'obs' folder).
        - obsid: Obsid to analyse.
        - ref_size: Size of the ellipse in a reference measurement [pixels]. The size here will be compared to that one.

    Returns:
        - Ellipse size [pixels].
    """

    from camtest.analysis.functions.hartmann_utils import analysis_single_cube

    datadir = f"{str(data_dir)}/"

    esize = analysis_single_cube(obsid=obsid, datadir=datadir, ref_size=ref_size, layer_selection=None, theta=theta)

    print(f"Ellipse size = {esize}.")

    return esize


@exec_ui(display_name="ShowImage", use_gui_app=True,
         icons=(ICON_PATH / "analysis.svg", ICON_PATH / "analysis-selected.svg"))
def show_single_image(
        obsid: int = 364,
        cube_number: int = 0,
        layer_number: int = 2,
        extension_number: int = 2,
        data_dir: Directory = DATA_PATH / "obs",
        cuts_sigma: float = 2.
):
    """ Analysis of a single-position observation.

    Args:
        - obsid: Obsid to analyse.
        - cube_number : int: "FoV position number" (counting from 0)
        - layer_number: int: image acquisition number (at given FoV position, counting from 0)
        - extension_number=2: int: fits extension number. If in doubt, open the fits file hdu=fits.open(file) then hdu.info()
        - datadir=None: directory where the data are stored ("obs"). Default = env. variable "PLATO_LOCAL_DATA_LOCATION"
        - vsigma=2   : float : controls the contrast in the image (the lower vsigma, the higher the contrast)
    """
    from camtest.analysis.image_utils import show_single

    datadir = f"{str(data_dir)}/"

    thisplot = show_single(obsid=obsid, cube_number=cube_number, layer_number=layer_number, extension_number=extension_number, datadir=datadir, vsigma=cuts_sigma)

    return thisplot
