const db = require('../config/db');

const getAllUsers = () => db.query('SELECT * FROM user');
const getUsersById = (id) => db.query('SELECT * FROM user WHERE id_user = ?', [id]);
const createUser = (user) => {
  const { email, username, password } = user;
  const query = 'INSERT INTO user (email, username, password) VALUES (?, ?, ?)';

  return db.query(query, [email, username, password]);
};
const updateUser = (user, id) => db.query('UPDATE user SET email = ?, username = ? WHERE id_user = ?', [user.email, user.username, id]);
const updateUserPassword = (user, id) => db.query('UPDATE user SET password = ? WHERE id_user = ?', [user.password, id]);
const deleteUser = (id) => db.query('DELETE FROM user WHERE id_user = ?', [id]);
const getUsersByEmail = (email) => {
  const query = 'SELECT * FROM user WHERE email = ?';
  return db.query(query, [email]).then(([rows]) => rows[0]);
};

module.exports = { getAllUsers, getUsersById, createUser, updateUser, updateUserPassword, deleteUser, getUsersByEmail };
