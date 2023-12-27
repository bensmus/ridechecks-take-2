# Read files in input folder, generate multiple_day_assignments, and write ridechecks_<day>_<month>_<year>.yaml file to output folder.

from mutliple_day_assignments import generate_multiple_day_assignments
import os

# Check the input folder.
if (not os.path.exists('input') or 
    not os.path.exists('input/workers_cannot_check.yaml') or 
    not os.path.exists('input/rides_time.yaml') or
    not os.path.exists('input/days_info.yaml')
    ):
    print("FAILURE: Please make sure that there is a folder called 'input' containing the files 'workers_cannot_check.yaml', 'rides_time.yaml', and 'days_info.yaml'.")
    exit()

# Check the output folder.
if not os.path.exists('output'):
    print("FAILURE: Please make sure that there is a folder called 'output.'")

# Read yaml files in the input folder to obtain:
# 1. week_info: Dict[Day, DayInfo] 
# 2. all_ride_times: Dict[str, int]
# 3. all_can_check: Dict[str, Set[str]])

# Validate the data.

# Generate assignments.

# Write assignments to yaml file.