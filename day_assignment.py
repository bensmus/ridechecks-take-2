from typing import Dict, List, Tuple, Set, Iterable, Callable
import random


class NoAssignmentError(Exception):
    pass


def generate_day_assignment(worker_time: int, rides_time: Dict[str, int], workers_can_check: Dict[str, Set[str]]) -> Dict[str, str]:
    """
    Find a complete assignment using dfs (backtracking), then improve the complete assignment using hillclimbing.
    Returns a random locally optimal assignment {ride: worker...} and the remaining times of the workers {worker: time...}.
    """
    def dfs(partial_assignment: Dict[str, str], partial_worker_times_remaining: Dict[str, int]) -> Tuple[Dict[str, str], Dict[str, int]]:
        """
        partial_assignment: Dictionary of {ride: worker...} containing a subset of rides.
        worker_times: How much time does every worker have remaining.
        Randomized dfs: find a random solution to CSP that is not even locally optimal.
        """
        # Base case: 
        if len(partial_assignment) == len(rides_time):
            return partial_assignment, partial_worker_times_remaining
        # Recursive case:
        ride = next(ride for ride in rides_time if ride not in partial_assignment)
        workers = list(workers_can_check.keys())
        random.shuffle(workers)
        for worker in workers: # Try to assign every worker to the ride in a random order.
            if ride in workers_can_check[worker] and rides_time[ride] <= partial_worker_times_remaining[worker]:
                # Recursive call, adding ride and worker to partial_assignment, worker_times reflect remaining time.
                complete_assignment, complete_worker_times_remaining = dfs(
                    partial_assignment | {ride: worker}, 
                    partial_worker_times_remaining | {worker: partial_worker_times_remaining[worker] - rides_time[ride]}
                )
                if complete_assignment:
                    return complete_assignment, complete_worker_times_remaining
        # Could not find a complete assignment based on the partial_assignment and worker_times_remaining.
        return {}, partial_worker_times_remaining
    

    complete_assignment, complete_worker_times_remaining = dfs({}, {worker: worker_time for worker in workers_can_check})
    if complete_assignment == {}:
        raise NoAssignmentError(f"No assignment exists for worker_time={worker_time}, ride_times={rides_time}, can_check={workers_can_check}")

    def hillclimb(complete_assignment: Dict[str, str], complete_worker_times_remaining: Dict[str, int]) -> bool:
        """
        Try to hillclimb (improve the assignment). Randomized to find different local optimums.
        Return whether further hillclimbing is possible.
        """
        def try_transfer_ride(transferring_worker: str) -> Tuple[str, str] | None:
            """
            Transfer rides from transferring_worker to another if it results in a better 
            balance of remaining time among the workers.

            A: accepting_worker time remaining.
            T: transferring_worker time remaining.
            |(A - delta) - (T + delta)| < |A - T| <=> Should transfer.

            Returns ride, accepting_worker if transfer occurs, otherwise returns None.
            """
            def should_transfer(accepting_worker_time_remaining: int, transferring_worker_time_remaining: int, ride_time: int) -> bool:
                new_diff = abs(accepting_worker_time_remaining - transferring_worker_time_remaining - 2 * ride_time)
                old_diff = abs(accepting_worker_time_remaining - transferring_worker_time_remaining)
                return new_diff < old_diff and accepting_worker_time_remaining > transferring_worker_time_remaining      
            transferring_worker_time_remaining = complete_worker_times_remaining[transferring_worker]
            rides_to_transfer = [ride for ride in complete_assignment if complete_assignment[ride] == transferring_worker]
            random.shuffle(rides_to_transfer)
            for ride in rides_to_transfer:
                ride_time = rides_time[ride]
                accepting_workers = filter(lambda worker: worker != transferring_worker and ride in workers_can_check[worker], workers_can_check.keys())
                for accepting_worker in accepting_workers:
                    accepting_worker_time_remaining = complete_worker_times_remaining[accepting_worker]
                    if should_transfer(accepting_worker_time_remaining, transferring_worker_time_remaining, ride_time):
                        return ride, accepting_worker
            return None
        transferring_workers = list(workers_can_check.keys()) # All workers.
        random.shuffle(transferring_workers)
        for transferring_worker in transferring_workers:
            # Choose random worker that will try to give one of its rides to a worker.
            if (res := try_transfer_ride(transferring_worker)):
                ride_transferred = res[0]
                accepting_worker = res[1]
                complete_assignment[ride_transferred] = accepting_worker
                complete_worker_times_remaining[transferring_worker] += rides_time[ride_transferred]
                complete_worker_times_remaining[accepting_worker] -= rides_time[ride_transferred]
                return True
        return False

    while hillclimb(complete_assignment, complete_worker_times_remaining): # Hillclimb until local optimum.
        pass
    return complete_assignment

