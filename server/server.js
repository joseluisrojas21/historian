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

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
