#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cstdlib>
#include <ctime>
#include <thread>
#include <chrono>
#include <conio.h> // For keyboard input control
#include <set>

using namespace std;

// Medication data structure
struct MedicationData {
    int patientID = 0;    // Patient ID
    int age = 0;          // Age
    int gender = 0;       // 0: Male, 1: Female
    string medication = "";
    string dosage = "";
    string time = "";
};

// Function to read medication data from CSV
vector<MedicationData> readMedicationData(const string& filename) {
    vector<MedicationData> medications;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << filename << endl;
        return medications;
    }

    string line;
    getline(file, line); // Skip header row

    while (getline(file, line)) {
        stringstream ss(line);
        MedicationData medData;

        ss >> medData.patientID;
        ss.ignore();
        ss >> medData.age;
        ss.ignore();
        ss >> medData.gender;
        ss.ignore();
        getline(ss, medData.medication, ',');
        getline(ss, medData.dosage, ',');
        getline(ss, medData.time);

        medications.push_back(medData);
    }

    file.close();
    return medications;
}

// Function to display all patient information
void displayAllPatients(const vector<MedicationData>& medications) {
    if (medications.empty()) {
        cout << "No medication data available." << endl;
        return;
    }

    set<int> displayedIDs; 

    cout << "\nPatient Information:\n";
    for (const auto& med : medications) {
        if (displayedIDs.find(med.patientID) == displayedIDs.end()) { 
            cout << "Patient ID: " << med.patientID
                << ", Age: " << med.age
                << ", Gender: " << (med.gender == 0 ? "Male" : "Female") << endl;
            displayedIDs.insert(med.patientID); 
        }
    }
}

// Function to display medication details for a specific patient
void displayMedicationDetails(const vector<MedicationData>& medications, int patientID) {
    cout << "\nMedication Details for Patient ID " << patientID << ":\n";
    bool found = false;

    for (const auto& med : medications) {
        if (med.patientID == patientID) {
            cout << "Medication: " << med.medication
                << ", Dosage: " << med.dosage
                << ", Time: " << med.time << endl;
            found = true;
        }
    }

    if (!found) {
        cout << "No medication details found for Patient ID " << patientID << "." << endl;
    }
}

// Function to simulate and log medication abnormalities
void simulateAndLogAbnormalities(const vector<MedicationData>& medications, const string& abnormalCSV, int patientID) {
    ofstream file(abnormalCSV, ios::app);
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << abnormalCSV << " for logging!" << endl;
        return;
    }

    bool found = false;
    cout << "\nSimulating medication timings for Patient ID " << patientID << "...\n";
    for (const auto& med : medications) {
        if (med.patientID == patientID) {
            found = true;

            // Randomize abnormality (1/3 chance)
            bool isAbnormal = rand() % 3 == 0;

            if (isAbnormal) {
                cout << "ALERT: Missed or incorrect medication timing detected for " << med.medication << " at " << med.time << endl;

                // Log to abnormal CSV
                auto now = chrono::system_clock::to_time_t(chrono::system_clock::now());
                char timestamp[20];
                strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", localtime(&now));

                file << timestamp << ","
                    << med.patientID << ","
                    << med.age << ","
                    << med.gender << ","
                    << med.medication << ","
                    << med.dosage << ","
                    << med.time << ","
                    << "Missed or incorrect timing\n";
            }
            else {
                cout << "Medication administered on time: " << med.medication << " at " << med.time << endl;
            }
        }
    }

    if (!found) {
        cout << "No medication data found for Patient ID " << patientID << "." << endl;
    }

    file.close();
}

// Function to display abnormalities
void displayAbnormalities(const string& abnormalCSV, int patientID) {
    ifstream file(abnormalCSV);
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << abnormalCSV << endl;
        return;
    }

    string line;
    getline(file, line); // Skip header row

    cout << "\nAbnormalities for Patient ID " << patientID << ":\n";
    bool found = false;

    while (getline(file, line)) {
        stringstream ss(line);
        int id;
        ss.ignore(20, ','); // Skip timestamp
        ss >> id;

        if (id == patientID) {
            cout << line << endl;
            found = true;
        }
    }

    if (!found) {
        cout << "No abnormalities detected for Patient ID " << patientID << "." << endl;
    }

    file.close();
}

// Submenu options for specific patient
void showSubMenu(const vector<MedicationData>& medications, const string& abnormalCSV) {
    int patientID;
    cout << "Enter Patient ID: ";
    cin >> patientID;

    bool subExit = false;
    while (!subExit) {
        cout << "\nSubmenu Options:\n";
        cout << "a. Display Medication Details\n";
        cout << "b. Simulate and Log Abnormalities\n";
        cout << "c. Display Abnormalities\n";
        cout << "q. Return to Main Menu\n";
        cout << "Enter your choice: ";
        char choice;
        cin >> choice;

        switch (choice) {
        case 'a':
            displayMedicationDetails(medications, patientID);
            break;
        case 'b':
            simulateAndLogAbnormalities(medications, abnormalCSV, patientID);
            break;
        case 'c':
            displayAbnormalities(abnormalCSV, patientID);
            break;
        case 'q':
            subExit = true;
            break;
        default:
            cout << "Invalid choice! Please try again.\n";
        }
    }
}

// Main menu
void showMenu(const vector<MedicationData>& medications, const string& abnormalCSV) {
    bool exit = false;
    while (!exit) {
        cout << "\nMain Menu:\n";
        cout << "1. Display All Patients\n";
        cout << "2. Access Specific Patient Data\n";
        cout << "3. Quit\n";
        cout << "Enter your choice: ";
        int choice;
        cin >> choice;

        switch (choice) {
        case 1:
            displayAllPatients(medications);
            break;
        case 2:
            showSubMenu(medications, abnormalCSV);
            break;
        case 3:
            exit = true;
            cout << "Exiting program...\n";
            break;
        default:
            cout << "Invalid choice! Please try again.\n";
        }
    }
}

int main() {
    string medicationFile = "medicationData.csv";
    string abnormalFile = "medicationAbnormal.csv";

    // Read data from medication CSV
    vector<MedicationData> medications = readMedicationData(medicationFile);

    // Show the main menu
    showMenu(medications, abnormalFile);

    return 0;
}