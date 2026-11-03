import numpy as np
import matplotlib.pyplot as plt


path = "test_dut/old_7_VV_261030_1512.csv"

if __name__ == "__main__":
    data = np.loadtxt(path, dtype="str", delimiter=",")
    vin = np.asarray(data[1:,0],dtype=float)
    vout = np.asarray(data[1:,1],dtype=float)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(vin, vout, color="cornflowerblue", alpha=0.75)
    ax.scatter(vin, vout, color="cornflowerblue")
    ax.set_ylabel("⟨Vout⟩ [V]")
    ax.set_xlabel("Vin [V]")
    ax.set_title("p-bit voltage transfer function [X time per point]")
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='gray')
    fig.tight_layout()
    fig.savefig(path + "_VV.png", dpi=400)

