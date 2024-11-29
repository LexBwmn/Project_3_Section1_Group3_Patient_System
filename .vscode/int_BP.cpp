#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>

class BloodPressureMonitoring {
private:
    struct Range {
        int systolic_min;
        int systolic_max;
        int diastolic_min;
        int diastolic_max;
    };

    std::map<std::string, Range> normal_ranges;

    // how patient will be found 
    std::string generateKey(int age, const std::string& gender) {
        return 0;
    }

public:
    // Load CSV data
    bool loadCSV(const std::string& csvfile) {
        std::ifstream file(csvfile);
        if (!file.is_open()) {
            std::cerr << "Error opening file!" << std::endl;
            return false;
        }
    }

    // Check if blood pressure is within normal range
    bool isBloodPressureNormal(int systolic, int diastolic, int age, const std::string& gender) {
        std::string key = generateKey(age, gender); // acessing the correct patient 
        if (normal_ranges.find(key) == normal_ranges.end()) { // checking bp levels and patient  
            std::cerr << "No data for age " << age << " and gender " << gender << std::endl;
            return false;
        }

        Range range = normal_ranges[key]; // comparison of data (mapping)
        return systolic >= range.systolic_min && systolic <= range.systolic_max &&
            diastolic >= range.diastolic_min && diastolic <= range.diastolic_max;
    }

    // Evaluate patient status
    std::string evaluatePatientStatus(int systolic, int diastolic) {
        if (systolic < 90 || diastolic < 60)
            return "Low";
        else if (systolic <= 120 && diastolic <= 80)
            return "Normal";
        else if (systolic <= 139 || diastolic <= 89)
            return "Slightly High";
        else
            return "High";
    }

    // Generate report (test function -- i wanted to see that the monitoring of the bp was working correctly)
    void generateReport_BP(const std::string& patientID, int systolic, int diastolic, int age, const std::string& gender) {
        bool normal = isBloodPressureNormal(systolic, diastolic, age, gender);
        std::string status = evaluatePatientStatus(systolic, diastolic);

        std::cout << "Patient ID: " << patientID << std::endl;
        std::cout << "Systolic: " << systolic << ", Diastolic: " << diastolic << std::endl;
        std::cout << "Age: " << age << " Gender: " << gender << std::endl;
        std::cout << "Normal Range: " << (normal ? "Yes" : "No") << std::endl;
        std::cout << "Status: " << status << std::endl;
    }
};

#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(blood_pressure, m) {
    py::class_<BloodPressureMonitoring>(m, "BloodPressureMonitoring")
        .def(py::init<>())
        .def("isBloodPressureNormal", &BloodPressureMonitoring::isBloodPressureNormal)
        .def("generateReport_BP", &BloodPressureMonitoring::generateReport_BP)
        .def("evaluatePatientStatus", &BloodPressureMonitoring::evaluatePatientStatus);
}
