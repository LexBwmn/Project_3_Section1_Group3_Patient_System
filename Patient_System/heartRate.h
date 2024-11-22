#pragma once
#include <string>
#include <vector>

struct PatientData {
    int patientID;       // Patient ID
    int age;             // Age
    int gender;          // 0: Male, 1: Female
    int thresholdLow;    // Low threshold for heart rate
    int thresholdHigh;   // High threshold for heart rate
};

// Function prototypes
std::vector<PatientData> readPatientsFromCSV(const std::string& filename);
void displayAbnormalities(const std::string& abnormalCSV, int patientID);
void logAbnormality(const std::string& filename, const PatientData& patient, const std::string& measuredRange, int measuredValue);
void showCurrentHeartRate(int patientID, const std::vector<PatientData>& patientData, const std::string& abnormalCSV);