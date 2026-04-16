import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

print(" Training Q-Sure Sentinel: Fraud Detection Model...")

# 1. Generate Synthetic 'Normal' Rider Data
# Features: [velocity_kmh, altitude_diff_m, device_temp_c]
num_samples = 1000
normal_velocity = np.random.normal(25, 5, num_samples) # Avg bike speed 25kmh
normal_altitude = np.random.normal(2, 1, num_samples)   # Flat ground movement
normal_temp = np.random.normal(38, 2, num_samples)     # Phone temp in use

X_train = pd.DataFrame({
    'velocity_kmh': normal_velocity,
    'altitude_diff_m': normal_altitude,
    'device_temp_c': normal_temp
})

# 2. Train Isolation Forest
# contamination=0.05 means we expect 5% of data to be 'anomalous'
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_train)

# 3. Save the Fraud Model
joblib.dump(model, 'qsure_fraud_model.pkl')
print(" Fraud Model saved as 'qsure_fraud_model.pkl'")

# --- TEST THE BRAIN ---
# Scenario: A spoofer 'teleports' (velocity 150kmh) from their couch (0 altitude change)
test_spoof = pd.DataFrame([[150.0, 0.0, 25.0]], columns=X_train.columns)
prediction = model.predict(test_spoof) # -1 is Fraud, 1 is Normal

if prediction[0] == -1:
    print(" ALERT: Fraudulent activity detected by ML!")