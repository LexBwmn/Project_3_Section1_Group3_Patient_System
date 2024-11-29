import BP

blood_pressure = BP.BloodPressureMonitoring()

# Call the methods defined in your C++/Cython class
blood_pressure.generateReport_BP("Patient123", 120, 80, 30, "Male")

# Or call other methods
status = blood_pressure.evaluatePatientStatus(120, 80)
print(status)
