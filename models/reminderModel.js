const db = require('../config/db');

const getAllReminders = () => db.query('SELECT * FROM reminders ORDER BY reminder_time ASC');
const getReminderById = (id) => db.query('SELECT * FROM reminders WHERE id = ?', [id]);
const createReminder = (reminder) => {
  const { user_id, title, description, reminder_time } = reminder;
  const query = 'INSERT INTO reminders (user_id, title, description, reminder_time) VALUES (?, ?, ?, ?)';

  return db.query(query, [user_id, title, description, reminder_time]);
};
const updateReminder = (reminder, id) => db.query('UPDATE reminders SET title = ?, description = ?, reminder_time = ? WHERE id = ?', [reminder.title, reminder.description, reminder.reminder_time, id]);
const deleteReminder = (id) => db.query('DELETE FROM reminders WHERE id = ?', [id]);

module.exports = { getAllReminders, getReminderById, createReminder, updateReminder, deleteReminder };
