## Endpoint
http://34.101.62.223:5000, 
http://34.101.62.223:6000
#### User-API
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
	- URL: http://34.101.62.223:5000/users/1
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
	- URL: http://34.101.62.223:5000/users/1
	- Method: PUT
```
//response body
{
  "username": "tester",
  "email": "tester@example.com",
  "password": "tester123"
}
```
```
//response
{
    "message": "user update successfully"
}
```

- DEL-user
	- URL: http://34.101.62.223:5000/users/5
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

#### Reminder-API
- GET-reminder
	- URL: http://34.101.62.223:5000/reminder
	- Method: GET
```
//response terlalu panjang tidak di include
```

- GET-reminderBy-id
	- URL: http://34.101.62.223:5000/reminder/1
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
	- URL: http://34.101.62.223:5000/reminder
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
	- URL: http://34.101.62.223:5000/reminder/2
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
	- URL: http://34.101.62.223:5000/reminder/2
	- Method: DELETE
```
{
    "message": "reminder delete successfully"
}
```
#### History-API
- GET-historyBy-id
	- URL: http://34.101.62.223:5000/history/14
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
	- URL: http://34.101.62.223:5000/history/16
	- Method: DELETE
```
//response
{
    "message": "history delete successfully"
}
```

- predict gambar
  	- URL: http://34.101.62.223:6000/predict
  	- Method: POST
```
//response
{
    "recommendation": [
        {
            "saran_kandungan": "Hyaluronic acid, niacinamide, retinol (mulailah dengan konsentrasi rendah)"
        },
        {
            "link_produk": "https://www.lookfantastic.com/la-roche-posay-toleriane-sensitive-fluid-moisturiser-40ml/11855110.html",
            "nama_produk": "La Roche-Posay Toleriane Sensitive Fluid Moisturiser 40ml"
        },
        {
            "link_produk": "https://www.lookfantastic.com/fade-out-advanced-age-protection-even-skin-tone-day-cream-spf-25-50ml/11490811.html",
            "nama_produk": "Fade Out ADVANCED + Age Protection Even Skin Tone Day Cream SPF 25 50ml"
        },
        {
            "link_produk": "https://www.lookfantastic.com/bioderma-hydrabio-gel-cream-40ml/11688484.html",
            "nama_produk": "Bioderma Hydrabio Gel Cream 40ml"
        },
        {
            "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html",
            "nama_produk": "PIXI Collagen and Retinol Serum 30ml"
        },
        {
            "link_produk": "https://www.lookfantastic.com/nip-fab-retinol-fix-serum-extreme-50ml/12192674.html",
            "nama_produk": "NIP+FAB Retinol Fix Serum Extreme 50ml"
        },
        {
            "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html",
            "nama_produk": "Murad Retinol Youth Renewal Serum Travel Size"
        }
    ],
    "skin_condition": "large_pores",
    "skin_type": "dry",
    "status": "success"
}
```
