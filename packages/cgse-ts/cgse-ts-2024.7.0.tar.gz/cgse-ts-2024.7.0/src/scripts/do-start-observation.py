#! /usr/bin/env python3

from egse.confman import ConfigurationManagerProxy
from camtest import start_observation

if __name__ == "__main__":

    # Test if there is an observation running

    with ConfigurationManagerProxy() as cm_proxy:
        obsid = cm_proxy.get_obsid().return_code

        if obsid:
            print(f"An observation is currently running [{obsid=}], end this observation before starting a new one.")
        else:
            obsid = start_observation("Starting an observation..")
            print(f"Observation {obsid=} started.")
