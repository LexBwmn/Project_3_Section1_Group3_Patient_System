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

    std::string generateKey(int age, const std::string& gender);

public:
    bool loadCSV(const std::string& csvfile);
    bool isBloodPressureNormal(int systolic, int diastolic, int age, const std::string& gender);
    std::string evaluatePatientStatus(int systolic, int diastolic);
    void generateReport_BP(const std::string& patientID, int systolic, int diastolic, int age, const std::string& gender);
};