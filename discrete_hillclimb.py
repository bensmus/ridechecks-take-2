from typing import Dict, List, Tuple, Set, Iterable, Callable
import random


def generate_random_assignment(worker_time: int, ride_times: Dict[str, int], can_check: Dict[str, Set[str]]) -> Tuple[Dict[str, str], Dict[str, int]]:
    
    def dfs(p_assignment: Dict[str, str], p_worker_times_remaining: Dict[str, int]) -> Tuple[Dict[str, str], Dict[str, int]]:
        """
        p_assignment: Dictionary of {ride: worker...} containing a subset of rides (partial assignment).
        c_... means complete assignment or worker times remaining.
        worker_times: How much time does every worker have remaining.
        Randomized dfs: find a random solution to CSP that is not even locally optimal.
        """
        # Base case: 
        if len(p_assignment) == len(ride_times):
            return p_assignment, p_worker_times_remaining
        # Recursive case:
        ride = next(ride for ride in ride_times if ride not in p_assignment)
        workers = list(can_check.keys())
        random.shuffle(workers)
        for worker in workers: # Try to assign every worker to the ride in a random order.
            if ride in can_check[worker] and ride_times[ride] <= p_worker_times_remaining[worker]:
                # Recursive call, adding ride and worker to partial_assignment, worker_times reflect remaining time.
                c_assignment, c_worker_times_remaining = dfs(
                    p_assignment | {ride: worker}, 
                    p_worker_times_remaining | {worker: p_worker_times_remaining[worker] - ride_times[ride]}
                )
                if c_assignment:
                    return c_assignment, c_worker_times_remaining
        # Could not find a complete assignment based on the partial_assignment and worker_times_remaining.
        return {}, p_worker_times_remaining
    
    c_assignment, c_worker_times_remaining = dfs({}, {worker: worker_time for worker in can_check})
    if c_assignment == {}:
        raise Exception("No assignment exists, problem is overconstrained.")
    return c_assignment, c_worker_times_remaining


if __name__ == '__main__':
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
    print(generate_random_assignment(worker_time, ride_times, can_check))

# TODO: Perform hill climbing on the objective of minimizing the maximum work time for any worker.