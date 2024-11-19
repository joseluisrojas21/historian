import express from 'express';
import Database from 'better-sqlite3';
import cors from 'cors';

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize database
const db = new Database('./database/testDB.db');

// Route to fetch all data
app.get('/allData', (req, res) => {
  try {
    const temperatureData = db.prepare('SELECT timestamp, temperature FROM temperature_data').all();
    const pressureData    = db.prepare('SELECT timestamp, pressure FROM pressure_data').all();
    const irradianceData  = db.prepare('SELECT timestamp, irradiance FROM irradiance_data').all();
    const humidityData    = db.prepare('SELECT timestamp, humidity FROM humidity_data').all();
    const garageData      = db.prepare('SELECT timestamp, garage FROM garage_data').all();
    const bathroomData    = db.prepare('SELECT timestamp, bathroom FROM bathroom_data').all();
    const bedroomData     = db.prepare('SELECT timestamp, bedroom FROM bedroom_data').all();
    const lrData          = db.prepare('SELECT timestamp, lr FROM lr_data').all();

    res.json({
      temperatureData,
      pressureData,
      irradianceData,
      humidityData,
      garageData,
      bathroomData,
      bedroomData,
      lrData
    });
  } catch (error) {
    console.error('Error fetching all data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/allLogs', (req, res) => {
  try {
    const logs = db.prepare('SELECT timestamp, event, description FROM logs').all();

    res.json({
      logs
    });
  } catch (error) {
    console.error('Error fetching logs:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/deleteAllData', (req, res) => {
  try {
    db.prepare('DELETE FROM temperature_data').run();
    db.prepare('DELETE FROM pressure_data').run();
    db.prepare('DELETE FROM irradiance_data').run();
    db.prepare('DELETE FROM humidity_data').run();
    db.prepare('DELETE FROM garage_data').run();
    db.prepare('DELETE FROM bathroom_data').run();
    db.prepare('DELETE FROM bedroom_data').run();
    db.prepare('DELETE FROM lr_data').run();
    db.prepare('DELETE FROM logs').run();

    res.json({ message: 'All data deleted successfully from all tables.' });
  } catch (error) {
    console.error('Error deleting all data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
