const db = require('../config/db');

const getHistory = (id) => db.query('SELECT * FROM user_data WHERE id_user_data = ?', [id]);

const deleteHistory = (id) => db.query('DELETE FROM user_data WHERE id_user_data = ?', [id]);

module.exports = { getHistory, deleteHistory };
