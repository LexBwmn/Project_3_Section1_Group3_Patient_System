#define _CRT_SECURE_NO_WARNINGS
#include "heartRate.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cstdlib>
#include <ctime>
#include <thread>
#include <chrono>
#include <conio.h>
#include <map>

// Function to read patient data from a CSV file
std::vector<PatientData> readPatientsFromCSV(const std::string& filename) {
    std::vector<PatientData> patients;
    std::ifstream file(filename);
    std::string line;

    // Skip the header row
    std::getline(file, line);

    // Read each line and parse patient data
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        PatientData patient;

        ss >> patient.patientID;
        ss.ignore();
        ss >> patient.age;
        ss.ignore();
        ss >> patient.gender;
        ss.ignore();
        ss >> patient.thresholdLow;
        ss.ignore();
        ss >> patient.thresholdHigh;

        patients.push_back(patient);
    }

    file.close();
    return patients;
}

// Function to display abnormalities from the CSV file
void displayAbnormalities(const std::string& abnormalCSV, int patientID) {
    std::ifstream file(abnormalCSV);
    std::string line;
    bool abnormalFound = false;

    // Skip the header row
    std::getline(file, line);

    // Check each row for matching patient ID
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        int id;
        ss.ignore(20, ','); // Skip timestamp
        ss >> id;
        if (id == patientID) {
            std::cout << line << std::endl;
            abnormalFound = true;
        }
    }

    if (!abnormalFound) {
        std::cout << "No abnormalities detected for Patient ID " << patientID << "." << std::endl;
    }

    file.close();
}

// Function to log abnormalities to a CSV file
void logAbnormality(const std::string& filename, const PatientData& patient, const std::string& measuredRange, int measuredValue) {
    std::ofstream file(filename, std::ios::app); // Open file in append mode
    if (!file.is_open()) {
        std::cerr << "Error: Could not open abnormal CSV file for logging!" << std::endl;
        return;
    }

    // Get the current timestamp
    auto now = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    char timestamp[20];
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", localtime(&now));

    // Write data to the CSV file
    file << timestamp << ","
        << patient.patientID << ","
        << patient.age << ","
        << patient.gender << ","
        << patient.thresholdLow << ","
        << patient.thresholdHigh << ","
        << measuredRange << ","
        << measuredValue << "\n";

    file.close();
}

// Function to show the current heart rate
void showCurrentHeartRate(int patientID, const std::vector<PatientData>& patientData, const std::string& abnormalCSV) {
    bool patientFound = false;

    for (const auto& record : patientData) {
        if (record.patientID == patientID) {
            patientFound = true;

            int rangeType = rand() % 3; // 0 = Low, 1 = Normal, 2 = High
            int low = 0, high = 0;
            std::string rangeName = "";
            int measuredValue = 0;
            int optimalValue = 0; // To store the most optimal value

            if (rangeType == 0) {
                low = record.thresholdLow - 5;
                high = record.thresholdLow - 1;
                rangeName = "Low";
                optimalValue = high;
            }
            else if (rangeType == 1) {
                low = record.thresholdLow;
                high = record.thresholdHigh;
                rangeName = "Normal";
            }
            else {
                low = record.thresholdHigh + 1;
                high = record.thresholdHigh + 5;
                rangeName = "High";
                optimalValue = low;
            }

            while (true) {
                measuredValue = rand() % (high - low + 1) + low;

                if (rangeName == "Low" || rangeName == "High") {
                    std::cout << "\n\033[1;31mALERT: Immediate intervention required!\033[0m" << std::endl;
                }

                std::cout << "Heart Rate (bpm): " << measuredValue << " (" << rangeName << ")" << std::endl;

                if (rangeName == "Low" && measuredValue < optimalValue) {
                    optimalValue = measuredValue;
                }
                if (rangeName == "High" && measuredValue > optimalValue) {
                    optimalValue = measuredValue;
                }

                std::this_thread::sleep_for(std::chrono::seconds(1));

                if (_kbhit()) {
                    char ch = _getch();
                    if (ch == 'Q' || ch == 'q') {
                        if (rangeName == "Low" || rangeName == "High") {
                            logAbnormality(abnormalCSV, record, rangeName, optimalValue);
                        }
                        return;
                    }
                }
            }
        }
    }

    if (!patientFound) {
        std::cout << "Error: Patient ID " << patientID << " does not exist in the database!" << std::endl;
    }
}