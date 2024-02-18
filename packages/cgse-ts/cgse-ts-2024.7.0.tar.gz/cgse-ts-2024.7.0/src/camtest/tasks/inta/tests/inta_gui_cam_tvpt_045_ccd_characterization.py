from gui_executor.exec import exec_ui
from gui_executor.utypes import ListList, List
from pathlib import Path

from gui_executor.exec import exec_ui, Directory

UI_MODULE_DISPLAY_NAME = "4.- CAM-TVPT-045_CCD Characterization"

ICON_PATH = Path(__file__).parent.parent.resolve() / "icons"


@exec_ui(display_name="dataset#45-1", 
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def command_tvpt045_ccd_45_1(
    num_bias: int = 30,
    num_dark: int = 3,
    int_time: int = 900,
    description: str = "CAM-TVPT-045 CCD Characterization dataset#45-1",
):

    from camtest.commanding.cam_tvpt_045_ccd_characterization import cam_tvpt_045
    from camtest import execute

    execute(cam_tvpt_045, num_bias = num_bias, num_dark = num_dark, int_time = int_time,description = description)
    

@exec_ui(display_name="dataset#45-2", 
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def command_tvpt045_ccd_45_2(
    num_bias: int = 12,
    num_dark: int = 3,
    int_time: int = 900,
    description: str = "CAM-TVPT-045 CCD Characterization dataset#45-2",
):
    """
    Runs the TVPT045 test described in PLATO CAM Test Plan
    Args:
        num_bias: number of bias images
        num_dark: number of dark images at int_time exposure
        int_time: integration time in seconds (should be long for this saturation test)
        description: text that will be saved along with the OBSID to identify it, should contain the test plan item identifier (such as TVPT-XXX)
    """
    from camtest.commanding.cam_tvpt_045_ccd_characterization import cam_tvpt_045
    from camtest import execute

    execute(cam_tvpt_045, num_bias = num_bias, num_dark = num_dark, int_time = int_time, description = description)
    
       