const { error } = require('@hapi/joi/lib/base');
const userModel = require('../models/userModel');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

//mendapatkan semua user
exports.getAllUsers = async (request, h) => {
  try {
    const [rows] = await userModel.getAllUsers();
    return h.response(rows).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
};

//mendapatkan user berdasarkan id
exports.getUsersById = async (request, h) => {
  try {
    const { id } = request.params;

    const [rows] = await userModel.getUsersById(id);

    if (!rows || rows.length === 0) {
      return h.response({ message: 'User not found' }).code(404);
    }
    return h.response(rows[0]).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
};

//membuat user baru
exports.createUser = async (request, h) => {
  try {
    const { password } = request.payload;

    const hashedPassword = await bcrypt.hash(password, 10);
    const userWithHashedPassword = { ...request.payload, password: hashedPassword };

    // Simpan pengguna ke database

    const result = await userModel.createUser(userWithHashedPassword);
    return h.response({ id: result[0].insertId, ...userWithHashedPassword }).code(201);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
};

//update data user
exports.updateUser = async (request, h) => {
  try {
    const { id } = request.params;
    const { nama, email, password } = request.payload;

    if (!nama || !email || !password) {
      return h.response({ error: 'All fields are required: nama, email, password' }).code(400);
    }

    const result = await userModel.updateUser({ nama, email, password }, id);

    if (result[0].affectedRows === 0) {
      return h.response({ message: 'user not found' }).code(404);
    }
    return h.response({ message: 'user update successfully' }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
};

//hapus user
exports.deleteUser = async (request, h) => {
  try {
    const result = await userModel.deleteUser(request.params.id);
    if (result[0].affectedRows === 0) {
      return h.response({ message: 'user not found' }).code(404);
    }
    return h.response({ message: 'user update successfully' }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
};

//login user
exports.login = async (request, h) => {
  try {
    const { email, password } = request.payload;
    console.log('Email:', email);
    console.log('Password:', password);

    //validasi input
    if (!email || !password) {
      return h.response({ error: 'email and password are required' }).code(400);
    }

    //cari user berdasarkan email
    const user = await userModel.getUsersByEmail(email);
    if (!user) {
      return h.response({ error: 'invalid email or password' }).code(401);
    }

    //periksa password
    const passwordValid = await bcrypt.compare(password, user.password);
    console.log('Password valid:', passwordValid);
    if (!passwordValid) {
      return h.response({ error: 'invalid email or password' }).code(401);
    }

    //buat token jwt
    const token = jwt.sign({ id: user.id, email: user.email }, process.env.JWT_SECRET, { expiresIn: '1h' });

    return h
      .response({
        message: 'login successfully',
        token,
        user: { id: user.id, email: user.email, nama: user.nama },
      })
      .code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
};
