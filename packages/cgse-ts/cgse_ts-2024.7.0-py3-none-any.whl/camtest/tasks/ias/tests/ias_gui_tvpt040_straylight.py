from gui_executor.utypes import ListList, List
from pathlib import Path

from gui_executor.exec import exec_ui, Directory

UI_MODULE_DISPLAY_NAME = "12 — TVPT040 — Straylight"

ICON_PATH = Path(__file__).parent.parent.resolve() / "icons"


@exec_ui(display_name="Command",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def command_tvpt040_straylight(
        num_frames: int = 6,
        num_bck: int = 6,
        theta_list: list = [19., 20., 21., 22., 23.],
        phi_list: list = [-175.],
        fwc_list: list = [21, 100],
        split_ccd_sides: bool = False,
        description: str = 'TVPT040 Straylight',
):
    """
    Runs the TVPT040 test described in PLATO CAM Test Plan
    Args:
        num_frames: number of images
        num_bck: number of background images
        theta_list: list of [theta] positions in degrees in the focal plane
        phi_list: list of phi positions in degrees in the focal plane
        fwc_list: list of light intensities in terms of full-well fractions
        split_ccd_sides: boolean, indicates whether the CCD should be read one half at a time or not
        description: text that will be saved along with the OBSID to identify it, should contain the test plan item identifier (such as TVPT-XXX)
    """
    from camtest.commanding.cam_tvpt_040_test_693_straylight_ncam import cam_tvpt_040_straylight
    from camtest import execute

    execute(cam_tvpt_040_straylight, num_frames=num_frames, num_bck=num_bck,
            fwc_list=fwc_list, theta_list=theta_list, phi_list=phi_list, split_ccd_sides=split_ccd_sides,
            description=description)
