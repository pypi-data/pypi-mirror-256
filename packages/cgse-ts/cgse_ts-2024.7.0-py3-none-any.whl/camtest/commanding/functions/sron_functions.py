"""
SRON specific functions

Version 1.0 20211202 First version
        2.0 20211215 fov_angles_to_gimbal_rotations, gimbal_rotations_to_fov_angles both accept scalar and array inputs
        3.0 20230918 changed transformation based on plato-test-scripts#589
        
P. Royer, R. Huisman, S.N.Gomashie
"""

import numpy as np

def fov_angles_to_gimbal_rotations(theta,phi):
    """
    fov_angles_to_gimbal_rotations(theta,phi)

    INPUT
    theta, phi : field angles = [elevation, azimuth]

    OUTPUT
    SRON gimbal rotation angles

    REF.
    Adapted from mgse.sron_point_source_to_fov (see PLATO-SRON-PL- PLATO CAM TVAC Gimbal Characterization Report draft)
    """
    theta, phi = np.deg2rad(theta), np.deg2rad(phi)

    gimbal_rx = -(np.rad2deg(np.arctan2(-np.sin(phi) * np.sin(theta), np.cos(theta))))
    gimbal_ry = np.rad2deg(np.arcsin(np.cos(phi) * np.sin(theta)))

    return gimbal_rx, gimbal_ry


def gimbal_rotations_to_fov_angles(rotx, roty):
    """
    gimbal_rotations_to_fov_angles(rotx, roty)

    INPUT
    rotx, roty : SRON gimbal rotation angles

    OUTPUT
    theta, phi : field angles = [elevation, azimuth]

    REF.
    Adapted from mgse.sron_point_source_to_fov (see PLATO-SRON-PL- PLATO CAM TVAC Gimbal Characterization Report draft)
    """

    tolerance = 1.e-5

    flag_scalar_input = False
    if isinstance(roty, float):
        rotx = np.array([rotx])
        roty = np.array([roty])
        flag_scalar_input = True

    rotx, roty = np.deg2rad(rotx), np.deg2rad(roty)

    theta = np.arccos(np.cos(rotx) * np.cos(roty))

    phi = np.zeros_like(roty)

    sel = np.where(np.abs(roty) < tolerance)
    phi[sel] = np.sign(rotx[sel]) * np.pi/2.

    sel = np.where(np.abs(roty) > tolerance)
    
    phi[sel] = np.arctan2(-np.sin(-rotx[sel]) * np.cos(roty[sel]), np.sin(roty[sel]))
    
    theta, phi = np.rad2deg(theta), np.rad2deg(phi)

    if flag_scalar_input:
        theta, phi = theta[0], phi[0]

    return theta, phi
