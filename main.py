# Read files in input folder, generate multiple_day_assignments, and write ridechecks_<day>_<month>_<year> YAML and HTML files to output folder.

from multiple_day_assignments import generate_multiple_day_assignments, Day, DayInfo
from day_assignment import NoDayAssignment
from make_html_table import make_html_table
from util import is_list_of_strings, without_keys
from typing import Dict, List, Tuple, Set, Iterable, Callable, Collection, Any
import os
import yaml


def early_exit(s: str):
    """
    Exit before generating files because conditions for generating files are not met.
    """
    print(f"PDF NOT GENERATED: {s}.")
    exit()


# Check the input folder.

if (not os.path.exists('input') or 
    not os.path.exists('input/workers_cannot_check.yaml') or 
    not os.path.exists('input/rides_time.yaml') or
    not os.path.exists('input/days_info.yaml')
    ):
    early_exit("Please make sure that there is a folder called 'input' containing the files 'workers_cannot_check.yaml', 'rides_time.yaml', and 'days_info.yaml'")

# Check the output folder.

if not os.path.exists('output'):
    early_exit("Please make sure that there is a folder called 'output'")

# Read yaml files in the input folder.
    
with open('input/workers_cannot_check.yaml', 'r') as file:
    all_workers_cannot_check: Dict[str, List[str]] = yaml.safe_load(file)

with open('input/rides_time.yaml', 'r') as file:
    all_rides_time: Dict[str, int] = yaml.safe_load(file)

with open('input/days_info.yaml', 'r') as file:
    days_info: Dict[Day, DayInfo] = yaml.safe_load(file)

# Validate the data.

for ride, time in all_rides_time.items():
    if type(ride) != str or type(time) != int:
        early_exit("Data in 'rides_time.yaml' does not follow format")

for worker, cannot_check in all_workers_cannot_check.items():
    if type(worker) != str or type(cannot_check) != list:
        early_exit("Data in 'workers_cannot_check.yaml' does not follow format")
    for ride in cannot_check:
        if ride not in all_rides_time:
            early_exit(f"Ride '{ride}' listed in 'workers_cannot_check.yaml' does not appear in 'rides_time.yaml', check ride name")

for day, day_info in days_info.items():
    if type(day) != str or type(day_info) != dict:
        early_exit("Data in 'days_info.yaml' does not follow format")
    
    for key, value in day_info.items():
        if key not in ['time', 'unavail_workers', 'unavail_rides']:
            early_exit("Data in 'days_info.yaml' does not follow format")
    
        if type(value) != int and not is_list_of_strings(value):
            early_exit("Data in 'days_info.yaml' does not follow format")
    
        if key == 'time' and type(value) != int:
            early_exit("Data in 'days_info.yaml' does not follow format, time must be a number")
    
        if (key == 'unavail_rides' or key == 'unavail_workers') and type(value) != list:
            early_exit("Data in 'days_info.yaml' does not follow format, expected a list of unavailable workers or unavailable rides")
    
        if key == 'unavail_rides':
            for ride in value: # type: ignore
                if ride not in all_rides_time:
                    early_exit(f"Unavailable ride '{ride}' listed in 'days_info.yaml' for day '{day}' does not appear in 'rides_time.yaml', check ride name")
        
        if key == 'unavail_workers':
            for worker in value: # type: ignore
                if worker not in all_workers_cannot_check:
                    early_exit(f"Unavailable worker '{worker}' listed in 'days_info.yaml' for day '{day}' does not appear in 'workers_cannot_check.yaml', check worker name")

# Convert all_workers_cannot_check to all_workers_can_check.

all_workers_can_check: Dict[str, Set[str]] = {}
for worker in all_workers_cannot_check:
    cannot_check = all_workers_cannot_check[worker]
    all_workers_can_check[worker] = set(all_rides_time.keys()) - set(cannot_check)

# Ignore days when time is 0 (playland is closed).

days_info = {day: day_info for day, day_info in days_info.items() if day_info['time'] != 0}

# Generate assignments, handling case where assignments cannot be generated.

try:
    multiple_day_assignments = generate_multiple_day_assignments(days_info, all_rides_time, all_workers_can_check)
except NoDayAssignment as e:
    early_exit(str(e))

# Write assignments to YAML file.

with open('output/ridechecks.yaml', 'w') as f:
    yaml.safe_dump(multiple_day_assignments, f, sort_keys=False) # type: ignore
    
# Write assignments to HTML file using jinja.

make_html_table(multiple_day_assignments, 'output/ridechecks.html') # type: ignore
