const db = require('../config/db');

const getAllReminders = () => db.query('SELECT * FROM reminder ORDER BY jam_reminder ASC');
const getReminderById = (id) => db.query('SELECT * FROM reminder WHERE id_reminder = ?', [id]);
const createReminder = (reminder) => {
  const { id_user, judul_reminder, deskripsi, jam_reminder } = reminder;
  const query = 'INSERT INTO reminder (id_user, judul_reminder, deskripsi, jam_reminder) VALUES (?, ?, ?, ?)';

  return db.query(query, [id_user, judul_reminder, deskripsi, jam_reminder]);
};
const updateReminder = (reminder, id) => db.query('UPDATE reminder SET judul_reminder = ?, deskripsi = ?, jam_reminder = ? WHERE id_reminder = ?', [reminder.judul_reminder, reminder.deskripsi, reminder.jam_reminder, id]);
const deleteReminder = (id) => db.query('DELETE FROM reminder WHERE id_reminder = ?', [id]);

module.exports = { getAllReminders, getReminderById, createReminder, updateReminder, deleteReminder };
