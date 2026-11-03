import numpy as np
import matplotlib.pyplot as plt


path = "test_dut/old_7_IR_261030_1422.csv"

if __name__ == "__main__":
    Is  = []
    Vs  = []
    data = np.loadtxt(path, dtype="str", delimiter=",")
    Is = np.asarray(data[1:,0],dtype=float)
    Vs = np.asarray(data[1:,1],dtype=float)
    Rs = np.asarray(data[1:,2],dtype=float)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(np.abs(Is), Vs, color="cornflowerblue", alpha=0.75)
    ax.scatter(np.abs(Is), Vs, color="cornflowerblue")
    ax.set_ylabel("⟨V⟩ [V]")
    ax.set_xlabel("Current [uA]")
    ax.set_title("MTJ current response [X time per point]")
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='gray')
    fig.tight_layout()
    fig.savefig(path + "_IV.png", dpi=400)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(np.abs(Is), Rs, color="cornflowerblue", alpha=0.75)
    ax.scatter(np.abs(Is), Rs, color="cornflowerblue")
    ax.set_ylabel("⟨R⟩ [Ohm]")
    ax.set_xlabel("Current [uA]")
    ax.set_title("MTJ current response [X time per point]")
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='gray')
    fig.tight_layout()
    fig.savefig(path + "_IR.png", dpi=400)

