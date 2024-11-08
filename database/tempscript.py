import sqlite3
import random
import time
from datetime import datetime
# from pymodbus.client import ModbusTcpClient

# Connect to the SQLite database
db_file = 'testDB.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to add random temperature data
def add_temperature_data(temperature, timestamp):
  cursor.execute('''INSERT INTO temperature_data (timestamp, temperature) VALUES (?, ?)''', (timestamp, temperature))
  conn.commit()
  print(f"Added temperature data: {timestamp} - {temperature}°C")

# Function to add random pressure data
def add_pressure_data(pressure, timestamp):
  cursor.execute('''INSERT INTO pressure_data (timestamp, pressure) VALUES (?, ?)''', (timestamp, pressure))
  conn.commit()
  print(f"Added pressure data: {timestamp} - {pressure} hPa")

# Function to add random irradiance data
def add_irradiance_data(irradiance, timestamp):
  cursor.execute('''INSERT INTO irradiance_data (timestamp, irradiance) VALUES (?, ?)''', (timestamp, irradiance))
  conn.commit()
  print(f"Added irradiance data: {timestamp} - {irradiance} W/m²")

# Function to add random humidity data
def add_humidity_data(humidity, timestamp):
  cursor.execute('''INSERT INTO humidity_data (timestamp, humidity) VALUES (?, ?)''', (timestamp, humidity))
  conn.commit()
  print(f"Added humidity data: {timestamp} - {humidity}%")

# Function to add random garage data
def add_garage_data(garage, timestamp):
  cursor.execute('''INSERT INTO garage_data (timestamp, garage) VALUES (?, ?)''', (timestamp, garage))
  conn.commit()
  print(f"Added garage data: {timestamp} - {garage}")

# Function to add random bathroom data
def add_bathroom_data(bathroom, timestamp):
  cursor.execute('''INSERT INTO bathroom_data (timestamp, bathroom) VALUES (?, ?)''', (timestamp, bathroom))
  conn.commit()
  print(f"Added bathroom data: {timestamp} - {bathroom}")

# Function to add random bedroom data
def add_bedroom_data(bedroom, timestamp):
  cursor.execute('''INSERT INTO bedroom_data (timestamp, bedroom) VALUES (?, ?)''', (timestamp, bedroom))
  conn.commit()
  print(f"Added bedroom data: {timestamp} - {bedroom}")

# Function to add random lr data
def add_lr_data(lr, timestamp):
  cursor.execute('''INSERT INTO lr_data (timestamp, lr) VALUES (?, ?)''', (timestamp, lr))
  conn.commit()
  print(f"Added lr data: {timestamp} - {lr}")

def add_random_data():
  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  temperature = round(random.uniform(15.00, 30.00), 2)
  pressure = round(random.uniform(950.00, 1050.00), 2)
  irradiance = round(random.uniform(0, 1000), 2)
  humidity = round(random.uniform(0, 100), 2)
  garage = random.choice([0, 1])
  bathroom = random.choice([0, 1])
  bedroom = random.choice([0, 1])
  lr = random.choice([0, 1])
  
  add_temperature_data(temperature, timestamp)
  add_pressure_data(pressure, timestamp)
  add_irradiance_data(irradiance, timestamp)
  add_humidity_data(humidity, timestamp)
  add_garage_data(garage, timestamp)
  add_bathroom_data(bathroom, timestamp)
  add_bedroom_data(bedroom, timestamp)
  add_lr_data(lr, timestamp)

def read_sensor_file(file_path, scenario_name):
  sensors = {}
  start_reading = False

  with open(file_path, "r") as file:
    for line in file:
      line = line.strip()
      
      # Check for scenario marker
      if line.lower().startswith('#') and scenario_name.lower() in line.lower():
        start_reading = True
        continue
      elif line.startswith('#'):
        start_reading = False
      
      if start_reading:
        if not line or line.startswith('#'):
          continue
        
        parts = line.split()
        sensor_name = parts[0].strip("'")
        values = list(map(int, parts[1:]))
        sensors[sensor_name] = values
  return sensors

def simulate_sensors(file_path):
  scenarios = {
    '1': 'Rainstorm',
    '2': 'Sunny',
    '3': 'Snowing',
    '4': 'Tornado',
    '5': 'Progressive Weather',
    '6': 'Random Data',
    '7': 'Exit'
  }

  while True:
    print("\nSelect a scenario to simulate:")
    for key, scenario in scenarios.items():
      print(f"{key}: {scenario}")
    selection = input("Enter your choice (1-7): ")
    selected_scenario = scenarios.get(selection, None)

    if not selected_scenario:
      print("Invalid selection, please choose a valid number (1-7).")
      continue
    
    if selection == '7':
      exit()

    while True:
      try:
        num_data_points = int(input("How many data points would you like to simulate? (1-20): "))
        if 1 <= num_data_points <= 20:
          break
        else:
          print("Please enter a number between 1 and 20.")
      except ValueError:
        print("Invalid input. Please enter a valid number.")

    data_count = 0

    if selection != '6':
      sensors = read_sensor_file(file_path, selected_scenario)

      if not sensors:
        print("No data found for the selected scenario.")
        continue
      
      for i in range(20):
        values_at_index = []
        # Go through each sensor in the dictionary
        for sensor_name, sensor_values in sensors.items():
          # Ensure the current index exists for this sensor's list
          if i < len(sensor_values):
            values_at_index.append(sensor_values[i])
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_humidity_data(values_at_index[0], timestamp)
        add_temperature_data(values_at_index[1], timestamp)
        add_irradiance_data(values_at_index[2], timestamp)
        add_pressure_data(values_at_index[3], timestamp)
        add_garage_data(values_at_index[4], timestamp)
        add_bathroom_data(values_at_index[5], timestamp)
        add_bedroom_data(values_at_index[6], timestamp)
        add_lr_data(values_at_index[7], timestamp)
        # write_to_holding_register(client, sensor_registers[sensor_name], value)

        print("-" * 30)
        data_count += 1
        if data_count >= num_data_points:
          break
        time.sleep(10)
      print("All sensor data has been read. Restarting simulation...\n")
    if selection == '6':
      while (data_count < num_data_points):
        add_random_data()
        print("-" * 30)
        data_count += 1
        if data_count >= num_data_points:
          break
        time.sleep(10)

if __name__ == "__main__":
  file_path = "Sensor_data"
  # client = ModbusTcpClient('100.108.218.111', port=502)
  sensor_registers = {
    'Barometer': 1027,
    'Humidity': 1028,
    'Motion_Sensor_Garage': 1029,
    'Temperature': 1025,
    'SunRadiation': 1026,
    'Pressure': 1033,
    'Motion_Sensor_Bathroom': 1031,
    'Motion_Sensor_Bedroom': 1030,
    'Motion_Sensor_LR': 1032,
    'LightBrightness': 1
  }
  simulate_sensors(file_path)

# Close the database connection
# cursor.close()
# conn.close()
