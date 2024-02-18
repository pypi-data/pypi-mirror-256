import csv
import datetime
import logging

import numpy as np

from pathlib import Path
from time                                   import time, sleep

from egse.state                             import GlobalState
from egse.hk                                import get_housekeeping
from egse.system                            import EPOCH_1958_1970

from camtest import execute
from camtest import building_block

from gui_executor.exec import exec_ui

logger = logging.getLogger(__name__)

UI_MODULE_DISPLAY_NAME = "8 — Facility MGSE"

ICON_PATH = Path(__file__).parent.parent.resolve() / "icons"

@exec_ui(display_name="MGSE Measure Stability",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))

def mgse_map_stability(num_circles: int=range(19)):
    """ Test the stability of the gimbal by moving the gimbal through the entire FOV
    and measuring the stability for 5 seconds at pre-defined points
    
    Args:
        num_circles (int, optional): number of circles to draw. Defaults to range(19).
    """
    execute(sron_mgse_map_stability,
            num_circles=num_circles,
            description="Map MGSE Gimmbal stability across whole FoV")

@exec_ui(display_name="MGSE Measure Step Response",
         icons=(ICON_PATH / "command.svg", ICON_PATH / "command-selected.svg"))
def mgse_step_response(num_steps: int = range(19),
                       num_angles: int = range(36)):
    
    execute(sron_mgse_step_response,
            num_steps=num_steps,
            num_angles=num_angles,
            description="Measure MGSE Gimbal step response across whole FoV")
           
def calculate_circle_points(radii, points):
    circles = []
    
    for radius, point in zip(radii, points):
        t = np.linspace(0, 2 * np.pi, point, endpoint=False)
        x = radius * np.cos(t)
        y = radius * np.sin(t)
        circles.append(np.c_[x, y])
        
    return circles

def wait_until_position_reached(gimbal):
    sleep(1)
    while bool(int(gimbal.get_plane_status()) & 0x01):
        sleep(0.5)
    
         
@building_block
def sron_mgse_map_stability(num_circles):
    
    gimbal = GlobalState.setup.gse.ensemble.device
    
    r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    n = [1, 8, 8 ,8, 12, 12, 16, 16, 20, 24, 28, 28, 32, 36, 36, 40, 44, 48, 48, 52]
    
    circle_step = int(19 / num_circles)
    
    c = [r[value] for value in range(0, 19, circle_step)]
    p = [n[value] for value in range(0, 19, circle_step)]
    
    circles = calculate_circle_points(c, p)
    
    now = datetime.datetime.now()
    now_str = now.strftime("%m%d%Y%H%M%S")
    
    with open(f'/data/plato-ops/{now_str}-stability-map.csv', 'w') as f:

        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Timestamp', 'X commanded', 'Y commanded', 'X maximum error', 'Y maximum error', 'X max current', 'Y max current', 'X average error', 'Y average error', 'X std dev', 'Y std dev'])

        for circle in circles:
            for idx, _ in enumerate(circle):
                # 1. Move to next position
                logger.info(f"\nMoving to X: {circle[idx, 0]:2e}, Y: {circle[idx, 1]:2e}")
                gimbal.move_axes_degrees(circle[idx, 0], circle[idx, 1])

                wait_until_position_reached(gimbal)

                # 2. Hold for 4 seconds
                sleep(10)
                
                X = []
                X_power = []
                Y = []
                Y_power = []

                for i in np.linspace(0, 500, 500):
                    X.append(gimbal.get_error_position('X'))
                    Y.append(gimbal.get_error_position('Y'))
                    X_power.append(gimbal.get_actual_current('X'))
                    Y_power.append(gimbal.get_actual_current('Y'))
                    sleep(0.001)
                    
                X_max = np.amax(X)
                Y_max = np.amax(Y)

                X_avg = np.mean(X)
                Y_avg = np.mean(Y)
                
                X_std = np.std(X)
                Y_std = np.std(Y)
                
                X_power_max = np.amax(X_power)
                Y_power_max = np.amax(Y_power)

                # 4. Plot position and max offset in heatmap
                t = datetime.datetime.now()

                writer.writerow([t.strftime('%H:%M:%S.%f %m-%d-%Y'), circle[idx, 0], circle[idx, 1], X_max, Y_max, X_power_max, Y_power_max, X_avg, Y_avg, X_std, Y_std])
                
    gimbal.move_axes_degrees(0, 0)
    
    wait_until_position_reached(gimbal)
                
@building_block
def sron_mgse_step_response(num_steps, num_angles):
    
    gimbal = GlobalState.setup.gse.ensemble.device

    gimbal.enable_axes()
    gimbal.home_axes()

    step_size = 19 / num_steps
    
    steps = range(0, 19, num_steps)
    
    angle_step_size = 360 / num_angles
    
    angles = range(0, 360, angle_step_size)

    now = datetime.datetime.now()
    now_str = now.strftime("%m%d%Y%H%M%S")
    
    with open(f'/data/plato-ops/{now_str}-step-response.csv', 'w') as f:

        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Timestamp', 'Step', 'Angle', 'X commanded', 'Y commanded', 'X feedback', 'Y feedback', 'X error', 'Y error'])

        def write():
            t = datetime.datetime.now()
            
            writer.writerow([t.strftime('%H:%M:%S.%f %m-%d-%Y'),
                            step,
                            angle, 
                            gimbal.get_command_position('X'),
                            gimbal.get_command_position('Y'),
                            gimbal.get_actual_position('X'),
                            gimbal.get_actual_position('Y'),
                            gimbal.get_error_position('X'),
                            gimbal.get_error_position('Y')]) 

        def step(x, y):
            gimbal.move_axes_degrees(x, y)
            
            while bool(gimbal.get_plane_status() & 0x01):
                write()
                sleep(0.001)
            
            start_time = time()
            
            while (time() -  start_time) < 20:
                write()
                sleep(0.001)
        


        for angle in angles:
            for step in steps:
                x = step * np.cos(angle)
                y = step * np.sin(angle)
                
                print(f"Measuring step response to: {x}, {y}")
                
                step(x, y)
                
                sleep(5)
                
                print(f"Measuring return step response from: {x}, {y}")
                
                step(0, 0)
                
    gimbal.move_axes_degrees(0, 0)
    
    while bool(int(gimbal.get_plane_status) & 0x01):
        print(f"X: {gimbal.get_actual_position('X'):.2f}, Y: {gimbal.get_actual_position('X'):.2f}", end='\r')
        sleep(0.5)
        
    gimbal.disable_axes()