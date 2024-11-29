# BP.pyx

# Define the struct outside of any function or method
cdef struct Range:
    int systolic_min
    int systolic_max
    int diastolic_min
    int diastolic_max

# The main class for BloodPressureMonitoring
cdef class BloodPressureMonitoring:
    cdef dict normal_ranges

    def __init__(self):
        self.normal_ranges = {}

    def generateKey(self, int age, str gender):
        return str(age) + gender

    def loadCSV(self, str csvfile):
        # You can implement CSV loading logic here
        pass

    def isBloodPressureNormal(self, int systolic, int diastolic, int age, str gender):
        cdef str key = self.generateKey(age, gender)
        if key not in self.normal_ranges:
            print(f"No data for age {age} and gender {gender}")
            return False
        cdef Range range = self.normal_ranges[key]
        return systolic >= range.systolic_min and systolic <= range.systolic_max and \
               diastolic >= range.diastolic_min and diastolic <= range.diastolic_max

    def evaluatePatientStatus(self, int systolic, int diastolic):
        if systolic < 90 or diastolic < 60:
            return "Low"
        elif systolic <= 120 and diastolic <= 80:
            return "Normal"
        elif systolic <= 139 or diastolic <= 89:
            return "Slightly High"
        else:
            return "High"

    def generateReport_BP(self, str patientID, int systolic, int diastolic, int age, str gender):
        normal = self.isBloodPressureNormal(systolic, diastolic, age, gender)
        status = self.evaluatePatientStatus(systolic, diastolic)

        print(f"Patient ID: {patientID}")
        print(f"Systolic: {systolic}, Diastolic: {diastolic}")
        print(f"Age: {age}, Gender: {gender}")
        print(f"Normal Range: {'Yes' if normal else 'No'}")
        print(f"Status: {status}")
