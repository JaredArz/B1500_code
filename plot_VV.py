import numpy as np
import matplotlib.pyplot as plt


path = ""

if __name__ == "__main__":
    data = np.loadtxt(path + ".csv", dtype="str", delimiter=",")
    vin = np.asarray(data[1:,0],dtype=float)
    vout = np.asarray(data[1:,1],dtype=float)
    
    t_data = np.loadtxt(path + "_t.csv", dtype="str", delimiter=",")
    t_data = np.asarray(t_data[1:,:], dtype=float)
    N = t_data[0,2]
    T = t_data[0,3]
    sample_time = N*T

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(vin, vout, color="cornflowerblue", alpha=0.75)
    ax.scatter(vin, vout, color="cornflowerblue")
    ax.set_ylabel("⟨Vout⟩ [V]")
    ax.set_xlabel("Vin [V]")
    ax.set_title(f"p-bit voltage transfer function [{sample_time:.2g} s/point]")
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='gray')
    fig.tight_layout()
    fig.savefig(path + "_VV.png", dpi=400)

