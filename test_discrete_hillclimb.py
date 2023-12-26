from typing import Dict, List, Tuple, Set, Iterable, Callable
import pytest
from discrete_hillclimb import generate_random_assignment


def is_valid_assignment(assignment: Dict[str, str], worker_time: int, ride_times: Dict[str, int], can_check: Dict[str, Set[str]]) -> bool:
    # Check that all workers have time.
    for worker in can_check:
        worker_time_remaining = worker_time
        for ride in assignment:
            if assignment[ride] == worker:
                worker_time_remaining -= ride_times[ride]
        if worker_time_remaining < 0:
            return False
    # Check that all workers check ride that they can check.
    for ride, worker in assignment.items():
        if ride not in can_check[worker]:
            return False
    return True
    

def test_generate_random_assignment():
    worker_time = 30
    ride_times = {
        'RA': 10, 
        'RB': 12, 
        'RC': 14, 
        'RD': 15, 
        'RE': 20,
        'RF': 1,
        'RG': 4,
        'RH': 11
    }
    can_check = {
        'WA': {'RA', 'RB'},
        'WB': {'RA', 'RB', 'RC', 'RD', 'RE'},
        'WC': {'RE', 'RD', 'RA'},
        'WD': {'RG', 'RF', 'RC'},
        'WE': {'RH', 'RA', 'RD'}
    }
    assignment, _ = generate_random_assignment(worker_time, ride_times, can_check)
    assert is_valid_assignment(assignment, worker_time, ride_times, can_check)


if __name__ == "__main__":
    pytest.main()
