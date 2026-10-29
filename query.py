from pymeasure.instruments.agilent import AgilentB1500

b1500 = AgilentB1500(
    "GPIB1::17::INSTR",
    timeout = 10000
)

b1500.initialize_all_smus()
print(b1500.query_modules())
print(b1500.smu_names)

