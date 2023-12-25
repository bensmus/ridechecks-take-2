from typing import Dict, List, Tuple, Set, Iterable, Callable
import random

# INPUTS
worker_time = 30
ride_times = {
    'RA': 10, 
    'RB': 12, 
    'RC': 14, 
    'RD': 15, 
    'RE': 20
}
can_check = {
    'WA': {'RA', 'RB'},
    'WB': {'RA', 'RB', 'RC', 'RD', 'RE'},
    'WC': {'RE', 'RD'}
}

# OUTPUT
'''
solution = {
    'RA': 'WA', 
    'RB': 'WB',
    'RC': 'WA',
    'RD': 'WC',
    'RE': 'WC'
}
'''

# TODO: Add unit tests.
# TODO: Change this to use DFS backtracking.
def generate_random_solution(worker_time: int, ride_times: Dict[str, int], can_check: Dict[str, Set[str]]) -> Dict[str, str]:
    remaining_times = {worker: worker_time for worker in can_check} # Modified in loop.
    partial_solution: Dict[str, str] = {} # Modified in loop.
    for ride in ride_times:
        ride_time = ride_times[ride]
        # Get candidate workers that have time to check the ride and have permission to check the ride.
        candidate_workers = [worker for worker in can_check if remaining_times[worker] >= ride_time and ride in can_check[worker]]
        if candidate_workers == []:
            raise Exception("Unlucky")
        random_candidate_worker = random.choice(candidate_workers)
        partial_solution[ride] = random_candidate_worker
        remaining_times[random_candidate_worker] -= ride_time
    return partial_solution # Partial solution is a satisfying assignment at this point.


print(generate_random_solution(worker_time, ride_times, can_check))

# TODO: Perform hill climbing on the objective of minimizing the maximum work time for any worker.