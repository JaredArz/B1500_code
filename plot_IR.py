import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


path = "./260509-A5_data/S2_7/S2_7_IR_261105_1132"

if __name__ == "__main__":
    series_R = 2.197e3
    Is  = []
    Vs  = []
    data = np.loadtxt(path + ".csv", dtype="str", delimiter=",")
    Is = np.asarray(data[1:,0],dtype=float)
    Vs = np.asarray(data[1:,1],dtype=float)
    Rs = np.asarray(data[1:,2],dtype=float)
    Vmtj = Vs - Is*series_R
    Rmtj = Vmtj/Is
    t_data = np.loadtxt(path + "_t.csv", dtype ="str", delimiter=",")
    t_data = np.asarray(t_data[1:,:], dtype=float)
    N = t_data[0,2]
    T = t_data[0,3]
    sample_time = N*T

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(np.abs(Is)*10**6, Vmtj, color="cornflowerblue", alpha=0.75)
    ax.scatter(np.abs(Is)*10**6, Vmtj, color="cornflowerblue")
    ax.set_ylabel("⟨V⟩ [V]")
    ax.set_xlabel("Current [uA]")
    ax.set_title(f"MTJ current response [{sample_time} per point]")
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='gray')
    fig.tight_layout()
    fig.savefig(path + "_IV.png", dpi=400)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(np.abs(Is)*10**6, Rmtj, color="cornflowerblue", alpha=0.75)
    ax.scatter(np.abs(Is)*10**6, Rmtj, color="cornflowerblue") 
    ax.set_ylabel("⟨R⟩ [Ohm]")
    ax.set_xlabel("Current [uA]")
    ax.set_title(f"MTJ current response [{sample_time:.2g} s/point]")
    ymin = np.min(Rmtj)
    ymax = np.max(Rmtj)
    ticks = ax.get_yticks()
    ticks = ticks[(ticks>=ymin) & (ticks <= ymax)]
    if abs(np.min(ticks) - ymin) > 33:    
        ticks = np.unique(np.append(ticks,[ymin]))
    if abs(np.max(ticks) - ymax) > 33:    
        ticks = np.unique(np.append(ticks,[ymax]))
    ax.set_yticks(ticks)

    
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.grid(which='major', linestyle="-", linewidth=0.8, alpha=0.7)
    ax.grid(which='minor', linestyle=":", linewidth=0.5, alpha=0.4)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.grid(which='major', axis="both", linestyle="-", linewidth=0.8, alpha=0.7)
    ax.grid(which='minor', axis="both", linestyle=":", linewidth=0.5, alpha=0.4)
    fig.tight_layout()
    fig.savefig(path + "_IR.png", dpi=400)

