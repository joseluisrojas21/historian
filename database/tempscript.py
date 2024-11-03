import sqlite3
import random
import time
from datetime import datetime

# Connect to the SQLite database
db_file = 'testDB.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to add random temperature data
def add_random_temperature_data():
  # Generate a random temperature between 15 and 30 degrees Celsius
  temperature = round(random.uniform(15.00, 30.00), 2)

  # Current date and time
  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  sql = '''INSERT INTO temperature_data (timestamp, temperature) VALUES (?, ?)'''

  # Execute the SQL command
  cursor.execute(sql, (timestamp, temperature))

  # Commit the changes
  conn.commit()
  print(f"Added temperature data: {timestamp} - {temperature}°C")

# Function to add random pressure data
def add_random_pressure_data():
  # Generate a random pressure between 950 and 1050 hPa
  pressure = round(random.uniform(950.00, 1050.00), 2)

  # Current date and time
  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  sql = '''INSERT INTO pressure_data (timestamp, pressure) VALUES (?, ?)'''

  # Execute the SQL command
  cursor.execute(sql, (timestamp, pressure))

  # Commit the changes
  conn.commit()
  print(f"Added pressure data: {timestamp} - {pressure} hPa")

# Function to add random irradiance data
def add_random_irradiance_data():
  # Generate a random irradiance between 0 and 1000 W/m²
  irradiance = round(random.uniform(0, 1000), 2)

  # Current date and time
  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  sql = '''INSERT INTO irradiance_data (timestamp, irradiance) VALUES (?, ?)'''

  # Execute the SQL command
  cursor.execute(sql, (timestamp, irradiance))

  # Commit the changes
  conn.commit()
  print(f"Added irradiance data: {timestamp} - {irradiance} W/m²")

if __name__ == "__main__":
  while True:
    add_random_temperature_data()
    add_random_pressure_data()
    add_random_irradiance_data()  # Add irradiance data
    time.sleep(10)  # Wait for 10 seconds before the next entry

# Close the database connection
cursor.close()
conn.close()
