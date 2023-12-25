from typing import Dict, List, Tuple, Set, Iterable, Callable
import random

# INPUTS
worker_time = 40
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
assignment = {
    'RA': 'WA', 
    'RB': 'WB',
    'RC': 'WA',
    'RD': 'WC',
    'RE': 'WC'
}
'''

# TODO: Add unit tests.
# def generate_random_assignment(worker_time: int, ride_times: Dict[str, int], can_check: Dict[str, Set[str]]) -> Dict[str, str]:
#     worker_times = {worker: worker_time for worker in can_check} # Modified in loop.
#     partial_assignment: Dict[str, str] = {} # Modified in loop.
#     for ride in ride_times:
#         ride_time = ride_times[ride]
#         # Get candidate workers that have time to check the ride and have permission to check the ride.
#         candidate_workers = [worker for worker in can_check if worker_times[worker] >= ride_time and ride in can_check[worker]]
#         if candidate_workers == []:
#             raise Exception("Unlucky")
#         random_candidate_worker = random.choice(candidate_workers)
#         partial_assignment[ride] = random_candidate_worker
#         worker_times[random_candidate_worker] -= ride_time
#     return partial_assignment # Partial assignment is a satisfying assignment at this point.


def generate_random_assignment(worker_time: int, ride_times: Dict[str, int], can_check: Dict[str, Set[str]]) -> Dict[str, str]:
    
    def dfs(partial_assignment: Dict[str, str], worker_times: Dict[str, int]) -> Dict[str, str]:
        """
        partial_assignment: Dictionary of {ride: worker...} containing a subset of rides.
        worker_times: How much time does every worker have remaining.
        Randomized dfs: find a random solution to CSP that is not even locally optimal.
        """    
        # Base case: 
        if len(partial_assignment) == len(ride_times):
            return partial_assignment
        # Recursive case:
        ride = next(ride for ride in ride_times if ride not in partial_assignment)
        workers = list(can_check.keys())
        random.shuffle(workers) # Randomizing the workers.
        for worker in workers: # Try to assign every worker to the ride.
            if ride in can_check[worker] and ride_times[ride] <= worker_times[worker]:
                # Recursive call, adding ride and worker to partial_assignment, worker_times reflect remaining time.
                complete_assignment = dfs(
                    partial_assignment | {ride: worker}, 
                    worker_times | {worker: worker_times[worker] - ride_times[ride]}
                )
                if complete_assignment:
                    return complete_assignment
        # Could not find a complete assignment based on the partial_assignment and worker_times.
        return {}
    
    complete_assignment = dfs({}, {worker: worker_time for worker in can_check})
    if complete_assignment == {}:
        raise Exception("No assignment exists, problem is overconstrained.")
    return complete_assignment


print(generate_random_assignment(worker_time, ride_times, can_check))

# TODO: Perform hill climbing on the objective of minimizing the maximum work time for any worker.