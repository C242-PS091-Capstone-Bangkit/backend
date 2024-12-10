const mysql = require('mysql2');
const dotenv = require('dotenv');

dotenv.config();

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  waitForConnections: true, // Menunggu koneksi jika pool penuh
  connectionLimit: process.env.DB_CONNECTION_LIMIT || 10, // Batas koneksi dalam pool
  queueLimit: 0, // Tidak membatasi antrean koneksi
});

module.exports = pool.promise();
