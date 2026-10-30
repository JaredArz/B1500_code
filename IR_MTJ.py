import numpy as np
import os
import csv
import time
import traceback
import warnings
from datetime import datetime
from exp_settings import *

warnings.filterwarnings("ignore", category=FutureWarning)
#needs pandas 2.3.3

from pymeasure.instruments.agilent import AgilentB1500

# B1500 (right, GPIB1), is configured with:
# SMU2: HRSMU
# SMU3: MPSMU
# run query.py to validate this.

I_START = 90e-6
I_STOP = 110e-6
I_STEP = 1e-6
#when sourcing current, compliance side measurement is voltage
V_COMPLIANCE = 1.0

HEADER = ["current", "mean_v", "resistance", "status", "error"]

def main():
    b1500 = AgilentB1500(
        GPIB_ADDRESS,
        timeout = 100000
    )

    smu = "SMU2" #HRSMU, only SMU2 works for now

    os.makedirs(SAVE_PATH, exist_ok=True)
    now = datetime.now()
    OUTPUT_FILE = SAVE_PATH + f"{DUT}_IR_{now.strftime("%y%m%d_%H%M")}"

    n_steps = int(round((I_STOP - I_START) / I_STEP)) + 1
    currents = np.linspace(
        I_START,
        I_START + (n_steps - 1) * I_STEP,
        n_steps
    )

    results, t_series = run_measurement(
        b1500=b1500,
        smu=smu,
        currents=currents,
        V_compliance=V_COMPLIANCE,
        sample_count=SAMPLE_COUNT,
        sample_interval=SAMPLE_INTERVAL,
        settling_time=SETTLING_TIME
    )

    save_csv(OUTPUT_FILE, results, t_series)

def run_measurement(
    b1500,
    smu,
    currents,
    V_compliance,
    sample_count,
    sample_interval,
    settling_time,
    ramp_pause=50e-3,
    ramp_step = 1**-6,
):
    b1500.initialize_all_smus()
    b1500.data_format(21, mode=0)

    input("Measurement is ready to start, please double check hardware")
    print("Configuring...")

    b1500.meas_mode("SAMPLING", smu)
    smu.enable()
    smu.adc_type = "HRADC"
    smu.meas_range_voltage = "2 V"
    smu.meas_op_mode = "COMPLIANCE_SIDE"
    b1500.sampling_mode = "LINEAR"
    b1500.adc_setup("HRADC", "AUTO", 6)

    b1500.sampling_timing(
        settling_time,
        sample_interval,
        sample_count
    )
    
    b1500.sampling_auto_abort(False)
    b1500.time_stamp = True
    
    results = []
    t_series = np.empty((0,2))

    try:
        #may need to be b1500.smu2....
        smu.ramp_source(
            "CURRENT",
            "Auto Ranging",
            currents[0],
            stepsize=ramp_step,
            pause=ramp_pause,
            comp = V_compliance
        ) 
        for current in currents:
            print(f"Measuring voltage at: {current:.4g} A")

            #type, range, base, bias, compliance (base and bias are same for constant measurement)
            smu.sampling_source(
                "CURRENT",
                "Auto Ranging",
                current,
                current,
                V_compliance
            )
            
            time.sleep(settling_time)
            b1500.check_errors()
            b1500.clear_buffer()
            b1500.clear_timer()
            b1500.send_trigger()
            
            b1500.check_idle()
            
            data = b1500.read_data(sample_count).to_numpy()
            voltages = data[:,1]
            t = data[:,0]
            mean_v = np.mean(voltages)
            resistance = mean_v / current
            print(f"Average voltage: {mean_v:.4g} V")
            print(f"Resistance:      {resistance:.8g} Ohm")
            results.append({
                HEADER[0]: current,
                HEADER[1]: mean_v,
                HEADER[2]: resistance,
                HEADER[3]: "OK",
                HEADER[4]: "",
            })
            new = np.column_stack((t, voltages))
            t_series = np.vstack((t_series, new))
            
    except Exception:
        error_message = traceback.format_exc()
        print("Measurement terminated due to an error:")
        print(error_message)
        results.append({
            HEADER[0]: np.nan,
            HEADER[1]: np.nan,
            HEADER[2]: np.nan,
            HEADER[3]: "FAILED",
            HEADER[4]: error_message
        })
    finally:
        time.sleep(0.5)
        smu.ramp_source(
            "CURRENT",
            "Auto Ranging",
            0,
            stepsize=ramp_step,
            pause=ramp_pause
        ) 
        input("Measurement is complete and current is ramped down, please double check hardware")
        smu.disable()

    return results, t_series

def save_csv(filename, results, t_series):
    data = np.array([
        [r[HEADER[0]], r[HEADER[1]], r[HEADER[2]], r[HEADER[3]], r[HEADER[4]]]
        for r in results
    ], dtype=object)

    np.savetxt(
        filename + ".csv",
        data,
        delimiter=",",
        header=f"{HEADER[0]},{HEADER[1]},{HEADER[2]},{HEADER[3]},{HEADER[4]}",
        comments="",
        fmt="%s"
    )
    np.savetxt(
        filename + "_t.csv",
        t_series,
        delimiter=",",
        header="t,Vout",
        comments=""
    )
    print(f"Measurement data saved to: {filename}")

if __name__ == "__main__":
    main()

