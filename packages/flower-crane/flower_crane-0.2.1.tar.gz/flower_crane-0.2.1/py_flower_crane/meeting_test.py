from meeting import find_meeting
from util import get_data, truth

import flower_crane

MAX_DIST_KM = 2.0
MAX_DIST_DEGREE = MAX_DIST_KM / 111.0
MAX_ALT_DIST = 500


def test_find_meeting_rs():
    data = get_data()
    data = (
        [(el[0], el[1]) for el in data[0]],
        [(el[0], el[1]) for el in data[1]],
        data[2].tolist(),
        data[3].tolist(),
        data[4].tolist(),
        data[5].tolist(),
        data[6],
        data[7],
    )
    meeting, _ = flower_crane.find_meeting(*data)
    assert meeting == truth, f"Found: {meeting}"


def test_find_meeting_py():
    meeting, _ = find_meeting(*get_data())
    assert meeting == truth, f"Found: {meeting}"


def test_find_meeting_rs_np():
    meeting, _ = flower_crane.find_meeting_np(*get_data())
    assert meeting == truth, f"Found: {meeting}"
