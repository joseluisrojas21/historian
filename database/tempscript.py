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

if __name__ == "__main__":
  while True:
    add_random_temperature_data()
    time.sleep(10)  # Wait for 10 second before the next entry

# Close the database connection
cursor.close()
conn.close()