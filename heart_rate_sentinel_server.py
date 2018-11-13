"""
    REQUIREMENT:

    remember to validate user inputs that come from (request.get_json())
    to ensure the right fields exist in the data and that they are
    the right type

    You can write independent, testable validate_heart_rate_request(r)
    functions. You do not have to test the flask handler functions directly
    (the functions associated with the @app.route decorator), but all other
    functions should be tested.
"""

from flask import Flask, jsonify, request

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
    # todo: use mongoDB to store the patient info


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


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    """
    should return whether this patient is currently tachycardic based on
    the previously available heart rate, and should also return the timestamp
    of the most recent heart rate.

    :param patient_id:
    :return:
    """
    # todo: is_tachycardic(patient_id) return True/False
    data = {
        "status": "Yes",
        "timestamp": "the most recent one"
    }
    return jsonify(data)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rate(patient_id):
    """
    should return all the previous heart rate measurements for that patient

    :param patient_id:
    :return:
    """


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_heart_rate_average(patient_id):
    """
    should return the patients's average heart rate over all measurements
    you have stored for this user.

    :param patient_id:
    :return:
    """


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_heart_rate_interval_average():
    """
    {
        "patient_id": "1",
        "heart_rate_average_since": "2018-03-09 11:00:36.372339" // date string
    }

    :return:
    """