const historyController = require('../controllers/historyController');

const historyRoutes = [
  { method: 'GET', path: '/history/{id}', handler: historyController.getHistories },
  { method: 'DELETE', path: '/history/{id}', handler: historyController.deleteHistory },
];

module.exports = historyRoutes;
