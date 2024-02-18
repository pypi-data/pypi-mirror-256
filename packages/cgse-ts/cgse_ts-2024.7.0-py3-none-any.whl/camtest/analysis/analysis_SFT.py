import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from camtest.analysis import convenience as cv
from camtest import load_setup
from camtest.analysis.observation import Observation

from camtest.analysis import image_utils as iu
from astropy.io import fits, ascii
from astropy.table import Table


def addstring(sref, s, verbose=True):
    """
    adds s to sref
    if verbose is True, prints s
    """
    sref = sref + s+'\n'
    if verbose:
        print(s)
    return sref


def analysis_SFT_HK(obsid, temp, camera=None, data_dir=None, output_dir=None, setup=None, verbose=True, showplots=True):
    """
    obsid : obsid. int.
    temp : temperature environment, in ['ambient', 'tvac']
    camera : camera ID, as in the data directory name ("achel", "brigand", "chimay", ..._
             default : setup.camera.ID
    data_dir : full path to the "/obs/" directory above the obsid-directory
    output_dir  : ouput directory (for both images & text file)
    setup : egse.setup.Setup object
    verbose : boolean, triggers print statements
    showplots : displays the plots during the execution, or saves them without display
    """
    # BASIC VARIABLE DECLARATIONS
    lightgray = (0.75, 0.75, 0.75)
    lightblue = (0.5, 0.5, 1.0)
    pink      = (1., 0.5, 0.75)
    stringout = ""
    sobsid = str(obsid).zfill(5)

    # NFEE MODES DEFINITIONS
    hmode = {"ON":0, "ON_MODE":0, "STANDBY_MODE":4, "STANDBY":4, "FULL_IMAGE":5, "FULL_IMAGE_MODE":5}

    # DEFAULTS FROM THE SETUP
    if setup is None:
        setup = load_setup()

    if camera is None:
        camera = setup.camera.ID

    temp = temp.lower()
    if temp == 'cold' or temp == 'cryo':
        temp = 'tvac'

    print(f"{setup.get_id()=}, {setup.site_id=}  {camera=}  temperature={temp}")

    # OBSERVATION OBJECT
    if data_dir is None:
        # if PLATO_LOCAL_DATA_LOCATION is defined; else set data_dir to "/.../obs/"
        obs = Observation(obsid=obsid, data_dir=None)
    else:
        # if PLATO_LOCAL_DATA_LOCATION is defined; else set data_dir to "/.../obs/"
        obs = Observation(obsid=obsid, data_dir=data_dir)

    # FRAME TIMES
    # If frames exist, start of image acquisition = t0 = first frame time = start of readout of the first frame.
    # Else t0 = start of the N-FEE-HK
    try:
        ftimes = np.sort(obs.get_frame_times())
        t0 = ftimes[0]
        relftimes = ftimes-t0
        hkonly = False
    except:
        hkonly = True

    #########
    # NFEE-HK
    #########
    device = "N-FEE-HK"

    hkn = obs.get_hk(device=device, verbose=False)

    if hkonly:
        t0 = hkn["finetime"][0]

    nreltime = hkn["finetime"] - t0
    dtn = np.diff(nreltime)

    nfeemode = hkn["NFEE_MODE"]

    ########
    # AEU HK
    ########
    device = "AEU-CRIO"

    hkt = obs.get_hk(device=device, verbose=False)

    reltime = hkt["finetime"]-t0

    ##################
    # TEST SEQUENCING
    ##################
    # Extracting the time periods where the NFEE is ON, STANDBY, DUMP, FULL_IMAGE
    # DUMP cannot be extracted from the csv telemetry at the moment (see ticket plato-common-egse #2532).
    # It could be FULL_IMAGE when not measuring, but it's actually not used.

    # Start of ON-MODE
    t_on = nreltime[:-1][np.where(dtn < 7.)[0][0]]
    reach_on = True

    # End of the test
    t_end = max(reltime[-1], nreltime[-1])

    try:
        # Start of STANDBY-MODE
        t_stdby = nreltime[np.where(nfeemode == hmode["STANDBY"])[0][0]]
        reach_stdby = True
    except:
        reach_stdby = False
        t_stdby = t_end
    try:
        # Start of FULL-IMAGE-MODE (dump)
        t_full = nreltime[np.where(nfeemode == hmode["FULL_IMAGE"])[0][0]]
        reach_full = True
    except:
        reach_full = False
        t_full = t_end

    if (t_stdby == t_on) or (t_full == t_on):
        reach_on = False
        t_on = t_end

    t_start = min(reltime[0], nreltime[0])

    s = f"Reach {'ON_MODE':15s}: {t_on:8.2f}\nReach {'STANDBY_MODE':15s}: {t_stdby:8.2f}\nReach FULL_IMAGE_MODE: {t_full:8.2f}\n{'Start img acq. (def)':21s}: {0.:8.2f}\n{'End':21s}: {t_end:8.2f}"
    stringout = addstring(stringout, s, verbose=verbose)

    #####################################
    # LOAD TM LIMITS FROM THE CONFIG FILE
    #####################################

    v_keys = ["GAEU_V_CCD_NFEE", "GAEU_V_AN1_NFEE", "GAEU_V_AN2_NFEE", "GAEU_V_AN3_NFEE", "GAEU_V_CLK_NFEE", "GAEU_V_DIG_NFEE"]
    vn_keys = ["NFEE_VCCD", "NFEE_VAN1_R", "NFEE_VAN2_R", "NFEE_VAN3_R", "NFEE_VCLK_R", "NFEE_VDIG"]

    i_keys = ["GAEU_I_CCD_NFEE", "GAEU_I_AN1_NFEE", "GAEU_I_AN2_NFEE", "GAEU_I_AN3_NFEE", "GAEU_I_CLK_NFEE", "GAEU_I_DIG_NFEE"]
    p_keys = ["GAEU_P_CCD_NFEE", "GAEU_P_AN1_NFEE", "GAEU_P_AN2_NFEE", "GAEU_P_AN3_NFEE", "GAEU_P_CLK_NFEE", "GAEU_P_DIG_NFEE"]

    limits = {}

    setup_ref = setup.camera.fee.power_consumption[temp]

    vtol_type = setup_ref.voltages.tolerance
    if vtol_type == "absolute":
        for v_key in v_keys:
            ref = setup_ref.voltages[v_key]
            limits[v_key] = [ref[0]-ref[1], ref[0]+ref[1]]
        for vn_key in vn_keys:
            ref = setup_ref.voltages[vn_key]
            limits[vn_key] = [ref[0] - ref[1], ref[0] + ref[1]]
    elif vtol_type == "relative":
        for v_key in v_keys:
            ref = setup_ref.voltages[v_key]
            limits[v_key] = [ref[0]*(1-ref[1]/100.), ref[0] * (1+ref[1]/100.)]
        for vn_key in vn_keys:
            ref = setup_ref.voltages[vn_key]
            limits[vn_key] = [ref[0]*(1-ref[1]/100.), ref[0] * (1+ref[1]/100.)]

    for i_key,p_key in zip(i_keys, p_keys):
        limits[i_key] = {}
        limits[p_key] = {}

    for feemode in ["on_mode", "standby_mode", "full_image_mode_readout", "full_image_mode_integration"]:

        itol_type = setup_ref.currents[feemode].tolerance
        if itol_type == "relative":
            for i_key in i_keys:
                ref = setup_ref.currents[feemode][i_key]
                limits[i_key][feemode] = [(ref[0]*(1-ref[1]/100.)) / 1000., (ref[0] * (1+ref[1]/100.)) / 1000.]
        else:
            # print("Setup indicates an absolute error specification for the current")
            # raise(NotImplementedError)
            for i_key in i_keys:
                ref = setup_ref.currents[feemode][i_key]
                limits[i_key][feemode] = [(ref[0]-ref[1]) / 1000., (ref[0]+ref[1]) / 1000.]

        ptol_type = setup_ref.powers[feemode].tolerance
        if ptol_type == "relative":
            for p_key in p_keys:
                ref = setup_ref.powers[feemode][p_key]
                limits[p_key][feemode] = [(ref[0] * (1 - ref[1] / 100.)), (ref[0] * (1 + ref[1] / 100.))]
        else:
            # print("Setup indicates an absolute error specification for the power")
            # raise(NotImplementedError)
            for p_key in p_keys:
                ref = setup_ref.powers[feemode][p_key]
                limits[p_key][feemode] = [(ref[0] - ref[1]), (ref[0] + ref[1])]

    ##################
    # TM STATS / FEE MODE
    ##################

    hok = {True: " OK", False: "NOK"}

    overallvok, overallvnok, overalliok, overallpok = True, True, True, True

    ### ON MODE  ###
    if reach_on:
        s = "NFEE ON-MODE"
        stringout = addstring(stringout, s, verbose=verbose)

        feemode = 'on_mode'
        tsel = np.where((reltime>=t_on) & (reltime <=t_stdby))
        tnsel = np.where((nreltime>=t_on) & (nreltime <=t_stdby))

        allvok, allvnok, alliok, allpok = True, True, True, True
        for v_key,vn_key, i_key, p_key in zip(v_keys, vn_keys, i_keys, p_keys):
            V = np.round(np.mean(hkt[v_key][tsel]), 3)
            I = np.round(np.mean(hkt[i_key][tsel]), 3)
            P = np.round(V * I, 3)
            Vn = np.round(np.mean(hkn[vn_key][tnsel]), 3)

            vlow, vhigh = limits[v_key][0], limits[v_key][1]
            if vlow > vhigh:
                vlow, vhigh = limits[v_key][1], limits[v_key][0]

            vnlow, vnhigh = limits[vn_key][0], limits[vn_key][1]
            if vnlow > vnhigh:
                vnlow, vnhigh = limits[vn_key][1], limits[vn_key][0]

            ilow, ihigh = limits[i_key][feemode][0], limits[i_key][feemode][1]
            if ilow > ihigh:
                ilow, ihigh = limits[i_key][feemode][1], limits[i_key][feemode][0]

            plow, phigh = limits[p_key][feemode][0], limits[p_key][feemode][1]
            if plow > phigh:
                plow, phigh = limits[p_key][feemode][1], limits[p_key][feemode][0]

            s = f"      {v_key:15s} {V:7.3f} in [{vlow:7.3f},{vhigh:7.3f}] {hok[(V >= vlow) & (V <= vhigh)]}      {vn_key:15s} {Vn:7.3f} in [{vnlow:7.3f},{vnhigh:7.3f}] {hok[(Vn >= vnlow) & (Vn <= vnhigh)]}      {i_key:15s} {I:7.3f} in [{ilow:7.3f},{ihigh:7.3f}] {hok[(I >= ilow) & (I <= ihigh)]}      {p_key:15s} P ={P:7.3f} in [{plow:7.3f},{phigh:7.3f}] {hok[(P >= plow) & (P <= phigh)]}"
            stringout = addstring(stringout, s, verbose=verbose)

            if (V < vlow) | (V > vhigh): allvok = False
            if (I < ilow) | (I > ihigh): alliok = False
            if (P < plow) | (P > phigh): allpok = False
            if (Vn < vnlow) | (Vn > vnhigh): allvnok = False

        s = f"      AEU Voltages OK: {str(allvok):5s} {' ' * 24}       FEE Voltages OK: {str(allvnok):5s} {' ' * 30} Currents OK: {alliok} {' ' * 34}  Powers OK: {allpok}"
        stringout = addstring(stringout, s, verbose = verbose)

        overallvok, overallvnok, overalliok, overallpok = allvok, allvnok, alliok, allpok

    ### STANDBY MODE  ###
    if reach_stdby:
        s = "NFEE STANDBY-MODE"
        stringout = addstring(stringout, s, verbose=verbose)

        feemode = "standby_mode"
        tsel = np.where((reltime >= t_stdby) & (reltime <= t_full))
        tnsel = np.where((nreltime >= t_stdby) & (nreltime <= t_full))

        allvok, allvnok, alliok, allpok = True, True, True, True
        for v_key, vn_key, i_key, p_key in zip(v_keys, vn_keys, i_keys, p_keys):
            V = np.round(np.mean(hkt[v_key][tsel]), 3)
            I = np.round(np.mean(hkt[i_key][tsel]), 3)
            P = np.round(V * I, 3)
            Vn = np.round(np.mean(hkn[vn_key][tnsel]), 3)

            vlow, vhigh = limits[v_key][0], limits[v_key][1]
            if vlow > vhigh:
                vlow, vhigh = limits[v_key][1], limits[v_key][0]

            vnlow, vnhigh = limits[vn_key][0], limits[vn_key][1]
            if vnlow > vnhigh:
                vnlow, vnhigh = limits[vn_key][1], limits[vn_key][0]

            ilow, ihigh = limits[i_key][feemode][0], limits[i_key][feemode][1]
            if ilow > ihigh:
                ilow, ihigh = limits[i_key][feemode][1], limits[i_key][feemode][0]

            plow, phigh = limits[p_key][feemode][0], limits[p_key][feemode][1]
            if plow > phigh:
                plow, phigh = limits[p_key][feemode][1], limits[p_key][feemode][0]

            #s = f"      {v_key:15s} {V:7.3f} in [{vlow:7.3f},{vhigh:7.3f}] {hok[(V >= vlow) & (V <= vhigh)]}      {vn_key:15s} {Vn:7.3f} in [{vlow:7.3f},{vhigh:7.3f}] {hok[(Vn >= vlow) & (Vn <= vhigh)]}      {i_key:15s} {I:7.3f} in [{ilow:7.3f},{ihigh:7.3f}] {hok[(I >= ilow) & (I <= ihigh)]}       P=V*I {V * I:7.3f}"
            s = f"      {v_key:15s} {V:7.3f} in [{vlow:7.3f},{vhigh:7.3f}] {hok[(V >= vlow) & (V <= vhigh)]}      {vn_key:15s} {Vn:7.3f} in [{vnlow:7.3f},{vnhigh:7.3f}] {hok[(Vn >= vnlow) & (Vn <= vnhigh)]}      {i_key:15s} {I:7.3f} in [{ilow:7.3f},{ihigh:7.3f}] {hok[(I >= ilow) & (I <= ihigh)]}      {p_key:15s} P ={P:7.3f} in [{plow:7.3f},{phigh:7.3f}] {hok[(P >= plow) & (P <= phigh)]}"
            stringout = addstring(stringout, s, verbose=verbose)

            if (V < vlow) | (V > vhigh): allvok = False
            if (I < ilow) | (I > ihigh): alliok = False
            if (P < plow) | (P > phigh): allpok = False
            if (Vn < vnlow) | (Vn > vnhigh): allvnok = False

        s = f"      AEU Voltages OK: {str(allvok):5s} {' ' * 24}       FEE Voltages OK: {str(allvnok):5s} {' ' * 30} Currents OK: {alliok} {' ' * 34}  Powers OK: {allpok}"
        stringout = addstring(stringout, s, verbose=verbose)

        overallvok, overallvnok = overallvok & allvok, overallvnok & allvnok
        overalliok, overallpok  = overalliok & alliok, overallpok & allpok

    ######################################
    ### FULL_IMAGE_MODE - ACQUISITION  ###
    ######################################
    if reach_full:
        # = excluding the initial & ending period in DUMP MODE
        tsel = np.where((reltime >= 0.) & (reltime <= t_end))
        tnsel = np.where((nreltime >= 0.) & (nreltime <= t_end))

        # 1. identify modes
        i_key = "GAEU_I_CLK_NFEE"
        current = hkt[i_key][tsel]
        try:
            modes = cv.kde_modes(current, bw_method=0.1, kde_threshold=None, verbose=False)
        except:
            s = "WARNING : NO BIMODAL DISTRIBUTION OF CURRENT IDENTIFIED IN FULL_IMAGE_MODE"
            stringout = addstring(stringout, s, verbose=verbose)

            modes = [np.arange(len(current))]

        if len(modes)!=2:
            s = f"WARNING : CURRENT DOES NOT EXHIBIT A BIMODAL DISTRIBUTION IN FULL_IMAGE_MODE: nmodes = {len(modes)}"
            stringout = addstring(stringout, s, verbose=verbose)

        # 2. map the modes to readout or integration
        modes_i = np.array([np.mean(current[mode]) for mode in modes])
        hmodes = {}
        hmodes['full_image_mode_readout'] = modes[np.where(modes_i == max(modes_i))[0][0]]
        hmodes['full_image_mode_integration'] = modes[np.where(modes_i == min(modes_i))[0][0]]

        readoutornot = np.zeros_like(reltime) - 1
        readoutornot[np.array(tsel[0])[hmodes['full_image_mode_readout']]] = 1
        readoutornot[np.array(tsel[0])[hmodes['full_image_mode_integration']]] = 0
        readoutornot = np.round(readoutornot / 10. + 0.4, 1)

        # 3. Apply to all
        hfeemode = {'full_image_mode_readout':"FULL_IMAGE_MODE_READOUT", 'full_image_mode_integration':"FULL_IMAGE_MODE_INTEGRATION"}
        for feemode in ['full_image_mode_integration', 'full_image_mode_readout']:
            s = f"{hfeemode[feemode]}"
            stringout = addstring(stringout, s, verbose=verbose)

            allvok, allvnok, alliok, allpok = True, True, True, True
            for v_key, vn_key, i_key, p_key in zip(v_keys, vn_keys, i_keys, p_keys):
                V = np.round(np.mean(hkt[v_key][tsel][hmodes[feemode]]), 3)
                I = np.round(np.mean(hkt[i_key][tsel][hmodes[feemode]]), 3)
                P = np.round(V * I, 3)
                Vn = np.round(np.mean(hkn[vn_key][tnsel]), 3)

                vlow, vhigh = limits[v_key][0], limits[v_key][1]
                if vlow > vhigh:
                    vlow, vhigh = limits[v_key][1], limits[v_key][0]

                vnlow, vnhigh = limits[vn_key][0], limits[vn_key][1]
                if vnlow > vnhigh:
                    vnlow, vnhigh = limits[vn_key][1], limits[vn_key][0]

                ilow, ihigh = limits[i_key][feemode][0], limits[i_key][feemode][1]
                if ilow > ihigh:
                    ilow, ihigh = limits[i_key][feemode][1], limits[i_key][feemode][0]

                plow, phigh = limits[p_key][feemode][0], limits[p_key][feemode][1]
                if plow > phigh:
                    plow, phigh = limits[p_key][feemode][1], limits[p_key][feemode][0]

                #s = f"      {v_key:15s} {V:7.3f} in [{vlow:7.3f},{vhigh:7.3f}] {hok[(V >= vlow) & (V <= vhigh)]}      {vn_key:15s} {Vn:7.3f} in [{vlow:7.3f},{vhigh:7.3f}] {hok[(Vn >= vlow) & (Vn <= vhigh)]}      {i_key:15s} {I:7.3f} in [{ilow:7.3f},{ihigh:7.3f}] {hok[(I >= ilow) & (I <= ihigh)]}       P=V*I {V * I:7.3f}"
                s = f"      {v_key:15s} {V:7.3f} in [{vlow:7.3f},{vhigh:7.3f}] {hok[(V >= vlow) & (V <= vhigh)]}      {vn_key:15s} {Vn:7.3f} in [{vnlow:7.3f},{vnhigh:7.3f}] {hok[(Vn >= vnlow) & (Vn <= vnhigh)]}      {i_key:15s} {I:7.3f} in [{ilow:7.3f},{ihigh:7.3f}] {hok[(I >= ilow) & (I <= ihigh)]}      {p_key:15s} P ={P:7.3f} in [{plow:7.3f},{phigh:7.3f}] {hok[(P >= plow) & (P <= phigh)]}"
                stringout = addstring(stringout, s, verbose=verbose)

                if (V < vlow) | (V > vhigh): allvok = False
                if (I < ilow) | (I > ihigh): alliok = False
                if (P < plow) | (P > phigh): allpok = False
                if (Vn < vnlow) | (Vn > vnhigh): allvnok = False

            s = f"      AEU Voltages OK: {str(allvok):5s} {' ' * 24}       FEE Voltages OK: {str(allvnok):5s} {' ' * 30} Currents OK: {alliok} {' ' * 34}  Powers OK: {allpok}"
            stringout = addstring(stringout, s, verbose=verbose)

            overallvok, overallvnok = overallvok & allvok, overallvnok & allvnok
            overalliok, overallpok = overalliok & alliok, overallpok & allpok


    ##################
    # OVERALL TM STATS
    ##################

    s = f"\nAll V-AEU OK: {overallvok}"
    stringout = addstring(stringout, s, verbose=verbose)
    s = f"All V-FEE OK: {overallvnok}"
    stringout = addstring(stringout, s, verbose=verbose)
    s = f"All I OK:     {overalliok}"
    stringout = addstring(stringout, s, verbose=verbose)
    s = f"All P OK:     {overallpok}"
    stringout = addstring(stringout, s, verbose=verbose)

    if overallvok & overallvnok & overalliok & overallpok:
        s = f"\nHK: All values OK. IF offsets & readout noise OK, you can PROCEED."
    else:
        s = f"\nHK: Some values deserve attention. STOP for analysis"
    str_hk_ok = s

    stringout = addstring(stringout, s, verbose=verbose)

    ##################
    # OUTPUT TM STATS
    ##################

    output_filename = output_dir + f"sft_analysis_{camera}_{sobsid}_HK_checks.txt"
    file = open(output_filename, 'w')
    file.write(stringout)
    file.close()

    print(stringout+'\n')

    ###############
    # PLOT VOLTAGES
    ###############

    if not showplots: plt.ioff()

    fontsize = 15
    # plot_xlim = [t_on - 100, t_end + 20]
    plot_xlim = [t_start - 100, t_end + 20]

    c=-1
    fig = plt.figure(figsize=(14, 14))
    gs = GridSpec(2, 1)

    axv = fig.add_subplot(gs[0, 0])

    ytf = [-10,40]
    if not hkonly:
        plt.plot([relftimes[0], relftimes[0]], ytf, c=lightgray, ls='--', label='Frames')
        for tf in relftimes[1:]:
            plt.plot([tf,tf], ytf, c=lightgray, ls='--')

    plt.plot([t_on, t_on], ytf, c=lightblue, ls='--')
    plt.plot([t_stdby,t_stdby], ytf, c=lightblue, ls='--')
    plt.plot([t_full,t_full], ytf, c=lightblue, ls='--', label="NFEE mode transitions")

    for key, nkey in zip(v_keys, vn_keys):
        c+=1
        plt.plot(reltime, hkt[key], c=cv.get_color(c), ls="-", marker=".", lw=2, label=f"{key}")# {np.mean(hkt[key]):.2f} +- {np.std(hkt[key]):.2f}")
        plt.plot(nreltime, hkn[nkey], c=cv.get_color(c), ls="-", marker="o", lw=2, label=f"{nkey}", alpha=0.5)# {np.mean(hkt[key]):.2f} +- {np.std(hkt[key]):.2f}")

    c+=1
    plt.plot(nreltime, hkn["NFEE_MODE"], c=cv.get_color(c), ls="-", marker="o", lw=2, label=f"NFEE_MODE")

    plt.title(f"{camera} {sobsid} AEU-CRIO & NFEE - Voltages", size=fontsize)
    plt.xlabel("Relative time [s]", size=fontsize)
    plt.ylabel("Voltages [V]", size=fontsize)
    plt.grid(alpha=0.25)
    plt.legend()
    if showplots:
        plt.show()

    ###############
    # PLOT CURRENTS
    ###############
    c=-1

    axi = fig.add_subplot(gs[1, 0])

    ytf = [-0.2,1.]
    if not hkonly:
        plt.plot([relftimes[0], relftimes[0]], ytf, c=lightgray, ls='--', label='Frames')
        for tf in relftimes[1:]:
            plt.plot([tf,tf],ytf, c=lightgray, ls='--')

    plt.plot([t_on, t_on], ytf, c=lightblue, ls='--')
    plt.plot([t_stdby, t_stdby], ytf, c=lightblue, ls='--')
    plt.plot([t_full, t_full], ytf, c=lightblue, ls='--', label="NFEE mode transitions")

    for key in i_keys:
        c+=1
        plt.plot(reltime, hkt[key], c=cv.get_color(c), ls="-", marker=".", lw=2, label=f"{key}")# {np.mean(hkt[key]):.2f} +- {np.std(hkt[key]):.2f}")

    c+=1
    plt.plot(nreltime, hkn["NFEE_MODE"] / 5., c=cv.get_color(c), ls="-", marker="o", lw=2, label=f"NFEE_MODE/5")

    axv.get_shared_x_axes().join(axv, axi)

    plt.plot(reltime, readoutornot, c=lightgray, ls='--', marker='.', label="Analysis S/W Read vs Integ.")

    plt.title(f"{camera} {sobsid} {device} - Currents", size=fontsize)
    plt.xlabel("Relative time [s]", size=fontsize)
    plt.ylabel("Currents [A]"
               "", size=fontsize)
    plt.grid(alpha=0.25)
    plt.legend()
    plt.xlim(plot_xlim[0],plot_xlim[1])

    if showplots:
        plt.show()

    viplotname = output_dir+f"sft_analysis_{camera}_{sobsid}_HK_{device}_VI.png"
    plt.savefig(viplotname)

    if not showplots:
        plt.ion()

    if verbose:
        print(f"\nGraphical and numerical results can be found in\n{output_filename}\n{viplotname}")#\n{iplotname}")

    return str_hk_ok


def analysis_SFT_img(obsid, temp, camera=None, data_dir=None, output_dir=None, setup=None, verbose=True, showplots=True, func=None, layer=2):
    """
    obsid, camera=None, data_dir=None, output_dir=None, setup=None, verbose=True, showplots=True, layer=2

    obsid : obsid
    temp : temperature environment, in ['ambient', 'tvac']
    camera : camera ID, as in the data directory name ("achel", "brigand", "chimay", ..._
             default : setup.camera.ID
    data_dir : full path to the "/obs/" directory above the obsid-directory
    output_dir  : ouput directory (for both images & text file)
    setup : setup object
    verbose : boolean, triggers print statements
    showplots : displays the plots during the execution, or saves them without display
    func      : function to combine the ron & offset statistics gathered on individual columns (default = numpy.mean)
    layer=2 : layer to be displayed in the output images
    """
    sobsid = str(obsid).zfill(5)

    # DEFAULTS FROM THE SETUP
    # -----------------------
    if setup is None:
        setup = load_setup()

    if camera is None:
        camera = setup.camera.ID

    # IDENTIFY THE INPUT DATAFILE(S)
    # ------------------------------
    obsidir = cv.fileSelect([f'{sobsid}'], location=data_dir)[0] + '/'
    filenames = cv.fileSelect([f'{sobsid}_', 'cube', 'fits'], location=data_dir + obsidir)
    ffilenames = [data_dir + obsidir + filename for filename in filenames]

    if verbose:
        cv.print1(ffilenames)

    split=False
    if len(ffilenames)>1:
        print(f"Multiple cubes found. Assuming E & F were split")
        split = True

    # IMAGE DISPLAYS. RAW, OFFSET SUBTRACTED AND AVERAGE ROW & COLUMN PROFILES
    # ------------------------------------------------------------------------

    if not showplots:
        plt.ioff()

    ln = layer
    full = True
    if not split:
        cn = 0
        bckgndsub = False
        offsetsub = False
        img_4 = iu.show_allccds(cn, ln, filenames=ffilenames, vsigma=2.5, obsid=obsid, full=full, bckgndsub=bckgndsub,
                                offsetsub=offsetsub, setup=setup)
        if showplots: plt.show()
        plt.savefig(output_dir + f"sft_analysis_{camera}_{sobsid}_img_raw.png")
        offsetsub = True
        img_4off = iu.show_allccds(cn, ln, filenames=ffilenames, vsigma=0.5, obsid=obsid, full=full, bckgndsub=False,
                                   offsetsub=offsetsub, setup=setup, vmin=-10, vmax=10)
        if showplots: plt.show()
        plt.savefig(output_dir + f"sft_analysis_{camera}_{sobsid}_img_offsetSubtracted.png")

        # Average rows & columns
        fig, mrows, mcols = iu.show_allccds_avg_rowcol(cube_number=cn, layer_number=ln, filenames=ffilenames, full=full,
                                                       bckgndsub=False, offsetsub=False, setup=setup)
        if showplots: plt.show()
        plt.savefig(output_dir + f"sft_analysis_{camera}_{sobsid}_img_avg_rows_and_columns.png")
    else:
        bckgndsub = False
        offsetsub = False
        img_4 = iu.show_sum_all_cubes(layer_number=ln, filenames=ffilenames, vsigma=2, obsid=obsid, full=full, bckgndsub=bckgndsub,
                           offsetsub=offsetsub, setup=setup)
        if showplots: plt.show()
        plt.savefig(output_dir + f"sft_analysis_{camera}_{sobsid}_img_raw.png")
        offsetsub = True
        img_4off = iu.show_sum_all_cubes(layer_number=ln, filenames=ffilenames, vsigma=2, obsid=obsid, full=full, bckgndsub=bckgndsub,
                           offsetsub=offsetsub, setup=setup)
        if showplots: plt.show()
        plt.savefig(output_dir + f"sft_analysis_{camera}_{sobsid}_img_offsetSubtracted.png")

        # TODO: Average rows & columns
        fig, mrows, mcols = None, None, None
        print("Execution of E, then F side measurements: computation & display of average rows & cols NotImplemented")

    if not showplots:
        plt.ion()

    # OFFSETS AND READOUT NOISE ON THE VARIOUS IMAGE PARTS
    # ----------------------------------------------------

    if not split:
        str_img_ok = offsets_and_ron(obsid, temp, filename=ffilenames[0], output_dir=output_dir, camera=camera, setup=setup, func=func, verbose=verbose)
    else:
        str_img_ok = ""
        for cn in range(len(ffilenames)):
            str_cn = offsets_and_ron(obsid, temp, filename=ffilenames[cn], output_dir=output_dir, camera=camera, setup=setup, func=func, postfix=str(cn).zfill(2), verbose=verbose)
            str_img_ok += f"Cube {cn}: {str_cn}\n"

    return fig, mrows, mcols, str_img_ok


def offsets_and_ron(obsid, temp, filename, output_dir=None, camera=None, setup=None, func=None, verbose=True, postfix=None):
    """
    offsets_and_ron(filename, output_dir=None, camera=None, setup=None, verbose=True)

    obsid     : obsid
    temp      : temperature environment, in ['ambient', 'tvac']
    filename  : fits file to analyse : full path!
    output_dir: output directory, where images and text results are printed
    camera    : camera ID, e.g. 'brigand'. Used for the output filename
    setup     : egse.setup
    func      : function to combine the statistics gathered on individual columns (default = numpy.mean)
    verbose   : controls the display of intermediate results on scren.
    postfix   : string that will be appended to the output filename
    """
    import numpy

    debug = False
    sobsid = str(obsid).zfill(5)

    if func is None:
        func, sfunc = numpy.mean, 'mean'
    elif isinstance(func, str):
        if func == "mean":
            func, sfunc = numpy.mean, 'mean'
        elif func == "median":
            func, sfunc = numpy.median, 'median'
        elif func == "max":
            func, sfunc = numpy.max, 'max'
        elif func == "min":
            func, sfunc = numpy.min, 'min'
        else:
            print(f"CRITICAL: String value of 'func' unrecognized: {func}. Please chose in ['mean', 'median', 'max', 'min']")
            raise ValueError
    elif isinstance(func, numpy.mean.__class__):
        sfunc = 'user_func'
    else:
        print(f"CRITICAL: Non-string value of 'func' unrecognized: {func}. Please chose in ['mean', 'median', 'max', 'min']")
        raise ValueError

    # DEFAULTS FROM THE SETUP
    if setup is None:
        setup = load_setup()

    if camera is None:
        camera = setup.camera.ID

    # LOAD THE ACCEPTABLE RANGES FOR THE OFFSETS AND READ OUT NOISE
    # -------------
    # hlimit = {'off':[1000, 1350], 'noise':[1.7, 2.25]}
    hlimit = {'off':setup.camera.ccd.limits[temp].offset, 'noise':setup.camera.ccd.limits[temp].noise}

    # LOAD THE DATA
    # -------------
    hduc = fits.open(filename)
    extnames = iu.get_extnames(0, [filename])
    if debug:
        print(f"{filename}\n    Extension names")
        cv.print1(extnames)

    # CHECK WHICH CCD_SIDES EXIST IN THE INPUT DATA CUBE
    ccd_sides = []
    for side in ["F", "E"]:
        for extname in extnames:
            if extname.find(f"_{side}") >= 0:
                ccd_sides.append(side)
                break

    # PREPARE THE COLLECTION OF 'TEST-VARIABLES'
    # ------------------------------------------
    # Usually extension 2 is the first image extension, e.g. IMAGE_1_E"
    tmp = np.array([i[:5] for i in extnames])
    first_img_ext = np.where(tmp=="IMAGE")[0][0]
    nlayers = hduc[first_img_ext].shape[0]

    nn = 4 * 2 * nlayers

    ccd_codes = np.zeros([nn],dtype=object)
    layers = np.zeros([nn], dtype=int)
    off_spres = np.zeros([nn], dtype=float)
    off_sovers = np.zeros_like(off_spres)
    off_povers = np.zeros_like(off_spres)
    nois_spres = np.zeros([nn], dtype=float)
    nois_sovers = np.zeros_like(off_spres)
    nois_povers = np.zeros_like(off_spres)
    off_imgs = np.zeros_like(off_spres)
    nois_imgs_col = np.zeros_like(off_spres)

    # ANALYSIS AND SORTING OF ALL EXTENSIONS
    # --------------------------------------
    hccd = 0
    for ccd in range(1,5):
        for side in ccd_sides:
            ccd_code = f"{str(ccd)}_{side}"

            # SPRE ANALYSIS  (5, 4540, 25)
            data = hduc[f"SPRE_{ccd_code}"].data
            if debug:
                print(F"{ccd_code} {hccd} {data.shape}")
                print(f"{ccd_code}  SPRE_{ccd_code}")

            c = hccd-1
            for l in range(nlayers):
                c += 1

                ccd_codes[c] = ccd_code
                layers[c] = l

                layer = data[l, :,12:22]
                off_spres[c] = np.nanmean(layer)
                #nois_spres[c] = np.nanstd(layer)
                nois_spres[c] = func(np.nanstd(layer, axis=0))

            # SOVER ANALYSIS (5, 4540, 15)
            data = hduc[f"SOVER_{ccd_code}"].data
            if debug:
                print(F"{ccd_code}  SOVER_{ccd_code} {data.shape}")

            c = hccd-1
            for l in range(nlayers):
                c+=1
                layer = data[l, :, 2:]
                off_sovers[c] = np.nanmean(layer)
                #nois_sovers[c] = np.nanstd(layer)
                nois_sovers[c] = func(np.nanstd(layer, axis=0))

            # POVER ANALYSIS (5, 30, 2255)
            try:
                data = hduc[f"POVER_{ccd_code}"].data
                if debug:
                    print(F"{ccd_code}  POVER_{ccd_code}  {data.shape}")

                c = hccd-1
                for l in range(nlayers):
                    c+=1
                    layer = data[l, :,:]
                    off_povers[c] = np.nanmean(layer)
                    nois_povers[c] = func(np.nanstd(layer,axis=0))
            except:
                print(f"     No // overscan: POVER_{ccd_code} ")

            # IMG ANALYSIS (5, 4510, 2255)
            data = hduc[f"IMAGE_{ccd_code}"].data
            if debug:
                print(F"{ccd_code}  IMAGE_{ccd_code}  {data.shape}")

            c = hccd-1
            for l in range(nlayers):
                c+=1

                off_imgs[c] = np.nanmean(data[l,:,:])
                nois_imgs_col[c] = func(np.nanstd(data[l,:,:], axis=0))

            hccd = c+1


    # ASSEMBLE THE TABLE OF RESULTS
    # -----------------------------
    keys = ["ccd_code", "layer", "off_spre", "off_sover", "off_pover", "off_img", "noise_spre", "noise_sover", "noise_pover", "noise_img_col"]
    values = [ccd_codes, layers, off_spres, off_sovers, off_povers, off_imgs, nois_spres, nois_sovers, nois_povers, nois_imgs_col]

    check_keys = ["off_spre", "off_sover", "off_pover", "off_img", "noise_sover", "noise_img_col"]

    tabout = Table()
    for key,value in zip(keys, values):
        if value.dtype == 'float64':
            tabout[key] = np.round(value, 3)
        else:
            tabout[key] = value

    # CHECK THE RESULTS AGAINST THE LIMITS
    # ------------------------------------
    if verbose:
        print(f"Limits:")
        print(f"        offset:")
        print(f"{hlimit['off']}")
        print(f"        r.o.n.:")
        print(f"{hlimit['noise']}\n")

    hok = {True:" OK", False:"NOK"}
    hkeyok = {'ccd_code':True, 'layer':True}

    allok = True
    stringout = ""
    for key,value in zip(keys, values):
        for observable in ['off', 'noise']:
            if key.find(observable)==0:
                hkeyok[key] = True
                for ccd in range(1, 5):
                    for side in ccd_sides:
                        ccdid,ccd_code = f"{str(ccd)}{side}", f"{str(ccd)}_{side}"
                        ccdsel = np.where(tabout['ccd_code']==ccd_code)
                        ccdvalues = value[ccdsel]
                        limits = hlimit[observable][ccdid]
                        value_ok = np.all((ccdvalues >= limits[0]) & (ccdvalues <= limits[1]))

                        if key in check_keys:
                            allok = allok & value_ok

                        hkeyok[key] = hkeyok[key] & value_ok

                        stringout += f"{key:14s} {ccdid} {np.round(ccdvalues, 3)} [{limits[0]:.3f},{limits[1]:.3f}] {hok[value_ok]}\n"
                        if verbose:
                            print(f"{key:14s} {ccdid} {np.round(ccdvalues, 3)} [{limits[0]:.3f},{limits[1]:.3f}] {hok[value_ok]}")

    tabout['img-sover'] = np.round(off_imgs-off_sovers,3)

    # OUTPUT THE RESULTS
    # ------------------
    if postfix is not None:
        postfix = "_" + postfix
    output_filename = f"sft_analysis_{camera}_{sobsid}_img_checks_offsets_ron_{sfunc}{postfix}.txt"
    ascii.write(tabout, output=output_dir + output_filename, format='fixed_width', overwrite=True)

    f = open(output_dir + output_filename, 'a')

    f.write(f"\nLimits:\n        offset:\n{hlimit['off']}\n")
    f.write(f"        r.o.n.:\n{hlimit['noise']}\n\n")

    f.write("\nField         CCD           Values                               Limits            OK / NOK\n")
    f.write(stringout+'\n')

    stringout = "\nSummary\n"
    for key in check_keys:
        stringout += f"{key:14s} {hok[hkeyok[key]]}\n"
    if allok:
        s = "\nCCD offsets & r.o.n.: OK.      IF voltage checks OK, you can PROCEED.\n"
    else:
        s = "\nCCD offsets & r.o.n.: NOT OK.  STOP for analysis.\n"
    stringout += s
    str_img_ok = s

    print(stringout)
    f.write(stringout)

    # f.write("Summary\n")
    # #print_keys = ["off_spre", "off_sover", "off_pover", "off_img", "off_img", "noise_spre", "noise_sover", "noise_pover", "noise_img_col"]
    # for key in check_keys:
    #     f.write(f"{key:14s} {hok[hkeyok[key]]}\n")
    #
    # if allok:
    #     f.write("\nChecks of CCD offsets & r.o.n. OK.\n\nIF voltage checks OK, you can PROCEED.\n")
    # else:
    #     f.write("\nChecks of CCD offsets & r.o.n. NOT OK.\n\nSTOP for analysis.")

    f.close()
    return str_img_ok
