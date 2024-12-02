import csv
import time
import random

def log_abnormality(patient, range_type, measured_value):
    filename = "abnormalHeart.csv"
    try:
        with open(filename, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)

            # Write headers if the file is empty
            if file.tell() == 0:
                writer.writerow([
                    "Timestamp", "Patient ID", "Name", "Surname", "Gender",
                    "Threshold Low", "Threshold High", "Measured Range", "Measured Value", "Final Record"
                ])

            # Create a timestamp for the entry
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # Write the row to the file
            writer.writerow([
                timestamp, patient["id"], patient["name"], patient["surname"],
                patient["gender"], patient["thresholdLow"], patient["thresholdHigh"],
                range_type, measured_value, "Yes"
            ])
    except Exception as e:
        print(f"Error logging abnormality: {e}")


def simulate_heart_rate(patient, callback, stop_event):
    threshold_low = patient["thresholdLow"]
    threshold_high = patient["thresholdHigh"]

    # Initial heart rate is set within the patient's normal range
    current_heart_rate = random.randint(threshold_low, threshold_high)
    print(f"Initial Heart Rate: {current_heart_rate} bpm")

    max_abnormal_value = None  # To track the highest abnormal value
    max_abnormal_range = None  # To track the range of the highest abnormal value

    try:
        # Randomly choose an initial range (Low, Normal, High)
        range_type = random.choices(["Normal", "Low", "High"], weights=[60, 20, 20], k=1)[0]

        # Determine the range boundaries based on the selected range
        if range_type == "Low":
            low = threshold_low - 5
            high = threshold_low - 1
            range_name = "Low"
        elif range_type == "Normal":
            low = threshold_low
            high = threshold_high
            range_name = "Normal"
        else:  # High
            low = threshold_high + 1
            high = threshold_high + 5
            range_name = "High"

        print(f"Selected Range: {range_name} ({low}-{high})")

        # Generate heart rate values until the stop event is triggered
        while not stop_event.is_set():
            if range_name == "Normal":
                # Stabilize heart rate changes within a small range
                next_heart_rate = current_heart_rate + random.choice([-2, -1, 0, 1, 2])
                next_heart_rate = max(min(next_heart_rate, high), low)
            else:
                # Randomly generate values within the selected range for Low or High
                next_heart_rate = random.randint(low, high)

            print(f"Generated Heart Rate: {next_heart_rate} bpm")

            # Check if the generated value is abnormal
            is_abnormal = next_heart_rate < threshold_low or next_heart_rate > threshold_high

            # Update the highest abnormal value if necessary
            if is_abnormal:
                if max_abnormal_value is None or next_heart_rate > max_abnormal_value:
                    max_abnormal_value = next_heart_rate
                    max_abnormal_range = range_name

            # Update the UI using the callback function
            callback(next_heart_rate, range_name, is_abnormal, f"{range_name} ({low}-{high})")

            # Update the current heart rate
            current_heart_rate = next_heart_rate

            time.sleep(1)  # Delay between heart rate readings

    except Exception as e:
        print(f"Simulation stopped: {str(e)}")

    finally:
        # Log the highest abnormal value when the simulation stops
        if max_abnormal_value is not None:
            log_abnormality(patient, max_abnormal_range, max_abnormal_value)
            print(f"Final abnormal value logged: {max_abnormal_value} bpm ({max_abnormal_range})")