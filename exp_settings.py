
GPIB_ADDRESS = "GPIB1::17::INSTR"
TIMEOUT=10000

# with current ADC settings, real time measured over is COUNT * INTERVAL
# HSADC can not measure accurately for these fluctuations (faster than 10's of KHz)
# so use a long sample interval , much longer than fluctuation and modulate sample count
# to get a longer time. Doing this instead of a single long measurement just adds
# redundancy and allows for observation of any potential drift/ESD events.
SAMPLE_COUNT = 1
SAMPLE_INTERVAL = 50e-3

# a hold before measuring
SETTLING_TIME = 10e-3 # minimum value
DUT = "S1_2"
SAVE_PATH = f"./260509-A1_data/{DUT}/"
