from typing import Dict, List, Tuple, Set, Iterable, Callable
import random


def generate_random_assignment(worker_time: int, ride_times: Dict[str, int], can_check: Dict[str, Set[str]]) -> Tuple[Dict[str, str], Dict[str, int]]:
    
    def dfs(partial_assignment: Dict[str, str], partial_worker_times_remaining: Dict[str, int]) -> Tuple[Dict[str, str], Dict[str, int]]:
        """
        partial_assignment: Dictionary of {ride: worker...} containing a subset of rides.
        worker_times: How much time does every worker have remaining.
        Randomized dfs: find a random solution to CSP that is not even locally optimal.
        """
        # Base case: 
        if len(partial_assignment) == len(ride_times):
            return partial_assignment, partial_worker_times_remaining
        # Recursive case:
        ride = next(ride for ride in ride_times if ride not in partial_assignment)
        workers = list(can_check.keys())
        random.shuffle(workers)
        for worker in workers: # Try to assign every worker to the ride in a random order.
            if ride in can_check[worker] and ride_times[ride] <= partial_worker_times_remaining[worker]:
                # Recursive call, adding ride and worker to partial_assignment, worker_times reflect remaining time.
                complete_assignment, complete_worker_times_remaining = dfs(
                    partial_assignment | {ride: worker}, 
                    partial_worker_times_remaining | {worker: partial_worker_times_remaining[worker] - ride_times[ride]}
                )
                if complete_assignment:
                    return complete_assignment, complete_worker_times_remaining
        # Could not find a complete assignment based on the partial_assignment and worker_times_remaining.
        return {}, partial_worker_times_remaining
    
    complete_assignment, complete_worker_times_remaining = dfs({}, {worker: worker_time for worker in can_check})
    if complete_assignment == {}:
        raise Exception("No assignment exists, problem is overconstrained.")
    
    # Now hillclimb this assignment
    return complete_assignment, complete_worker_times_remaining


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