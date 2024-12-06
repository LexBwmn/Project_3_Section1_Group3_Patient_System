import csv
import random
import time

def read_medication_data(filename):
    #Reads medication data from a CSV file
    medications = []
    try:
        with open("medicationData.csv", mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                print(row)  
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except Exception as e:
        print(f"Error reading medication data: {e}")
    return medications


def simulate_medication_abnormalities(filename, patient_id, log_filename):
    #Simulates and logs medication abnormalities for a specific patient
    try:
        medications = read_medication_data(filename)
        abnormalities = []

        for med in medications:
            try:
                if "patientID" in med and med["patientID"].isdigit() and int(med["patientID"]) == int(patient_id):
                    is_abnormal = random.choice([True, False, False])  # 1/3 chance of abnormality
                    if is_abnormal:
                        print(f"ALERT: Missed or incorrect timing for {med['medication']} at {med['time']}.")
                        abnormalities.append(med)
                        log_abnormality(med, log_filename)
                    else:
                        print(f"Medication administered on time: {med['medication']} at {med['time']}.")
            except ValueError as ve:
                print(f"ValueError: {ve} - Check the patientID field in medication data.")
            except KeyError as ke:
                print(f"KeyError: {ke} - Missing expected key in medication data.")

        return abnormalities
    except Exception as e:
        print(f"Error during simulation: {e}")
        return []


def log_abnormality(medication, filename):
    #Logs abnormalities to a CSV file
    try:
        with open(filename, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Timestamp", "Patient ID", "Name", "Surname", "Medication", "Dosage", "Time", "Issue"])
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            writer.writerow([
                timestamp,
                medication.get("patientID", "Unknown"),
                medication.get("name", "Unknown"),
                medication.get("surname", "Unknown"),
                medication.get("medication", "Unknown"),
                medication.get("dosage", "Unknown"),
                medication.get("time", "Unknown"),
                "Missed or incorrect timing"
            ])
    except Exception as e:
        print(f"Error logging abnormality: {e}")


def display_abnormalities(log_filename, patient_id):
    #Displays logged abnormalities for a specific patient
    try:
        with open(log_filename, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            abnormalities = [
                row for row in csv_reader
                if int(row["Patient ID"]) == int(patient_id)  
            ]
            return abnormalities
    except FileNotFoundError:
        print(f"Error: The file {log_filename} was not found.")
        return []
    except ValueError as ve:
        print(f"ValueError: {ve} - Check the Patient ID field in log file.")
        return []
    except Exception as e:
        print(f"Error reading abnormalities: {e}")
        return []