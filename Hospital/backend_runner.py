import subprocess

def run_backend_with_input(patient_id):
    backend_path = "HeartRateMonitor.exe"  # Remove "./"
    patient_data_path = "patientData.csv"  # Remove "./"
    abnormal_data_path = "abnormal.csv"    # Remove "./"

    try:
        # Start the backend process
        process = subprocess.Popen(
            [backend_path, patient_data_path, abnormal_data_path, str(patient_id)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Prepare user inputs
        user_inputs = [
            "2\n",  # Menu choice
            f"{patient_id}\n"  # Patient ID
        ]

        # Communicate with the backend process
        stdout, stderr = process.communicate(input="".join(user_inputs), timeout=30)

        # Log the backend outputs
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")

        # Check the backend output
        if process.returncode == 0:
            return stdout.strip()  # Return successful output
        else:
            return f"Error:\n{stderr.strip()}"  # Return error

    except subprocess.TimeoutExpired:
        process.kill()  # Kill the process if it times out
        return "Error: Backend process timed out!"
    except FileNotFoundError:
        return "Error: One or more required files are missing in the project folder!"
    except Exception as e:
        return f"Unexpected error: {e}"