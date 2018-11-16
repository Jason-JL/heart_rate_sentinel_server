from pymodm import connect
from pymodm import MongoModel, fields


def connect_to_mongodb():
    """
    a wrapper function used to connect to MongoDB
    :return:
    """
    from pymodm import connect

    url = "mongodb://void001:goduke18@ds159993.mlab.com:59993/bme590"
    connect(url)


class Patient(MongoModel):
    """
    Data Class used by MongoDB
    """
    from pymodm import fields

    patient_id = fields.BigIntegerField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.IntegerField()
    last_heart_rate = fields.IntegerField()
    last_timestamp = fields.DateTimeField()
    heart_rates = fields.ListField()
    timestamps = fields.ListField()