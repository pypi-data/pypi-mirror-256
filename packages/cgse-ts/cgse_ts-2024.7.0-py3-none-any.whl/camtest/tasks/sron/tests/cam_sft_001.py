import csv
import datetime

import numpy as np

from pathlib import Path
from time                                   import time, sleep

from egse.state                             import GlobalState
from egse.hk                                import get_housekeeping
from egse.system                            import EPOCH_1958_1970

from camtest import end_observation
from camtest import start_observation

from gui_executor.exec import exec_ui

UI_MODULE_DISPLAY_NAME = "4 - CAM-SFT-001 - Short functional test CAM"

ICON_PATH = Path(__file__).parent.parent.resolve() / "icons"