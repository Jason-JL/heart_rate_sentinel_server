import numpy as np


def validate_heart_rate_request(age, heart_rate):
    """
    determine whether there is abnormal of the heart rate

    1–2 years: Tachycardia >151 bpm
    3–4 years: Tachycardia >137 bpm
    5–7 years: Tachycardia >133 bpm
    8–11 years: Tachycardia >130 bpm
    12–15 years: Tachycardia >119 bpm
    >15 years – adult: Tachycardia >100 bpm

    :param age: the age of people, an factor in consideration of Tachycardia
    :param heart_rate: the last measured heart rate
    :return: status in the range ['Tachycardia', 'Normal', 'Undefined']
    """
    status = "Undefined"

    if age < 1:
        tachycardia_threshold = -1
    if age in range(1,3):
        tachycardia_threshold = 151
    if age in range(3,5):
        tachycardia_threshold = 137
    if age in range(5,8):
        tachycardia_threshold = 133
    if age in range(8,12):
        tachycardia_threshold = 130
    if age in range(12, 16):
        tachycardia_threshold = 119
    if age > 15:
        tachycardia_threshold = 100

    if tachycardia_threshold != -1:
        if heart_rate >= tachycardia_threshold:
            status = "Tachycardia"
        else:
            status = "Normal"

    return status


def validate_json_data_entry(request_json, entry_dict):
    """
    check if the request json data has the expected entry and the expected type

    :param request_json: json data to check
    :param entry_dict: dictionary has the format {entry:example_data}
    :return:
    """
    for entry_name, data in entry_dict.items():
        if entry_name not in request_json:
            raise ValueError("No entry in the request json data")
        if isinstance(type(entry_dict[entry_name]), type(data)):
            raise TypeError("Data Type is not as expected")
    return True


def average_heart_rate(heart_rate_list):
    """
    calc the average of heart rate

    :param heart_rate_list: list contains the measured heart rates
    :return: the average
    """
    return int(np.sum(heart_rate_list) / len(heart_rate_list))
