const { options } = require('@hapi/joi/lib/base');
const userController = require('../controllers/userController');

const routes = [
  { method: 'GET', path: '/users', handler: userController.getAllUsers },
  { method: 'GET', path: '/users/{id}', handler: userController.getUsersById },
  { method: 'POST', path: '/users', handler: userController.createUser },
  {
    method: 'PUT',
    path: '/users/{id}',
    options: {
      pre: [userController.verifyToken],
    },
    handler: userController.updateUser,
  },
  { method: 'DELETE', path: '/users/{id}', handler: userController.deleteUser },
  { method: 'POST', path: '/login', handler: userController.login },
];

module.exports = routes;
