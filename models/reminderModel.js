const db = require('../config/db');

const getAllReminders = async () => {
  const [rows] = await db.query('SELECT * FROM reminders');
  return rows;
};
const getReminderById = (id) => db.query('SELECT * FROM reminders WHERE id_reminder = ?', [id]);
const createReminder = (reminder) => {
  const { id_user, judul_reminder, deskripsi, jam_reminder } = reminder;
  const query = 'INSERT INTO reminders (id_user, judul_reminder, deskripsi, jam_reminder) VALUES (?, ?, ?, ?)';

  return db.query(query, [id_user, judul_reminder, deskripsi, jam_reminder]);
};
const updateReminder = (reminder, id) => db.query('UPDATE reminders SET judul_reminder = ?, deskripsi = ?, jam_reminder = ? WHERE id_reminder = ?', [reminder.judul_reminder, reminder.deskripsi, reminder.jam_reminder, id]);
const deleteReminder = (id) => db.query('DELETE FROM reminders WHERE id_reminder = ?', [id]);

module.exports = { getAllReminders, getReminderById, createReminder, updateReminder, deleteReminder };
