const historyModel = require('../models/historyModel');

//get history
exports.getHistories = async (request, h) => {
  try {
    const { id } = request.params;

    const [rows] = await historyModel.getHistory(id);

    if (!rows || rows.length === 0) {
      return h.response({ message: 'history not found' }).code(404);
    }
    return h.response(rows[0]).code(200);
  } catch (error) {
    console.log('error in taking history', error);
    return h.response({ error: error.message }).code(500);
  }
};

//delete history
exports.deleteHistory = async (request, h) => {
  try {
    const result = await historyModel.deleteHistory(request.params.id);
    if (result[0].affectedRows === 0) {
      return h.response({ message: 'history not found' }).code(404);
    }
    return h.response({ message: 'history delete successfully' }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
};
