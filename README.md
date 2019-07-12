Runnable files are "scripts/UAV_TESTER.py" and "scripts/USV_TESTER.py". To perform a test, both of these have to be running in their own terminal. The scripts communicate (quite inelegantly) with each other in ROS, so make sure that roscore is also running in a terminal.

The code is most easily understood by reading the files "scripts/UAV_simulation.py" and "scripts/USV_simulation", which contain the main classes for running the UAV simulation and USV simulation respectively. 

NOTE: These files are in an AWFUL condition and code cleanup is nowhere near finished. I don't recomment trying to understand them until a future commit with severe restructuring and clarification is finished. Sorry, but constant change of plans during the project has made the code into quite a mess.
