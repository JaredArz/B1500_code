
GPIB_ADDRESS = "GPIB1::17::INSTR"
TIMEOUT=30000

# with current ADC settings, real time measured over is COUNT * INTERVAL
# HSADC can not measure accurately for these fluctuations (faster than 10's of KHz)
# so use a long sample interval , much longer than fluctuation and modulate sample count
# to get a longer time. Doing this instead of a single long measurement just adds
# redundancy and allows for observation of any potential drift/ESD events.
SAMPLE_INTERVAL = 100e-3
SAMPLE_COUNT = 10
# 10 to sanity
# 50 for fast, 1us
# 100 for 2-5us
#let time captured be minimum 5 second then sample count minimum is 50, can be higher for ms fluctuating deviecs up to a hundred or so
DUT = "S2_7"
I_START = -75e-6
I_STOP = -130e-6
I_STEP = -2.5e-6
WAFER = "A5"




V_START = 1.56
V_STOP = 1.6
V_STEP = 2.5e-3 #step should be <= 10mV

# a hold before measuring
SETTLING_TIME = 10e-3 # minimum value

SAVE_PATH = f"./260509-{WAFER}_data/{DUT}/"
