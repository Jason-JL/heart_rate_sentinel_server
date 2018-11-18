#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Jason L

import pytest
from toolbox_jason import validate_json_data_entry, validate_heart_rate_request
from toolbox_jason import average_heart_rate


@pytest.mark.parametrize("test_input, expected", [
    ([1, 1, 1, 1, 1, 1, 1, 1, 1], 1),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], 5),
    ([3, 4], 3)
])
def test_average_heart_rate(test_input, expected):
    assert(average_heart_rate(test_input) == expected)


@pytest.mark.parametrize("test_input, expected", [
    ({'integer_type': 1, 'char_type': 'aa', 'list_type': [1, 1]}, True),
])
def test_validate_json_data_entry(test_input, expected):
    assert(validate_json_data_entry(test_input, test_input) == expected)


@pytest.mark.parametrize("test_input, expected", [
    ([1, 152], "Tachycardia"),
    ([3, 138], "Tachycardia"),
    ([5, 134], "Tachycardia"),
    ([8, 131], "Tachycardia"),
    ([12, 120], "Tachycardia"),
    ([16, 101], "Tachycardia"),
    ([16, 99], "Normal")
])
def test_validate_heart_rate_request(test_input, expected):
    assert(validate_heart_rate_request(test_input[0],
                                       test_input[1]) == expected)
