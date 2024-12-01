const Hapi = require('@hapi/hapi');
const userRoutes = require('./routes/userRoutes');
const routes = require('./routes/userRoutes');
const reminderRoutes = require('./routes/reminderRoutes');

const init = async () => {
  const server = Hapi.Server({
    port: 5000,
    host: 'localhost',
    routes: {
      cors: true,
    },
  });

  server.route(userRoutes);
  server.route(reminderRoutes);

  await server.start();
  console.log(`Server is running on ${server.info.uri}`);
};

process.on('unhandledRejection', (err) => {
  console.log(err);
  process.exit(1);
});

init();
