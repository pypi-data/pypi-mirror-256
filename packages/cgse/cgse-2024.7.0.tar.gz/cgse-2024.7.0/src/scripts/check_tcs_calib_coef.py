from egse.setup import load_setup
import numpy as np
import matplotlib.pyplot as plt

def check_calib_coef(setup_id: int):
    setup = load_setup(setup_id)
    print(f"\nThis script checks that TOU RTD calibration coefficients provided by Alter are identical than coefficients"
          f" set in Setup file for camera {setup.camera.ID} {setup.camera.serial_number}.\n")
    print('Setup ID loaded: ', setup.get_id())


    print("\n\nFirst, we check that serial numbers of TOU RTD set in the setup file match with ABCL.\n")
    sensors = setup.gse.tcs.calibration.sensors
    rtd_serial_numbers_in_setup = dict()
    for tou_rtd in sensors:
        rtd_serial_numbers_in_setup[sensors[tou_rtd].conversion] = sensors[tou_rtd].serial_number
    rtd_serial_numbers_in_abcl = dict()
    for frtd in rtd_serial_numbers_in_setup:
        rtd_serial_numbers_in_abcl[frtd] = input(f"Serial name of TOU {frtd} (TRP-1#{frtd[-1]}) in ABCL: ")

    err = 0
    for frtd in rtd_serial_numbers_in_setup:
        if rtd_serial_numbers_in_setup[frtd] != rtd_serial_numbers_in_abcl[frtd]:
            print(f"\nERROR in S/N of {frtd}.\n"
                  f"In Setup file: {rtd_serial_numbers_in_setup[frtd]}\n"
                  f"In ABCL: {rtd_serial_numbers_in_abcl[frtd]}")
            err += 1
    if err == 0:
        print("\nAll S/N of TOU RTD match: OK")
    else:
        print("\nSome S/N are not identical between Setup file and ABCL. See above for detail.")
        return

    print("\n\nNow we check that TOU RTD calibration coefficients set in the Setup file match with Alter file.")
    print("Use doucment 'PLATO THERMISTORS CALIBRATION TEST REPORT' (Eclipse ref: 2022013099).\nCopy the entire line of"
          " the three polynomial equations.\n"
          "For instance: 'T = -1.636680380E-11R 5 + 5.537426295E-08xR 4 - 7.472300219E-05R 3 + 5.028427373E-02R 2 -"
          "1.663264016E+01R + 2.013507126E+03'\n")

    rtd_calib_coef_in_setup = dict(setup.gse.tcs.calibration.conversion)
    rtd_calib_coef_in_alter = dict()
    for frtd in rtd_serial_numbers_in_setup:
        list_coef = input(f"Polynomial equation of {frtd} with S/N {rtd_serial_numbers_in_setup[frtd]}: ").strip()
        while list_coef[-1] not in [str(i) for i in range(10)]:
            list_coef = list_coef[:-1]
        list_coef = list_coef.replace(' ', '').replace('T', '').replace('=', '').replace('x', '').replace('X', '').split('R')
        for i in range(1,5):
            list_coef[i] = list_coef[i][1:]
        for i in range(6):
            list_coef[i] = float(list_coef[i])
        rtd_calib_coef_in_alter[frtd] = list_coef

    err = 0
    for frtd in rtd_calib_coef_in_setup:
        for i in range(6):
            if rtd_calib_coef_in_setup[frtd][i] != rtd_calib_coef_in_alter[frtd][i]:
                print(f"\nERROR in {frtd} ({rtd_serial_numbers_in_setup[frtd]}) for coefficient of R{5 - i}.\n"
                      f"In Setup file: {rtd_calib_coef_in_setup[frtd][i]}\n"
                      f"In Alter file: {rtd_calib_coef_in_alter[frtd][i]}")
                err += 1

    if err == 0:
        print("\nAll coefficients are identical in Setup file and Alter file: OK")
    else:
        print(f"\n{err} errors detected in calibration coefficients between Setup file and Alter file. "
              f"See above for detail.")
        return

    print("\n\nNow we plot the three relations T(R) defined by the polynomial equations.")

    R = np.arange(520, 1020.5, 0.5)
    for frtd in rtd_calib_coef_in_setup:
        list_coef = np.array(rtd_calib_coef_in_setup[frtd])
        T = np.zeros(np.shape(R))
        for i in range(6):
            T += list_coef[i] * R**(5-i)
        plt.plot(R, T, label=frtd)
    plt.plot(R, -110*np.ones(np.shape(R)), '--r', linewidth=2)
    plt.plot(R, -65*np.ones(np.shape(R)), '--r', linewidth=2)
    plt.legend(loc='best')
    plt.text(min(R), -109, "-110°C", color='red', fontsize=12)
    plt.text(min(R), -64, "-65°C", color='red', fontsize=12)
    plt.title("Thermal calibration curves for TCS using coefficients for cold temperature (below -65°C)")
    plt.xlabel("Resistance (Ohm)")
    plt.ylabel("Temperature (°C)")
    plt.grid()
    plt.show()


check_calib_coef(int(input("Setup file ID to be loaded: ")))