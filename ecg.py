import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file while skipping the first row (header)
data = pd.read_csv("ecg_data.csv", header=None, names=["ECG"], nrows=5000, skiprows=1)

# Plot the ECG signal
plt.figure(figsize=(10, 4))
plt.plot(data["ECG"], color="blue")
plt.title("ECG Signal (First 1000 Data Points)")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.grid(True)

# Show the plot
plt.show()
