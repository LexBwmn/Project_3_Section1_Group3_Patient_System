#define _CRT_SECURE_NO_WARNINGS
#include "heartRate.h"
#include <iostream>
#include <string>

using namespace std;

// Function to display the submenu
void showSubMenu() {
    cout << "\nSubmenu Options:" << endl;
    cout << "a. Patient Information" << endl;
    cout << "b. Show Current Heart Rate" << endl;
    cout << "c. Display Abnormalities" << endl;
    cout << "q. Return to Main Menu" << endl;
}

// Function to display the main menu
void showMenu() {
    cout << "\nMenu Options:" << endl;
    cout << "1. Display All Patient Information" << endl;
    cout << "2. Access Specific Patient Data" << endl;
    cout << "3. Quit" << endl;
}

int main() {
    string patientFilename = "patientData.csv";
    string abnormalFilename = "abnormal.csv";

    vector<PatientData> patients = readPatientsFromCSV(patientFilename);

    bool exit = false;

    while (!exit) {
        showMenu();
        int choice;
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
        case 1: {
            for (const auto& patient : patients) {
                cout << "Patient ID: " << patient.patientID
                    << ", Age: " << patient.age
                    << ", Gender: " << (patient.gender == 0 ? "Male" : "Female")
                    << ", Threshold Low: " << patient.thresholdLow
                    << ", Threshold High: " << patient.thresholdHigh << endl;
            }
            break;
        }
        case 2: {
            int patientID;
            cout << "Enter Patient ID: ";
            cin >> patientID;

            bool subExit = false;
            while (!subExit) {
                showSubMenu();
                char subChoice;
                cout << "Enter your choice: ";
                cin >> subChoice;

                switch (subChoice) {
                case 'a':
                    for (const auto& patient : patients) {
                        if (patient.patientID == patientID) {
                            cout << "Patient ID: " << patient.patientID
                                << ", Age: " << patient.age
                                << ", Gender: " << (patient.gender == 0 ? "Male" : "Female")
                                << ", Threshold Low: " << patient.thresholdLow
                                << ", Threshold High: " << patient.thresholdHigh << endl;
                            break;
                        }
                    }
                    break;
                case 'b':
                    showCurrentHeartRate(patientID, patients, abnormalFilename);
                    break;
                case 'c':
                    displayAbnormalities(abnormalFilename, patientID);
                    break;
                case 'q':
                    subExit = true;
                    break;
                default:
                    cout << "Invalid choice! Please select a valid option." << endl;
                }
            }
            break;
        }
        case 3:
            cout << "Exiting program..." << endl;
            exit = true;
            break;
        default:
            cout << "Invalid choice! Please select a valid option." << endl;
        }
    }

    return 0;
}