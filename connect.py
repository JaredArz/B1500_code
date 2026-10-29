import pyvisa

rm = pyvisa.ResourceManager()
instr = rm.open_resource("GPIB1::17::INSTR")
instr.timeout = 10000
instr.query("*IDN?")