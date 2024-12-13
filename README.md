# CLoud Computing Project - Creating APIs 🚀

in this project cloud computing created an API to support the frontend in creating applications and implementing Machine Learning such as predicting skin type and condition, we used visual studio code to create the code and after completion we tested the API in postman, after all the APIs were running well , we deployed it to one of the Google Cloud Platform services, namely Compute Engine, and for our application database we used Cloud SQL

## Requirements📋
The project uses the following libraries and dependensi:
- `hapi`
- `jwt`
- `bcrypt`
- `dotenv`
- `mysql2, mysql-connector`
- `nademod`
- `node js`
- `python`
- `flask`
- `tensorflow`
- `numpy`

The tool used
- `visual studio code`
- `github`
- `postman`
- `Google CLoud Service`

all of this is used to build servers and APIs


## Endpoint🌐
- http://34.101.62.223:5000 for login, register, reminder, history feature
- http://34.101.62.223:6000 for predict the model

### User-API
- GET-User
	- URL: http://34.101.62.223:5000/users
	- Method: GET
```
//response
[
    {
        "id_user": 1,
        "email": "kadek@example.com",
        "username": "kadek",
        "password": "$2b$10$ZsNTX2RO/dvj6CrkxEkh9eQFv86F1QrGTHyJ5lg/VN7pN0CnUCzpG"
    },
    {
        "id_user": 3,
        "email": "made@example.com",
        "username": "made",
        "password": "$2b$10$O/OK7cZwGbWJMlDYZZ0nYe9d0ZLHldBI1gVLBmLqMO9.w5c7oq9Sm"
    },
    {
        "id_user": 4,
        "email": "test@example.com",
        "username": "Test",
        "password": "$2b$10$VhNREccXjmdJ5ExfHiT3s.ogFb1zx5CTwfa4ywg9.SXXLrh5GAE3G"
    }
]
```

- GET-userBy-id
	- URL: http://34.101.62.223:5000/users/{id}
	- Method: GET
```
//response
{
    "id_user": 1,
    "email": "kadek@example.com",
    "username": "kadek",
    "password": "$2b$10$ZsNTX2RO/dvj6CrkxEkh9eQFv86F1QrGTHyJ5lg/VN7pN0CnUCzpG"
}
```

- POST-new-user
	- URL: http://34.101.62.223:5000/users
	- Method: POST
```
//request body
{
  "username": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```
```
//response
{
    "id": 5,
    "username": "John Doe",
    "email": "john@example.com",
    "password": "$2b$10$gByJj9siEFXVShSEUNDtvuEYJn/WVBmxsvMnKs2Y/oz1fpuiBSUpO"
}
```

- PUT-edit-user
	- URL: http://34.101.62.223:5000/users/{id}
	- Method: PUT
```
//response body
{
  "username": "tester",
  "email": "tester@example.com",
}
```
```
//response
{
    "message": "user update successfully"
}
```
- PUT-edit-password
	- URL: http://34.101.62.223:5000/users/{id}/password
	- Method: PUT
```
//response body
{
  "password": "tester123"
}
```
```
//response
{
    "message": "password update successfully"
}
```

- DEL-user
	- URL: http://34.101.62.223:5000/users/{id}
	- Method: DELETE
```
{
    "message": "user delete successfully"
}
```

- Login-user
	- URL: http://34.101.62.223:5000/login
	- Method: POST
```
//request body
{
  "email": "test@example.com",
  "password": "test123"
}
```
```
//response
{
    "message": "login successfully",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiaWF0IjoxNzMzODIyMzM3LCJleHAiOjE3MzM4MjU5Mzd9.6wmr_jfczfkNdETPo_IL4Kik4MOcP21W_cjxgX8SAFQ",
    "user": {
        "id": 4,
        "email": "test@example.com",
        "username": "Test"
    }
}
```

### Reminder-API
- GET-reminder
	- URL: http://34.101.62.223:5000/reminders
	- Method: GET
```
//response terlalu panjang tidak di include
```

- GET-reminderBy-id
	- URL: http://34.101.62.223:5000/reminders/{id}
	- Method: GET
```
//response
{
    "id_reminder": 1,
    "id_user": 1,
    "judul_reminder": "inget skincare an",
    "deskripsi": "Use moisturizer",
    "jam_reminder": "09:00:00"
}
```

- POST-new-reminder
	- URL: http://34.101.62.223:5000/reminders
	- Method: POST
```
//request body
{
  "judul_reminder": "test reminder",
  "deskripsi": "This is a test reminder.",
  "jam_reminder": "10:00:00"
}
```
```
//response
{
    "message": "reminder create successfully"
}
```

- PUT-edit-reminder
	- URL: http://34.101.62.223:5000/reminders/{id}
	- Method: PUT
```
//request body
{
  "judul_reminder": "Updated Reminder",
  "deskripsi": "Updated description for the reminder.",
  "jam_reminder": "11:00:00"
}
```
```
//response
{
    "message": "reminder update successfully"
}
```

- DEL-reminder
	- URL: http://34.101.62.223:5000/reminders/{id}
	- Method: DELETE
```
{
    "message": "reminder delete successfully"
}
```
### History-API
- GET-historyBy-id
	- URL: http://34.101.62.223:5000/history/{id}
	- Method: GET
```
//response
{
    "id_user_data": 14,
    "id_user": null,
    "skin_type": "kering",
    "skin_condition": "keriput",
    "saran_kandungan": "",
    "nama_produk": "Zelens Youth Concentrate Supreme Age-Defying Serum (30ml)",
    "link_produk": "https://www.lookfantastic.com/zelens-youth-concentrate-supreme-age-defying-serum-30ml/11097958.html"
}
```

- DEL-history
	- URL: http://34.101.62.223:5000/history/{id}
	- Method: DELETE
```
//response
{
    "message": "history delete successfully"
}
```

### Predict-API
- predict gambar
  	- URL: http://34.101.62.223:6000/predict
  	- Method: POST
```
//response
{
    "recommendation": [
        {
            "saran_kandungan": "Niacinamide, retinol, clay mask"
        },
        {
            "gambar_produk": "https://www.lookfantastic.com/images?url=https://static.thcdn.com/productimg/original/11434755-2124929883353345.jpg&format=webp&auto=avif&width=985&height=985&fit=cover",
            "link_produk": "https://www.lookfantastic.com/la-roche-posay-effaclar-clay-mask-100ml/11434755.html",
            "nama_produk": "La Roche-Posay Effaclar Clay Mask 100ml"
        },
        {
            "gambar_produk": "https://www.lookfantastic.com/images?url=https://static.thcdn.com/productimg/original/11247489-8064918723776630.jpg&format=webp&auto=avif&width=985&height=985&fit=cover",
            "link_produk": "https://www.lookfantastic.com/elizabeth-arden-skin-illuminating-advanced-brightening-night-capsules-50-capsules/11247489.html",
            "nama_produk": "Elizabeth Arden Skin Illuminating Advanced Brightening Night Capsules (50 Capsules)"
        },
        {
            "gambar_produk": "https://www.lookfantastic.com/images?url=https://static.thcdn.com/productimg/original/11097958-1504896380665305.jpg&format=webp&auto=avif&width=985&height=985&fit=cover",
            "link_produk": "https://www.lookfantastic.com/dermalogica-age-bright-clearing-serum-30ml/12134833.html",
            "nama_produk": "Dermalogica AGE Bright Clearing Serum 30ml"
        },
        {
            "gambar_produk": "https://www.lookfantastic.com/images?url=https://static.thcdn.com/productimg/original/11540506-1374897169744244.jpg&format=webp&auto=avif&width=985&height=985&fit=cover",
            "link_produk": "https://www.lookfantastic.com/dr-dennis-gross-skincare-c-collagen-brighten-and-firm-vitamin-c-serum-30ml/11540506.html",
            "nama_produk": "Dr Dennis Gross Skincare C+Collagen Brighten and Firm Vitamin C Serum 30ml"
        },
        {
            "gambar_produk": "https://www.lookfantastic.com/images?url=https://static.thcdn.com/productimg/original/11925166-7314945662583233.jpg&format=webp&auto=avif&width=985&height=985&fit=cover",
            "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html",
            "nama_produk": "Murad Retinol Youth Renewal Serum Travel Size"
        },
        {
            "gambar_produk": "https://www.lookfantastic.com/images?url=https://static.thcdn.com/productimg/original/11097958-1504896380665305.jpg&format=webp&auto=avif&width=985&height=985&fit=cover",
            "link_produk": "https://www.lookfantastic.com/zelens-youth-concentrate-supreme-age-defying-serum-30ml/11097958.html",
            "nama_produk": "Zelens Youth Concentrate Supreme Age-Defying Serum (30ml)"
        },
        {
            "gambar_produk": "https://www.lookfantastic.com/images?url=https://static.thcdn.com/productimg/original/12040130-1374969285198860.jpg&format=webp&auto=avif&width=985&height=985&fit=cover",
            "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html",
            "nama_produk": "PIXI Collagen and Retinol Serum 30ml"
        }
    ],
    "skin_condition": "large_pores",
    "skin_type": "oily",
    "status": "success"
}
```
