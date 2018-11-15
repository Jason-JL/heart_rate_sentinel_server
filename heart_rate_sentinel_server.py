"""
    REQUIREMENT:

    ? remember to validate user inputs that come from (request.get_json())
    to ensure the right fields exist in the data and that they are
    the right type

    ? You can write independent, testable validate_heart_rate_request(r)
    functions.

    ? how to test the functions( require a return value? )

    ? the meaning of last post function

    ? should we store the status? what value type should be use?
"""

from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
from datetime import datetime
import toolbox_jason as jtb


connect("mongodb://void001:goduke18@ds159993.mlab.com:59993/bme590")


class Patient(MongoModel):
    patient_id = fields.BigIntegerField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.IntegerField()
    last_heart_rate = fields.IntegerField()
    last_timestamp = fields.DateTimeField()
    heart_rates = fields.ListField()
    timestamps = fields.ListField()


app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def post_new_patient():
    """

    {
        "patient_id": "1", # usually this would be the patient MRN
        "attending_email": "suyash.kumar@duke.edu",
        "user_age": 50, # in years
    }

    This will be called when the heart rate monitor is checked out to be
    attached to a particular patient, the system emits this event to register
    the patient with your heart rate server. This will allow you to initialize
    a patient, and accecpt future heart rate measurements for this patient.

    :return:
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


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    """


    {
        "patient_id": "1", # usually this would be the patient MRN
        "heart_rate": 100
    }

    which should store this heart rate measurement for the user with
    that email. Be sure to include the `current time stamp` in your database
    or your program cache.

    :return:
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
            # Todo: notify the user by email
            print("Todo: notify the user by email")

        p.last_heart_rate = r['heart_rate']
        p.heart_rates.append(p.last_heart_rate)
        p.last_timestamp = datetime.now()
        p.timestamps.append(p.last_timestamp)

        p.save


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    """
    should return whether this patient is currently tachycardic based on
    the previously available heart rate, and should also return the timestamp
    of the most recent heart rate.

    :param patient_id:
    :return:
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
    should return all the previous heart rate measurements for that patient

    :param patient_id:
    :return:
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
    you have stored for this user.

    :param patient_id:
    :return:
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
    {
        "patient_id": "1",
        "heart_rate_average_since": "2018-03-09 11:00:36.372339" // date string
    }

    :return:
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
