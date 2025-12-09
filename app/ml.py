import math


def predict_risk(patient):
    z = 0.02 * patient.get("age", 0) + 0.01 * patient.get("avg_glucose_level", 0) + 0.01 * patient.get("bmi", 0)
    z += 0.5 * float(patient.get("hypertension", 0)) + 0.5 * float(patient.get("stroke", 0))
    return round(1 / (1 + math.exp(-z)), 4)
