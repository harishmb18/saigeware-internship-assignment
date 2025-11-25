import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# STEP 1: Load the dataset
df = pd.read_csv("wellness_data.csv")

print("Loaded Wellness Data:")
print(df)
print("\n----------------------------------------\n")

# STEP 2: Function to calculate Z-score anomalies
def detect_anomalies_zscore(series):
    mean = series.mean()
    std = series.std()

    # z-score = (value - mean) / std
    z_scores = (series - mean) / std

    # Mark anomalies where |z| > 2
    return z_scores.abs() > 2, z_scores

# STEP 3: Detect anomalies for heart_rate
heart_anomalies, hr_z = detect_anomalies_zscore(df["heart_rate"])
df["heart_rate_z"] = hr_z
df["heart_rate_anomaly"] = heart_anomalies

# STEP 4: Detect anomalies for sleep_hours
sleep_anomalies, sleep_z = detect_anomalies_zscore(df["sleep_hours"])
df["sleep_hours_z"] = sleep_z
df["sleep_hours_anomaly"] = sleep_anomalies

# STEP 5: Show anomalies
anomalies = df[(df["heart_rate_anomaly"] == True) | (df["sleep_hours_anomaly"] == True)]

print("Detected Anomalies:")
print(anomalies)
print("\n----------------------------------------\n")

# STEP 6: Save anomalies to a new file
anomalies.to_csv("anomalies_detected.csv", index=False)
print("Saved anomalies to 'anomalies_detected.csv'")


print("\n----------------------------------------")
print("IQR-Based Anomaly Detection")
print("----------------------------------------")

def detect_anomalies_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    anomalies = (series < lower_bound) | (series > upper_bound)

    return anomalies, lower_bound, upper_bound

# IQR for heart_rate
hr_iqr_anom, hr_low, hr_high = detect_anomalies_iqr(df["heart_rate"])
df["heart_rate_iqr_anomaly"] = hr_iqr_anom

# IQR for sleep_hours
sleep_iqr_anom, sh_low, sh_high = detect_anomalies_iqr(df["sleep_hours"])
df["sleep_hours_iqr_anomaly"] = sleep_iqr_anom

# Show detected anomalies
iqr_anomalies = df[(df["heart_rate_iqr_anomaly"] == True) | (df["sleep_hours_iqr_anomaly"] == True)]

print("Detected IQR Anomalies:")
print(iqr_anomalies)

# Save the IQR anomalies
iqr_anomalies.to_csv("anomalies_iqr.csv", index=False)
print("Saved 'anomalies_iqr.csv'")



print("\n----------------------------------------")
print("Creating anomaly visualization plots...")
print("----------------------------------------")

# Convert date column to datetime for plotting
df["date"] = pd.to_datetime(df["date"])

# 1) Plot Heart Rate with anomalies (using Z-score anomalies)
plt.figure()
plt.plot(df["date"], df["heart_rate"], marker="o", label="Heart Rate")

# Mark anomalies in red
hr_anom_points = df[df["heart_rate_anomaly"] == True]
plt.scatter(hr_anom_points["date"], hr_anom_points["heart_rate"], marker="o", s=80, label="Anomaly",)

plt.xlabel("Date")
plt.ylabel("Heart Rate (bpm)")
plt.title("Heart Rate Over Time (Anomalies Highlighted)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("heart_rate_anomalies.png")
plt.close()

# 2) Plot Sleep Hours with anomalies (using Z-score anomalies)
plt.figure()
plt.plot(df["date"], df["sleep_hours"], marker="o", label="Sleep Hours")

sleep_anom_points = df[df["sleep_hours_anomaly"] == True]
plt.scatter(sleep_anom_points["date"], sleep_anom_points["sleep_hours"], marker="o", s=80, label="Anomaly",)

plt.xlabel("Date")
plt.ylabel("Sleep Hours")
plt.title("Sleep Hours Over Time (Anomalies Highlighted)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("sleep_hours_anomalies.png")
plt.close()

print("Saved 'heart_rate_anomalies.png' and 'sleep_hours_anomalies.png'")
