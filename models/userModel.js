const db = require('../config/db');

const getAllUsers = () => db.query('SELECT * FROM users');
const getUsersById = (id) => db.query('SELECT * FROM users WHERE id = ?', [id]);
const createUser = (user) => {
  const { email, password, nama } = user;
  const query = 'INSERT INTO users (email, password, nama) VALUES (?, ?, ?)';

  return db.query(query, [email, password, nama]);
};
const updateUser = (user, id) => db.query('UPDATE users SET nama = ?, email = ?, password = ? WHERE id = ?', [user.nama, user.email, user.password, id]);
const deleteUser = (id) => db.query('DELETE FROM users WHERE id = ?', [id]);
const getUsersByEmail = (email) => {
  const query = 'SELECT * FROM users WHERE email = ?';
  return db.query(query, [email]).then(([rows]) => rows[0]);
};

module.exports = { getAllUsers, getUsersById, createUser, updateUser, deleteUser, getUsersByEmail };
