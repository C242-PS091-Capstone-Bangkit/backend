const reminderController = require('../controllers/reminderController');

const reminderRoutes = [
  { method: 'POST', path: '/reminders', handler: reminderController.createReminder },
  { method: 'GET', path: '/reminders', handler: reminderController.getAllReminder },
  { method: 'GET', path: '/reminders/{id}', handler: reminderController.getReminderById },
  { method: 'PUT', path: '/reminders/{id}', handler: reminderController.updateReminder },
  { method: 'DELETE', path: '/reminders/{id}', handler: reminderController.deleteReminder },
];

module.exports = reminderRoutes;
