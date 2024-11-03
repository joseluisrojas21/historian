import express from 'express';
import cors from 'cors';
import Database from 'better-sqlite3';

const app = express();
app.use(cors()); // Enable CORS for all routes

const db = new Database('./database/testDB.db');

app.get('/temperature', (req, res) => {
  const data = db.prepare('SELECT timestamp, temperature FROM temperature_data').all();
  res.json(data);
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
