from typing import Dict, List, Tuple, Set, Iterable, Collection, Callable, Any, Literal, get_args
from day_assignment import generate_day_assignment, NoDayAssignment
from util import without_keys, Day

DayInfoKey = Literal['time', 'uaworkers', 'uarides']
DayInfo = Dict[DayInfoKey, Any]

def generate_multiple_day_assignments(
        days_info: Dict[Day, DayInfo], 
        all_rides_time: Dict[str, int], 
        all_workers_can_check: Dict[str, Set[str]]) -> Dict[Day, Dict[str, str]]:
    multiple_day_assignments: Dict[Day, Dict[str, str]] = {}
    for day in get_args(Day): # Looping through those and not days_info keys to preserve order
        if day not in days_info: # Playland closed on that day
            continue
        day_info = days_info[day]
        worker_time: int = day_info['time']
        day_ride_times = without_keys(all_rides_time, day_info['uarides'])
        day_can_check = without_keys(all_workers_can_check, day_info['uaworkers'])
        try:
            day_assignment = generate_day_assignment(worker_time, day_ride_times, day_can_check)
        except NoDayAssignment as e:
            # print(e)
            raise NoDayAssignment(f"No assignment exists for day '{day}'")
        multiple_day_assignments[day] = day_assignment
    return multiple_day_assignments
