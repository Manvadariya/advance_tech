# import necessary moduls for online line database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# add database url and secret key
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://faceattendance-c7b33-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

# add student data
data = {
    "1":
        {
            "name": "Man Vadariya",
            "branch": "CE",
            "starting_year": 2023,
            "total_attendance": 0,
            "class": "B",
            "year": 1,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
    "2":
        {
            "name": "Zeel Javia",
            "branch": "CE",
            "starting_year": 2023,
            "total_attendance": 0,
            "class": "B",
            "year": 1,
            "last_attendance_time": "2023-12-15 00:05:34"
        },
    "3":
        {
            "name": "Krish Sojitra",
            "branch": "EC",
            "starting_year": 2023,
            "total_attendance": 0,
            "class": "C",
            "year": 1,
            "last_attendance_time": "2023-10-29 10:54:34"
        },
    "4":
        {
            "name": "Florence Barvaliya",
            "branch": "CH",
            "starting_year": 2023,
            "total_attendance": 0,
            "class": "G",
            "year": 1,
            "last_attendance_time": "2023-09-10 09:24:34"
        },
    "5":
        {
            "name": "Kirtan Domadiya",
            "branch": "EC",
            "starting_year": 2023,
            "total_attendance": 0,
            "class": "C",
            "year": 1,
            "last_attendance_time": "2023-12-11 08:25:54"
        },

}
