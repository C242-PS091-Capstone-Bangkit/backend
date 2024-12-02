const reminderController = require('../controllers/reminderController');

const reminderRoutes = [
  { method: 'POST', path: '/reminder', handler: reminderController.createReminder },
  { method: 'GET', path: '/reminder', handler: reminderController.getAllReminder },
  { method: 'GET', path: '/reminder/{id}', handler: reminderController.getReminderById },
  { method: 'PUT', path: '/reminder/{id}', handler: reminderController.updateReminder },
  { method: 'DELETE', path: '/reminder/{id}', handler: reminderController.deleteReminder },
];

module.exports = reminderRoutes;
