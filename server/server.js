import express from 'express';
import Database from 'better-sqlite3'; // Ensure you're using the correct import for your DB
import cors from 'cors';

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize database
const db = new Database('./database/testDB.db');

// Route to fetch irradiance data
app.get('/irradiance', (req, res) => {
  try {
    const data = db.prepare('SELECT timestamp, irradiance FROM irradiance_data').all();
    console.log(data);
    res.json(data);
  } catch (error) {
    console.error('Error fetching irradiance data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Route to fetch pressure data
app.get('/pressure', (req, res) => {
  try {
    const data = db.prepare('SELECT timestamp, pressure FROM pressure_data').all();
    console.log(data);
    res.json(data);
  } catch (error) {
    console.error('Error fetching pressure data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Route to fetch temperature data
app.get('/temperature', (req, res) => {
  try {
    const data = db.prepare('SELECT timestamp, temperature FROM temperature_data').all();
    console.log(data);
    res.json(data);
  } catch (error) {
    console.error('Error fetching temperature data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Route to fetch humidity data
app.get('/humidity', (req, res) => {
  try {
    const data = db.prepare('SELECT timestamp, humidity FROM humidity_data').all();
    console.log(data);
    res.json(data);
  } catch (error) {
    console.error('Error fetching humidity data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Route to fetch garage data
app.get('/garage', (req, res) => {
  try {
    const data = db.prepare('SELECT timestamp, garage FROM garage_data').all();
    console.log(data);
    res.json(data);
  } catch (error) {
    console.error('Error fetching garage data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Route to fetch bathroom data
app.get('/bathroom', (req, res) => {
  try {
    const data = db.prepare('SELECT timestamp, bathroom FROM bathroom_data').all();
    console.log(data);
    res.json(data);
  } catch (error) {
    console.error('Error fetching bathroom data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Route to fetch bedroom data
app.get('/bedroom', (req, res) => {
  try {
    const data = db.prepare('SELECT timestamp, bedroom FROM bedroom_data').all();
    console.log(data);
    res.json(data);
  } catch (error) {
    console.error('Error fetching bedroom data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Route to fetch lr data
app.get('/lr', (req, res) => {
  try {
    const data = db.prepare('SELECT timestamp, lr FROM lr_data').all();
    console.log(data);
    res.json(data);
  } catch (error) {
    console.error('Error fetching lr data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
