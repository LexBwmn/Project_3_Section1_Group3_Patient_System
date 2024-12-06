#import numpy as np
import random
import csv
import time

# Define the PatientData structure
class PatientData:
    def __init__(self, id, roomNumber, age, gender, weight, currentPressure, temperature, disease, respiratoryRate, oxygenSaturation, glucoseLevel):
        self.id = id
        self.roomNumber = roomNumber
        self.age = age
        self.gender = gender
        self.weight = weight
        self.currentPressure = currentPressure
        self.temperature = temperature
        self.disease = disease
        self.respiratoryRate = respiratoryRate
        self.oxygenSaturation = oxygenSaturation
        self.glucoseLevel = glucoseLevel

# Define the ThresholdData structure
class ThresholdData:
    def __init__(self, age, gender, weight, pressure, thresholdPressure):
        self.age = age
        self.gender = gender
        self.weight = weight
        self.pressure = pressure
        self.thresholdPressure = thresholdPressure

class BodyWeightPressureMonitor:
    WEIGHT_TOLERANCE = 0.01

    def __init__(self):
        self.thresholds = []
        self.patients = []
        self.dataLoaded = False

    def loadThresholdData(self, filePath):
        try:
            with open("BodyWeight.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header line
                for row in reader:
                    threshold = ThresholdData(
                        age=int(row[0]),
                        gender=row[1],
                        weight=float(row[2]),
                        pressure=float(row[3]),
                        thresholdPressure=float(row[4])
                    )
                    self.thresholds.append(threshold)
                print("Threshold data loaded successfully.")
        except Exception as e:
            print(f"Error opening Body Weight and Pressure data file: {filePath}")
            print(e)

    def loadPatientData(self, filePath):
        try:
            with open("Patient_Dat.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header line
                for row in reader:
                    patient = PatientData(
                        id=int(row[0]),
                        roomNumber=int(row[1]),
                        age=int(row[2]),
                        gender=row[3],
                        weight=float(row[5]),
                        currentPressure=float(row[6]),
                        temperature=None,  # Placeholder, assuming no field for this
                        disease=None,      # Placeholder, assuming no field for this
                        respiratoryRate=None,  # Placeholder, assuming no field for this
                        oxygenSaturation=None,  # Placeholder, assuming no field for this
                        glucoseLevel=None  # Placeholder, assuming no field for this
                    )
                    self.patients.append(patient)
                self.dataLoaded = True
                print("Patient data loaded successfully.")
        except Exception as e:
            print(f"Error opening patient data file: {filePath}")
            print(e)

    def isDataLoaded(self):
        return self.dataLoaded

    def monitorRandomPatientData(self):
        if not self.patients:
            print("No patient data available to monitor.")
            return

        # Select a random patient
        randomIndex = random.randint(0, len(self.patients) - 1)
        randomPatient = self.patients[randomIndex]

        print(f"Monitoring body pressure on bed for Patient ID {randomPatient.id} in Room {randomPatient.roomNumber}...")

        thresholdExceeded = False
        matchedThreshold = False

        for threshold in self.thresholds:
            if (randomPatient.age == threshold.age and
                randomPatient.gender == threshold.gender and
                abs(randomPatient.weight - threshold.weight) < self.WEIGHT_TOLERANCE):
                
                matchedThreshold = True  # Patient's data matches threshold criteria

                if randomPatient.currentPressure > threshold.thresholdPressure:
                    self.sendAlert(randomPatient)
                    thresholdExceeded = True
                    break
                else:
                    print(f"Patient ID {randomPatient.id} in Room {randomPatient.roomNumber} is within safe limits.")

    def sendAlert(self, patient):
        print(f"ALERT: Patient ID {patient.id} in Room {patient.roomNumber} exceeds the pressure threshold with current pressure {patient.currentPressure} Pa")
        
        # Simulate prompt to caregiver to use bed positioning control
        print("\nAdjust the bed position.")
        print("1. Supine\n2. Fowler\n3. Skip")
        choice = input("Enter your choice: ")

        if choice == "1":
            self.changeBedPosition("Supine")
        elif choice == "2":
            self.changeBedPosition("Fowler")
        else:
            print("No changes made to bed position.")

    def changeBedPosition(self, position):
        print(f"Changing bed position to {position}.")
        
class BedPositioningController:
    # Enum-like class to define bed positions
    class BedPosition:
        SUPINE = "Supine"
        FOWLER = "Fowler"

    def __init__(self):
        self.log_file_path = "BedPositionLog.log"

    def change_bed_position(self, position):
       # print(f"Changing bed position to {self.get_position_name(position)}...")
        # Log the change after adjusting the bed position
        self.log_position_change(position)

    def log_position_change(self, position):
        try:
            # Open the log file in append mode
            with open(self.log_file_path, "a") as log_file:
                # Get current time
                current_time = time.localtime()
                time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
                
                # Log the position change with a timestamp
                log_file.write(f"Timestamp: {time_str} | Bed Position Changed to: {self.get_position_name(position)}\n")
        except Exception as e:
            print(f"Error opening log file: {self.log_file_path}")
            print(f"Exception: {e}")

    def get_position_name(self, position):
        return position

class ThresholdDataBedTemp:
    def __init__(self, ageGroup, disease, normalTemperature, minimumTemperature,maximumTemperature):
        self.ageGroup = ageGroup
        self.disease = disease
        self.normalTemperature = normalTemperature
        self.minimumTemperature = minimumTemperature
        self.maximumTemperature = maximumTemperature
        
class BedTemperatureMonitor:
    def __init__(self):
        self.thresholds = []
        self.patients = []
        self.data_loaded = False

    def load_threshold_data(self, file_path):
        try:
            with open("Bed_Temperature.csv", 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header line
                for row in reader:
                    threshold = ThresholdDataBedTemp(
                        ageGroup = int(row[0]),
                        disease = row[1],
                        normalTemperature = float(row[2]),
                        minimumTemperature = float(row[3]),
                        maximumTemperature = float(row[4])
                    )
                    self.thresholds.append(threshold)
                print("Threshold data loaded successfully.")
        except Exception as e:
            print(f"Error opening Bed Temperature data file: {file_path}")
            print(f"Exception: {e}")
            
    def load_patient_data(self, filePath):
        try:
            with open("Patient_Dat.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header line
                for row in reader:
                    patient = PatientData(
                        id=int(row[0]),
                        roomNumber=int(row[1]),
                        age=int(row[2]),
                        gender=None,
                        disease=row[4],
                        weight=None,
                        currentPressure=None,
                        temperature=float(row[7]),  # Placeholder, assuming no field for this
                              # Placeholder, assuming no field for this
                        respiratoryRate=None,  # Placeholder, assuming no field for this
                        oxygenSaturation=None,  # Placeholder, assuming no field for this
                        glucoseLevel=None  # Placeholder, assuming no field for this
                    )
                    self.patients.append(patient)
                self.data_loaded = True
                print("Patient data loaded successfully.")
        except Exception as e:
            print(f"Error opening patient data file: {filePath}")
            print(e)


    def is_data_loaded(self):
        return self.data_loaded

    def monitor_random_patient_data(self):
        if not self.patients:
            print("No patient data available to monitor.")
            return

        # Select a random patient
        randomIndex = random.randint(0, len(self.patients) - 1)
        randomPatient = self.patients[randomIndex]

        print(f"Monitoring bed temperature for Patient ID {randomPatient.id} in Room {randomPatient.roomNumber}...")

        thresholdExceeded = False
        matchedThreshold = False

        # Iterate through the threshold data to find a match
        for threshold in self.thresholds:
            if randomPatient.age == threshold.ageGroup and randomPatient.disease == threshold.disease:
                matchedThreshold = True

                # Check if temperature is outside the acceptable range
                if randomPatient.temperature < threshold.minimumTemperature:
                    print(f"ALERT: Patient ID {randomPatient.id} has low temperature ({randomPatient.temperature}). Action required.")
                    self.send_alert(randomPatient , threshold)
                    break
                elif randomPatient .temperature > threshold.maximumTemperature:
                    print(f"ALERT: Patient ID {randomPatient.id} has high temperature ({randomPatient .temperature}). Action required.")
                    self.send_alert(randomPatient, threshold)
                    break
                else:
                    print(f"Patient ID {randomPatient.id} in Room {randomPatient.roomNumber} has a body temperature within acceptable limits ({randomPatient.temperature}).")

        if not matchedThreshold:
            print(f"No matching threshold found for Patient ID {randomPatient.id}.")

    def send_alert(self, patient, threshold):
        print(f"Normal Range: {threshold.minimumTemperature} - {threshold.maximumTemperature}")

        temp_controller = BedTemperatureController()
        choice = int(input("\nAdjust the bed temperature.\n1. Increase temperature\n2. Decrease temperature\n3. Skip adjustment\nEnter your choice: "))

        if choice == 1:
            temp_controller.adjust_temperature(TemperatureAdjustment.INCREASE)
        elif choice == 2:
            temp_controller.adjust_temperature(TemperatureAdjustment.DECREASE)
        else:
            print("No changes made to bed temperature.")

class TemperatureAdjustment:
    INCREASE = "Increase"
    DECREASE = "Decrease"

class BedTemperatureController:
    def adjust_temperature(self, adjustment):
        if adjustment == TemperatureAdjustment.INCREASE:
            print("Increasing bed temperature for patient comfort.")
        elif adjustment == TemperatureAdjustment.DECREASE:
            print("Decreasing bed temperature to prevent overheating.")
        
        self.log_temperature_adjustment(adjustment)

    def log_temperature_adjustment(self, adjustment):
        try:
            with open("BedTemperatureAdjustments.log", 'a') as log_file:
                current_time = time.localtime()
                time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
                log_file.write(f"Time: {time_str} | Temperature adjustment: {adjustment}\n")
        except Exception as e:
            print(f"Error logging temperature adjustment: {e}")
            
class OxygenSaturationMonitoringDevice:
    oxygenSaturationLowerThreshold = 90  # Lower threshold value
    oxygenSaturationUpperThreshold = 95  # Upper threshold value

    def __init__(self):
        self.patients = []
        self.dataLoaded = False

    def load_patient_data(self, filePath):
        try:
            with open("Patient_Dat.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header line
                for row in reader:
                    patient = PatientData(
                        id=int(row[0]),
                        roomNumber=int(row[1]),
                        age=int(row[2]),
                        gender=None,
                        disease=None,
                        weight=None,
                        currentPressure=None,
                        temperature=None,  # Placeholder, assuming no field for this
                              # Placeholder, assuming no field for this
                        respiratoryRate=None,  # Placeholder, assuming no field for this
                        oxygenSaturation=int(row[9]),  # Placeholder, assuming no field for this
                        glucoseLevel=None  # Placeholder, assuming no field for this
                    )
                    self.patients.append(patient)
                self.dataLoaded = True
                print("Patient data loaded successfully.")
        except Exception as e:
            print(f"Error opening patient data file: {filePath}")
            print(e)

    def is_data_loaded(self):
        return self.dataLoaded

    def monitor_patient_data(self):
        if not self.patients:
            print("No patient data loaded.")
            return

        # Select a random patient
        randomIndex = random.randint(0, len(self.patients) - 1)
        random_patient = random.choice(self.patients)

        print(f"Monitoring oxygen saturation for Patient ID {random_patient.id} in Room {random_patient.roomNumber}...")

        if random_patient.oxygenSaturation < self.oxygenSaturationLowerThreshold:
            self.send_alert(random_patient.id, random_patient.roomNumber, random_patient.oxygenSaturation, "Below")
        elif random_patient.oxygenSaturation > self.oxygenSaturationUpperThreshold:
            self.send_alert(random_patient.id, random_patient.roomNumber, random_patient.oxygenSaturation, "Above")
        else:
            print(f"Patient ID {random_patient.id} in Room {random_patient.roomNumber} has oxygen saturation within acceptable limits.")

    def send_alert(self, patient_id, roomNumber, oxygen_saturation, message):
        print(f"ALERT: Patient ID {patient_id} has {message} threshold oxygen saturation!\n"
              f"Oxygen Saturation: {oxygen_saturation}% (Threshold range: "
              f"{self.oxygenSaturationLowerThreshold}% - {self.oxygenSaturationUpperThreshold}%)\n")

        # Simulate oxygen flow adjustment
        oxygen_controller = OxygenSaturationController()
        choice = input("\nAdjust the oxygen flow.\n1. Start oxygen flow\n2. Stop oxygen flow\n3. Skip adjustment\nEnter your choice: ")

        if choice == '1':
            oxygen_controller.adjust_oxygen_flow(True)  # Start the oxygen flow
        elif choice == '2':
            oxygen_controller.adjust_oxygen_flow(False)  # Stop the oxygen flow
        else:
            print("No changes made to oxygen flow.")


class OxygenSaturationController:
    def adjust_oxygen_flow(self, start_flow):
        if start_flow:
            print("Oxygen flow started.")
        else:
            print("Oxygen flow stopped.")
            
class GlucoseLevelMonitor:
    glucose_level_lower_threshold = 85  # Lower threshold value
    glucose_level_upper_threshold = 100  # Upper threshold value

    def __init__(self):
        self.patients = []
        self.data_loaded = False

    def load_patient_data(self, filePath):
        try:
            with open("Patient_Dat.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header line
                for row in reader:
                    patient = PatientData(
                        id=int(row[0]),
                        roomNumber=int(row[1]),
                        age=int(row[2]),
                        gender=None,
                        disease=None,
                        weight=None,
                        currentPressure=None,
                        temperature=None,  # Placeholder, assuming no field for this
                              # Placeholder, assuming no field for this
                        respiratoryRate=None,  # Placeholder, assuming no field for this
                        oxygenSaturation=None,  # Placeholder, assuming no field for this
                        glucoseLevel=int(row[10])  # Placeholder, assuming no field for this
                    )
                    self.patients.append(patient)
                self.data_loaded = True
                print("Patient data loaded successfully.")
        except Exception as e:
            print(f"Error opening patient data file: {filePath}")
            print(e)

    def is_data_loaded(self):
        return self.data_loaded

    def monitor_patient_data(self):
        if not self.patients:
            print("No patient data loaded.")
            return

        #random.seed(1) 
        
        # Select a random patient
        randomIndex = random.randint(0, len(self.patients) - 1)
        random_patient = random.choice(self.patients)

        print(f"Monitoring glucose level for Patient ID {random_patient.id}"
              f" in Room {random_patient.roomNumber}...")

        # Check if glucose level is below or above the thresholds
        if random_patient.glucoseLevel < self.glucose_level_lower_threshold:
            self.send_alert(random_patient.id, random_patient.roomNumber, random_patient.glucoseLevel, "Below")
        elif random_patient.glucoseLevel > self.glucose_level_upper_threshold:
            self.send_alert(random_patient.id, random_patient.roomNumber, random_patient.glucoseLevel, "Above")
        else:
            print(f"Patient ID {random_patient.id} in Room {random_patient.roomNumber} "
                  f"has a glucose level within acceptable limits.")

    def send_alert(self, id, roomNumber, glucoseLevel, message):
        print(f"ALERT: Patient ID {id} has {message} threshold glucose level!\n"
              f"Glucose Level: {glucoseLevel} (Threshold range: "
              f"{self.glucose_level_lower_threshold} - {self.glucose_level_upper_threshold})\n")

        # Simulate adjusting glucose flow based on user input
        glucose_controller = GlucoseLevelController()
        choice = int(input("\nAdjust the Glucose Flow.\n"
                           "1. Start glucose flow\n"
                           "2. Stop glucose flow\n"
                           "3. Skip adjustment\nEnter your choice: "))

        if choice == 1:
            glucose_controller.adjust_glucose_flow(True)
        elif choice == 2:
            glucose_controller.adjust_glucose_flow(False)
        else:
            print("No changes made to glucose flow.")


class GlucoseLevelController:
    def adjust_glucose_flow(self, start_flow):
        if start_flow:
            print("Glucose flow started.")
        else:
            print("Glucose flow stopped.")
            
class OxygenSaturationController:
    def adjust_oxygen_flow(self, start_flow):
        if start_flow:
            print("Starting oxygen flow to maintain patient saturation.")
        else:
            print("Stopping oxygen flow to prevent over-saturation.")
        self.log_oxygen_flow_change(start_flow)

    def log_oxygen_flow_change(self, start_flow):
        try:
            with open("OxygenSaturationAdjustments.log", "a") as log_file:
                current_time = time.ctime()
                log_file.write(f"Time: {current_time}\nOxygen flow {'Started' if start_flow else 'Stopped'}\n\n")
        except Exception as e:
            print(f"Error: Unable to open log file for oxygen saturation adjustments. {e}")

class GlucoseLevelController:
    def adjust_glucose_flow(self, start_flow):
        if start_flow:
            print("Starting Glucose flow.")
        else:
            print("Stopping Glucose flow.")
        self.log_glucose_flow_change(start_flow)

    def log_glucose_flow_change(self, start_flow):
        try:
            with open("GlucoseLevelAdjustments.log", "a") as log_file:
                current_time = time.ctime()
                log_file.write(f"Time: {current_time}\nGlucose Flow {'Started' if start_flow else 'Stopped'}\n\n")
        except Exception as e:
            print(f"Error: Unable to open log file for glucose level adjustments. {e}")
