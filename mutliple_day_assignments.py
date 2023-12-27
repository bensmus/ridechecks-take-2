from typing import Dict, List, Tuple, Set, Iterable, Collection, Callable, Any, Literal
from day_assignment import generate_day_assignment

Day = Literal['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
DayInfoKey = Literal['time', 'unavail_workers', 'unavail_rides']
DayInfo = Dict[DayInfoKey, Any]


def without_keys[T](d: Dict[T, Any], keys_to_exclude: Collection[T]) -> Dict[T, Any]:
    return {k: v for k, v in d.items() if k not in keys_to_exclude}


def generate_multiple_day_assignments(
        days_info: Dict[Day, DayInfo], 
        all_rides_time: Dict[str, int], 
        all_workers_can_check: Dict[str, Set[str]]) -> Dict[Day, Dict[str, str]]:
    multiple_day_assignments: Dict[Day, Dict[str, str]] = {}
    for day, day_info in days_info.items():
        worker_time: int = day_info['time']
        day_ride_times = without_keys(all_rides_time, day_info['unavail_rides'])
        day_can_check = without_keys(all_workers_can_check, day_info['unavail_workers'])
        day_assignment = generate_day_assignment(worker_time, day_ride_times, day_can_check)
        multiple_day_assignments[day] = day_assignment
    return multiple_day_assignments
