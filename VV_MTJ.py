import numpy as np
import os
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
# uses these in this exact configuration, no safety checks
# run query.py to validate this.

V_START = 1.3
V_STOP = 1.4
V_STEP = 10e-3 #step should be <= 10mV

I_COMPLIANCE = 100*10**-6 #measurement side


HEADER = ["Vin", "mean_Vout", "status", "error"]
def main():

    b1500 = AgilentB1500(
        GPIB_ADDRESS,
        timeout = 100000
    )

    os.makedirs(SAVE_PATH, exist_ok=True)
    now = datetime.now()
    OUTPUT_FILE = SAVE_PATH + f"{DUT}_VV_{now.strftime("%y%m%d_%H%M")}"

    n_steps = int(round((V_STOP - V_START) / V_STEP)) + 1
    voltages = np.linspace(
        V_START,
        V_START + (n_steps - 1) * V_STEP,
        n_steps
    )


    results, t_series = run_measurement(
        b1500=b1500,
        voltages=voltages,
        I_compliance=I_COMPLIANCE,
        sample_count=SAMPLE_COUNT,
        sample_interval=SAMPLE_INTERVAL,
        settling_time=SETTLING_TIME
    )

    save_csv(OUTPUT_FILE, results, t_series)

def run_measurement(
    b1500,
    voltages,
    I_compliance,
    sample_count,
    sample_interval,
    settling_time,
    V_compliance = 0.5,
    ramp_pause= 50e-3,
    ramp_step = 5*10**-3
):

    b1500.initialize_all_smus()
    b1500.data_format(21, mode=0)

    smu_force = list(b1500.smu_references)[2]
    smu_sense = list(b1500.smu_references)[1] #HRSMU

    input("Measurement is ready to start, please double check hardware")
    print(f"Configuring...")

    b1500.meas_mode("SAMPLING", smu_force, smu_sense)
    for smu in [smu_force, smu_sense]:
        smu.enable()
        smu.adc_type = "HRADC"
        smu.meas_op_mode = "COMPLIANCE_SIDE"
    smu_force.meas_range_current = "1 uA"
    smu_sense.meas_range_voltage = "5 V"
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
        smu_sense.sampling_source(
            "CURRENT",
            "Auto Ranging",
            0,
            0,
            V_compliance
        )
        
        voltage = voltages[0]
        smu_force.ramp_source(
            "VOLTAGE",
            "Auto Ranging",
            voltage,
            stepsize=ramp_step,
            pause=ramp_pause,
            comp = I_compliance
        ) 

        for voltage in voltages:
            print(f"Measuring voltage at: {voltage:.4g} V")

            #type, range, base, bias, compliance (base and bias are same for constant measurement)
            smu_force.sampling_source(
                "VOLTAGE",
                "Auto Ranging",
                voltage,
                voltage,
                I_compliance
            )
            
            time.sleep(settling_time)
            b1500.check_errors()
            b1500.clear_buffer()
            b1500.clear_timer()
            b1500.send_trigger()
            b1500.check_idle()
            
            data = b1500.read_data(sample_count*2).to_numpy()
            vout = data[:,1][1::2]
            t = data[:,0][1::2]
            mean_vout = np.mean(vout)
            print(f"Average voltage out: {mean_vout:.4g} V")

            results.append({
                HEADER[0]: voltage,
                HEADER[1]: mean_vout,
                HEADER[2]: "OK",
                HEADER[3]: ""
            })
            new = np.column_stack((t, vout))
            t_series = np.vstack((t_series, new))
            
    except Exception:
        error_message = traceback.format_exc()
        print(f"Measurement terminated due to an error:\n\r{error_message}")
        results.append({
            HEADER[0]: np.nan,
            HEADER[1]: np.nan,
            HEADER[2]: "FAILED",
            HEADER[3]: error_message
        })
    finally:
        ramp_down = np.round(np.linspace(
            voltage,
            0,
            int(voltage/(ramp_step))
        ),decimals=4)
        time.sleep(0.5)
        for v in ramp_down:
            smu_force.force(
                "Voltage",
                "Auto Ranging",
                v,
                comp=I_compliance
            ) 
            time.sleep(ramp_pause*2)
        b1500.check_idle()
        input("Measurement is complete and current is ramped down, please double check hardware")
        smu_sense.disable()
        smu_force.disable()
    return results, t_series

def save_csv(filename, resuls, t_series):
    data = np.array([
        [r[HEADER[0]], r[HEADER[1]], r[HEADER[2]], r[HEADER[3]]]
        for r in results
    ], dtype=object)

    np.savetxt(
        filename + ".csv",
        data,
        delimiter=",",
        header=f"{HEADER[0]},{HEADER[1]},{HEADER[2]},{HEADER[3]}",
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

