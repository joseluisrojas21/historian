import sqlite3
import random
import time
from datetime import datetime
from pymodbus.client import ModbusTcpClient

# Connect to the SQLite database
db_file = '/var/www/historian/database/testDB.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

def insert_data(table, data):
  query = f"INSERT INTO {table} (timestamp, {table[:-5]}) VALUES (?, ?)"
  cursor.executemany(query, data)
  conn.commit()
  
  print(f"Added {table[:-5]} data:")
  for row in data:
    timestamp, value = row
    print(f"  {timestamp} - {value}")

def addLog(coils, timestamp):
  descriptions = [
    ("Fan", "The fan turned on"),
    ("Sunny", "The weather is sunny"),
    ("Storm", "A storm is occurring"),
    ("Dehumidifier", "The dehumidifier turned on"),
    ("Garage Lightbulb", "The garage lightbulb turned on"),
    ("Bedroom Lightbulb", "The bedroom lightbulb turned on"),
    ("Bathroom Lightbulb", "The bathroom lightbulb turned on"),
    ("Living Room Lightbulb", "The living room lightbulb turned on"),
    ("Tornado", "A tornado is approaching"),
    ("Alarm Light", "The alarm light turned on because of the tornado"),
    ("Snowing", "It is snowing"),
    ("Heater", "The heater turned on")
  ]

  for address, coil in enumerate(coils):
    if coil:
      event, description = descriptions[address]
      cursor.execute('''INSERT INTO logs (event, timestamp, description) VALUES (?, ?, ?)''', (event, timestamp, description))
  
  conn.commit()

def createTables():
    table_creation_queries = [
        '''CREATE TABLE IF NOT EXISTS temperature_data (id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, temperature REAL NOT NULL)''',
        '''CREATE TABLE IF NOT EXISTS pressure_data (id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, pressure REAL NOT NULL)''',
        '''CREATE TABLE IF NOT EXISTS irradiance_data (id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, irradiance REAL NOT NULL)''',
        '''CREATE TABLE IF NOT EXISTS humidity_data (id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, humidity REAL NOT NULL)''',
        '''CREATE TABLE IF NOT EXISTS garage_data (id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, garage REAL NOT NULL)''',
        '''CREATE TABLE IF NOT EXISTS bathroom_data (id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, bathroom REAL NOT NULL)''',
        '''CREATE TABLE IF NOT EXISTS bedroom_data (id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, bedroom REAL NOT NULL)''',
        '''CREATE TABLE IF NOT EXISTS lr_data (id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, lr REAL NOT NULL)''',
        '''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, event TEXT NOT NULL, timestamp TEXT NOT NULL, description TEXT NOT NULL)'''
    ]
    for query in table_creation_queries:
        cursor.execute(query)
    conn.commit()

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
  
  write_to_holding_register(client, sensor_registers['Humidity'],               humidity)
  write_to_holding_register(client, sensor_registers['Temperature'],            temperature)
  write_to_holding_register(client, sensor_registers['SunRadiation'],           irradiance)
  write_to_holding_register(client, sensor_registers['Pressure'],               pressure)
  write_to_holding_register(client, sensor_registers['Motion_Sensor_Garage'],   garage)
  write_to_holding_register(client, sensor_registers['Motion_Sensor_Bathroom'], bathroom)
  write_to_holding_register(client, sensor_registers['Motion_Sensor_Bedroom'],  bedroom)
  write_to_holding_register(client, sensor_registers['Motion_Sensor_LR'],       lr)

  read_and_save_data()

  coils = read_from_coils(client, 0, 12)
  addLog(coils, timestamp)

def write_to_holding_register(client, register_address, value):
  client.write_register(register_address, int(value))

def read_from_holding_register(client, register_address, count=1):
  # Read 'count' number of holding registers starting from 'register_address'
  result = client.read_holding_registers(register_address, count)
  
  if not result.isError():
    return result.registers
  else:
    print("Error reading holding registers:", result)
    return None

def read_from_coils(client, coil_address, count=1):
  # Read 'count' number of coils starting from 'coil_address'
  result = client.read_coils(coil_address, count)
  
  if not result.isError():
    return result.bits
  else:
    print("Error reading coils:", result)
    return None

def read_and_save_data():
  # Create tables if they do not exist
  createTables()

  # Get current timestamp
  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  # Define sensor register mappings
  sensors = {
    "temperature_data": ("Temperature", sensor_registers['Temperature']),
    "pressure_data": ("Pressure", sensor_registers['Pressure']),
    "irradiance_data": ("SunRadiation", sensor_registers['SunRadiation']),
    "humidity_data": ("Humidity", sensor_registers['Humidity']),
    "garage_data": ("Motion_Sensor_Garage", sensor_registers['Motion_Sensor_Garage']),
    "bathroom_data": ("Motion_Sensor_Bathroom", sensor_registers['Motion_Sensor_Bathroom']),
    "bedroom_data": ("Motion_Sensor_Bedroom", sensor_registers['Motion_Sensor_Bedroom']),
    "lr_data": ("Motion_Sensor_LR", sensor_registers['Motion_Sensor_LR']),
  }

  # Prepare the data for batch insert
  data_to_insert = []

  for table, (sensor_name, register) in sensors.items():
    sensor_value = read_from_holding_register(client, register)
    if sensor_value is not None:
      data_to_insert.append((table, timestamp, sensor_value[0]))

  # Insert data (batch insert for all sensors)
  if data_to_insert:
    # Insert the data into each table
    for table, timestamp, value in data_to_insert:
      insert_data(table, [(timestamp, value)])

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

        # Registers
        write_to_holding_register(client, sensor_registers['Humidity'],               values_at_index[0])
        write_to_holding_register(client, sensor_registers['Temperature'],            values_at_index[1])
        write_to_holding_register(client, sensor_registers['SunRadiation'],           values_at_index[2])
        write_to_holding_register(client, sensor_registers['Pressure'],               values_at_index[3])
        write_to_holding_register(client, sensor_registers['Motion_Sensor_Garage'],   values_at_index[4])
        write_to_holding_register(client, sensor_registers['Motion_Sensor_Bathroom'], values_at_index[5])
        write_to_holding_register(client, sensor_registers['Motion_Sensor_Bedroom'],  values_at_index[6])
        write_to_holding_register(client, sensor_registers['Motion_Sensor_LR'],       values_at_index[7])

        # Database
        read_and_save_data()

        coils = read_from_coils(client, 0, 12)
        addLog(coils, timestamp)

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
  client = ModbusTcpClient('100.108.218.111', port=502)
  sensor_registers = {
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
cursor.close()
conn.close()
