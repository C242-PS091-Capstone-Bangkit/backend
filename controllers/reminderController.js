const reminderModel = require('../models/reminderModel');

//creating reminder
exports.createReminder = async (Request, h) => {
  try {
    const { user_id, title, description, reminder_time } = Request.payload;

    const result = await reminderModel.createReminder({
      user_id,
      title,
      description,
      reminder_time,
    });

    return h.response({ id: result.insertId, message: 'reminder create successfully' }).code(201);
  } catch (error) {
    console.log('error creating reminder', error);
    return h.response({ error: error.message }).code(500);
  }
};

//get all reminder
exports.getAllReminder = async (request, h) => {
  try {
    const reminder = await reminderModel.getAllReminders();
    return h.response(reminder).code(200);
  } catch (error) {
    console.log('error in taking reminder', error);
    return h.response({ error: error.message }).code(500);
  }
};

//get reminder by id reminder
exports.getReminderById = async (request, h) => {
  try {
    const { id } = request.params;

    const [rows] = await reminderModel.getReminderById(id);

    if (!rows || rows.length === 0) {
      return h.response({ message: 'reminder not found' }).code(404);
    }
    return h.response(rows[0]).code(200);
  } catch (error) {
    console.log('error in taking reminder', error);
    return h.response({ error: error.message }).code(500);
  }
};

//update reminder
exports.updateReminder = async (request, h) => {
  try {
    const { id } = request.params;
    const { title, description, reminder_time } = request.payload;

    if (!title || !description || !reminderModel) {
      return h.response({ error: 'All fields are required: title, description, reminder_time' }).code(400);
    }

    const updatereminder = {
      title: title || undefined,
      description: description || undefined,
      reminder_time: reminder_time || undefined,
    };

    const result = await reminderModel.updateReminder(updatereminder, id);

    if (result[0].affectedRows === 0) {
      return h.response({ message: 'reminder not found' }).code(404);
    }
    return h.response({ message: 'reminder update successfully' }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
};

//delete reminder
exports.deleteReminder = async (request, h) => {
  try {
    const result = await reminderModel.deleteReminder(request.params.id);
    if (result[0].affectedRows === 0) {
      return h.response({ message: 'reminder not found' }).code(404);
    }
    return h.response({ message: 'reminder delete successfully' }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
};
