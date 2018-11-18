"""
Your Flask web service should implement the following API routes:

POST /api/new_patient with
{
    "patient_id": "1", # usually this would be the patient MRN
    "attending_email": "suyash.kumar@duke.edu",
    "user_age": 50, # in years
}
This will be called when the heart rate monitor is checked out to be attached to a particular patient, the system emits this event to register the patient with your heart rate server. This will allow you to initialize a patient, and accecpt future heart rate measurements for this patient.
POST /api/heart_rate with
{
    "patient_id": "1", # usually this would be the patient MRN
    "heart_rate": 100
}
which should store this heart rate measurement for the user with that email. Be sure to include the current time stamp in your database or your program cache.
GET /api/status/<patient_id> should return whether this patient is currently tachycardic based on the previously available heart rate, and should also return the timestamp of the most recent heart rate.
GET /api/heart_rate/<patient_id> should return all the previous heart rate measurements for that patient
GET /api/heart_rate/average/<patient_id> should return the patients's average heart rate over all measurements you have stored for this user.
POST /api/heart_rate/interval_average with
{
    "patient_id": "1",
    "heart_rate_average_since": "2018-03-09 11:00:36.372339" // date string
}
"""

import sys


def main():
    import requests

    requests.post("http://127.0.0.1:5000/api/new_patient", json={
        "patient_id": 7,
        "attending_email": "user1@email.com",
        "user_age": 100
    })

    r_heart_rate = requests.post("http://127.0.0.1:5000/api/heart_rate", json={
        "patient_id": 7,  # usually this would be the patient MRN
        "heart_rate": 100
    })
    status = r_heart_rate
    print(status)

    r_heart_rate_avg_since = requests.post("http://127.0.0.1:5000/api/heart_rate/interval_average", json={
        "patient_id": 7,
        "heart_rate_average_since": "2018-03-09 11:00:36.372339"
    })
    data = r_heart_rate_avg_since.json()
    print(data)

    r_status = requests.get("http://127.0.0.1:5000/api/status/7")
    status = r_status.json()
    print(status)

    r_heart_rate = requests.get("http://127.0.0.1:5000/api/heart_rate/7")
    data = r_heart_rate.json()
    print(data)

    r_heart_rate_avg = requests.get("http://127.0.0.1:5000/api/heart_rate/average/7")
    data = r_heart_rate_avg.json()
    print(data)


if __name__ == '__main__':
    sys.exit(main())


