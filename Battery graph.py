import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('battery_data.csv')

# Display first rows
print(data.head())

# Plot Voltage vs Time
plt.figure()
plt.plot(data['Time (s)'], data['Voltage (V)'])
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Voltage vs Time')
plt.show()

# Plot Current vs Time
plt.figure()
plt.plot(data['Time (s)'], data['Current (A)'])
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title('Current vs Time')
plt.show()

# Calculate Capacity (Ah)
data['Time_diff'] = data['Time (s)'].diff().fillna(0)
capacity = (data['Current (A)'] * data['Time_diff']).sum() / 3600

print("Estimated Capacity (Ah):", capacity)

# Detect Overvoltage (> 58.4V for 16S LiFePO4)
overvoltage = data[data['Voltage (V)'] > 58.4]

print("Overvoltage Events:")
print(overvoltage)

# Voltage vs Time
plt.figure()
plt.plot(data['Time (s)'], data['Voltage (V)'])
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Battery Voltage vs Time')
plt.grid()
plt.savefig('voltage.png')
plt.show()

# Current vs Time
plt.figure()
plt.plot(data['Time (s)'], data['Current (A)'])
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title('Battery Current vs Time')
plt.grid()
plt.savefig('current.png')
plt.show()

# Temperature vs Time
plt.figure()
plt.plot(data['Time (s)'], data['Temperature (°C)'])
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.title('Battery Temperature vs Time')
plt.grid()
plt.savefig('temperature.png')
plt.show()

# SOC Calculation
total_capacity = 50  # Ah (your battery)

data['Time_diff'] = data['Time (s)'].diff().fillna(0)

data['Ah_used'] = (data['Current (A)'] * data['Time_diff']) / 3600

data['SOC (%)'] = 100 - (data['Ah_used'].cumsum() / total_capacity * 100)

data.to_csv('battery_with_soc.csv', index=False)

# Plot SOC
plt.figure()
plt.plot(data['Time (s)'], data['SOC (%)'])
plt.xlabel('Time (s)')
plt.ylabel('SOC (%)')
plt.title('State of Charge vs Time')
plt.grid()
plt.savefig('soc.png')
plt.show()

# Energy calculation
data['Power (W)'] = data['Voltage (V)'] * data['Current (A)']
data['Energy (Wh)'] = (data['Power (W)'] * data['Time_diff']) / 3600

charge_energy = data[data['Current (A)'] > 0]['Energy (Wh)'].sum()
discharge_energy = abs(data[data['Current (A)'] < 0]['Energy (Wh)'].sum())

efficiency = (discharge_energy / charge_energy) * 100

print("Efficiency (%):", round(efficiency, 2))
