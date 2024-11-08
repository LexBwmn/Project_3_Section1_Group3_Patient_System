#pragma once
#include<iostream>

class BloodPressureMonitoring {
private:
	int pressure;

	loadCSV();

	readCSV();

	getPressure();

	ComparePressure();

public:

	AlertBloodPressure();

}

class medicineMonitoring {
private:
	std::string typeOfMedication;

	float Dosage;

	//PatientData
public:
	loadCSV();

	readCSV();

	GetMedication();

	GetDosage();

	GetType();

	ValidateDosage();

	AdjustDosage();

}
