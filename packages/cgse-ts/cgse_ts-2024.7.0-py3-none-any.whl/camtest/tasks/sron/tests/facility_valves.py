from typing import List
import logging

from pathlib import Path
from gui_executor.utypes import Callback

from egse.state                             import GlobalState

from camtest import execute
from camtest import building_block
from gui_executor.exec import exec_ui

UI_MODULE_DISPLAY_NAME = "10 — Facility Vacuum"

ICON_PATH = Path(__file__).parent.parent.resolve() / "icons"

logger = logging.getLogger(__name__)

def confirmation_option() -> List:
    return [True, False]

def default_choice() -> bool:
    return False

@exec_ui(display_name="Valves Check control",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def valve_check(full: Callback(confirmation_option, name=List, default=default_choice)):
    """ !!!WARNING: THIS TEST SCRIPT CAN OPEN ALL VALVES IN THE SYSTEM, INCLUDING THE VENT AND GATE VALVE!!!

    This testscript is meant to test the functionality of all valves in the system. It does the following:
    1. Opens a valve
    2. Asks the user to confirm the right valve was opened 
    (Users can use the front panel of the valve controller to verify valve states)
    3. Close the gate
    4. Repeat for all valves in the system

    Args:
        - full: boolean, indicating whether you want to test the gate and vent valve
    """
    execute(sron_facility_valve_check,
            full=full,
            description="Verify all facility valves")
        
    
@building_block
def sron_facility_valve_check(full=False):
    valves = GlobalState.setup.gse.beaglebone_vacuum.device
    
    # Go through every valve and confirm the right ones are opening
    # Set full argument to True to test the gate and vent valve as well
    
    valve_codes      = ['MV011', 'MV012', 'MV013', 'MV014', 'MV021', 'MV022', 'MV023', 'MV024']
    valve_names = ['LN2 Shroud', 'LN2 TEB-FEE', 'LN2 TEB-TOU', 'LN2 TRAP', 'N2 Shroud', 'N2 TEB-FEE', 'N2 TEB-TOU', 'N2 Trap']

    if full:
        valve_codes.extend(['MV002', 'MV001'])
        valve_names.extend(['Gate valve', 'Vent valve'])
    
    correct = {}

    for valve, name in zip(valve_codes, valve_names):
        print(f'Opening the {name} valve')
        valves.set_valve(valve, True)
        if input("Is the {} valve open? (y/n)").lower().startswith('y'):
            correct[name] = True
        else:
            correct[name] = False
            print(f"{name} has been connected incorrectly")
        valves.set_valve(valve, False)