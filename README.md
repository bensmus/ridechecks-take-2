# Usage

This is a scheduling tool that assigns maintenance tasks to workers based on the worker's training and availability. The goal is to make all workers have the same total time spent on maintenance. The tool is designed specifically for the context of Playland daily rollercoaster/ride maintenance.

The tool looks at Playland ridecheck data specified in the `input` folder and creates a schedule in the `output` folder.

To use the command line tool, first download the zip archive of this repository.

Then unzip the archive, open up powershell in the unzipped location, and run `.\dist\main.exe`. This creates a schedule in the `output` folder called `ridechecks.yaml`. This schedule will change when you modify the contents of the `input` folder such as the lengths of the maintenance tasks (`rides_time.yaml`) or availability (`days_info.yaml`).

# More info
*If you just want to use the tool, you don't have to read this.*

The scheduling task is basically a constraint satisfaction problem (CSP) where for all workers, the sum of the assigned maintenance task times must be below a certain amount. Since this job of assigning maintenance tasks was done by a person, this CSP is actually fairly easy to solve, it is underconstrained. So a simple depth first search with checking (a.k.a backtracking) is able to solve the CSP quickly. Then, the solutions are improved using hillclimbing. To see the algorithm, look at `day_assignment.py`.

# GUI - not available yet, in progress.

Path of the user (99% of time):

- Click shortcut on desktop to run python script which opens GUI.

(in GUI)

- Edit days_info
	- Days open
	- Day time
    ---> days_info: (Mon, 10 {-}), (Tue, 10 {-}), (Thu, 10 {-})
    ---> Add day: Two inputs
    - For each day e.g. <- Mon ->
	    - Workers not avail
	    - Rides not avail
        ---> absent workers: (John {-}), (Bill {-})
        ---> Add absent: One input
        ---> closed rides: (Wooden {-})
        ---> Add closed: One input

- Click on button to generate HTML table file which saves the file on the system and opens it in the browser.

---

Sometimes, editing workers permissions is neccessary. GUI for this will be added at a later time.

Note that being able to see past schedules is a requirement.
