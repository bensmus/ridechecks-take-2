from typing import Dict
from multiple_day_assignments import generate_multiple_day_assignments, without_keys, Day, DayInfo 
from test_day_assignment import is_valid_assignment


def test_without_keys(): 
    d = {'apple': 2, 'cuke': 3, 'frog': 4}
    assert without_keys(d, ['apple']) == {'cuke': 3, 'frog': 4}
    d = {'apple': 2, 'cuke': 3, 'frog': 4}
    assert without_keys(d, ['apple', 'frog']) == {'cuke': 3}


def test_generate_multiple_day_assignments():
    week_info: Dict[Day, DayInfo] = {
        'mon': {
            'time': 10,
            'uaworkers': [],
            'uarides': []
        },
        'wed': {
            'time': 20,
            'uaworkers': [],
            'uarides': []
        }
    }
    all_ride_times = {
        'wooden': 10,
        'scary': 1,
        'slow': 1,
        'fast': 5
    }
    all_can_check = {
        'john': {'wooden', 'scary', 'slow'},
        'bob': {'wooden', 'scary', 'slow', 'fast'},
    }
    assignments = generate_multiple_day_assignments(week_info, all_ride_times, all_can_check)
    assert 'mon' in assignments
    assert 'wed' in assignments
    assert is_valid_assignment(assignments['mon'], week_info['mon']['time'], without_keys(all_ride_times, week_info['mon']['uarides']), without_keys(all_can_check, week_info['mon']['uaworkers']))
    assert is_valid_assignment(assignments['wed'], week_info['wed']['time'], without_keys(all_ride_times, week_info['wed']['uarides']), without_keys(all_can_check, week_info['wed']['uaworkers']))
