#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Jason L

from flask import Flask, jsonify, request
from datetime import datetime
# from database_mongodb import Patient, connect_to_mongodb
from pymodm import connect, MongoModel, fields
import toolbox_jason as jtb
from sendEmail import send_notification_email

url = "mongodb://void001:goduke18@ds159993.mlab.com:59993/bme590"
connect(url)
app = Flask(__name__)


class Patient(MongoModel):
    """
    Data Class used by MongoDB
    """

    patient_id = fields.BigIntegerField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.IntegerField()
    last_heart_rate = fields.IntegerField()
    last_timestamp = fields.DateTimeField()
    heart_rates = fields.ListField()
    timestamps = fields.ListField()


@app.route("/api/new_patient", methods=["POST"])
def post_new_patient():
    """
    This will be called when the heart rate monitor is checked out to be
    attached to a particular patient, the system emits this event to register
    the patient with your heart rate server. This will allow you to initialize
    a patient, and accept future heart rate measurements for this patient.

    expected request data: POST /api/new_patient with
    {
        "patient_id": "1", # usually this would be the patient MRN
        "attending_email": "suyash.kumar@duke.edu",
        "user_age": 50, # in years
    }

    :return: 400 if data entry is not valid, 200 if data is successfully saved
    """
    r = request.get_json()
    entry_to_check = {'patient_id': 1,
                      'attending_email': 'emailstr',
                      'user_age': 100}
    try:
        jtb.validate_json_data_entry(r, entry_to_check)
    except ValueError or TypeError as err:
        print(err)
        return 400
    else:
        p = Patient(r['patient_id'],
                    attendint_email=r['attending_email'],
                    user_age=r['user_age'])
        p.save()
        return 200


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    """
    which should store this heart rate measurement for the user with
    that id, as well as a time stamp.

    Expected request data: POST /api/heart_rate with
    {
        "patient_id": "1", # usually this would be the patient MRN
        "heart_rate": 100
    }

    :return: 400 if data entry is not valid, 200 if data is successfully saved
    """
    r = request.get_json()
    entry_to_check = {'patient_id': 1, 'heart_rate': 60}
    try:
        jtb.validate_json_data_entry(r, entry_to_check)
    except ValueError or TypeError as err:
        print(err)
        return 400
    else:
        p = Patient.objects.raw({"_id": r['patient_id']}).first()
        if "Tachycardia" is jtb.validate_heart_rate_request(p.user_age,
                                                            r['heart_rate']):
            date_string = p.last_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
            send_notification_email(p.attending_email,
                                    p.last_heart_rate,
                                    date_string)

        p.last_heart_rate = r['heart_rate']
        p.heart_rates.append(p.last_heart_rate)
        p.last_timestamp = datetime.now()
        p.timestamps.append(p.last_timestamp)

        p.save
        return 200


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    """
    should return whether this patient is currently tachycardic based on
    the previously available heart rate, and should also return the timestamp
    of the most recent heart rate.

    :param patient_id: request patient id
    :return: json data contains: "status" and "timestamp"
    """
    p = Patient.objects.raw({"_id": patient_id}).first()
    status = jtb.validate_heart_rate_request(p.user_age, p.last_heart_rate)
    try:
        timestamp_str = p.last_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
    except TypeError as err:
        raise err("the timestamp has not expected type")

    data = {
        "status": status,
        "timestamp": timestamp_str
    }
    return jsonify(data)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rates(patient_id):
    """
    should return all the previous heart rate measurements for that patient.

    :param patient_id:
    :return: json data contains "heart_rates"
    """
    p = Patient.objects.raw({"_id": patient_id}).first()
    data = {
        "heart_rates": p.heart_rates
    }
    return jsonify(data)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_heart_rate_average(patient_id):
    """
    should return the patients's average heart rate over all measurements
    have stored for this user.

    :param patient_id: request patient_id
    :return: json data contains "heart_rate_average"
    """
    p = Patient.objects.raw({"_id": patient_id}).first()
    heart_rate_avg = jtb.average_heart_rate(p.heart_rates)
    data = {
        "heart_rate_average": heart_rate_avg
    }
    return jsonify(data)


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_heart_rate_interval_average():
    """
    should return the patients's average heart rate since the post time

    expected request data: POST /api/heart_rate/interval_average with
    {
        "patient_id": "1",
        "heart_rate_average_since": "2018-03-09 11:00:36.372339" // date string
    }

    :return: 400 if data entry is not valid, json data contains
        "heart_rate_interval_average" if data entry is valid
    """
    r = request.get_json()
    entry_to_check = {'patient_id': 1,
                      'heart_rate_average_since': "2018-03-09 11:00:36.372339"}
    try:
        jtb.validate_json_data_entry(r, entry_to_check)
    except ValueError or TypeError as err:
        print(err)
        return 400
    else:
        p = Patient.objects.raw({"_id": r['patient_id']}).first()
        heart_rates = [p.heart_rates[x] for x, y in enumerate(p.timestamps)
                       if y > datetime.strptime(r['heart_rate_average_since'],
                                                '%Y-%m-%d %H:%M:%S.%f')]
        data = {
            'heart_rate_interval_average': jtb.average_heart_rate(heart_rates)
        }
        return jsonify(data)


if __name__ == '__main__':
    app.run()
