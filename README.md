**Minimum required work to get results:** 

Make sure roscore is already running, and run "scripts/main_UAV.py" and "scripts/main_USV.py" in separate terminal windows on the same machine. After the scripts have terminated, run "scripts/data_analysis.py Experiment_1" to get a plot of the two vehicles moving, as seen from above. If you have performed more than one experiment, you need to go into the folder "robbj_experiment_results" in your home directory as put the name of the most recent folder there instead of "Experiment_1".

**More detailed experiment procedure:**

Runnable files are "scripts/main_UAV.py" and "scripts/main_USV.py". To perform a test, make sure roscore is already running, and then run both of these scripts, each in their own terminal. main_UAV represents the algorithm running on the UAV and main_USV the algorithm running on the USV, and they communicate with each other using ROS. Then can run on the same machine or on different machines, but when running on seperate machines, additional steps are necessary (see [this tutorial](http://wiki.ros.org/ROS/Tutorials/MultipleMachines)). In these files one can set the prediction horizons of the vehicles, their initial states, as well as whether the USV should pursue a second objective other than landing. **Note:** You have to manually ensure that the two scripts use the same prediction horizon.

In "scripts/IMPORT_MAIN.py", most important parameters are defined. There you can set which of the three algorithms (centralised, distributed, and cascade) should be used, how many iterations the simulations should last, and whether the UAV should be by the scripts, or if a physical drone is used. If the parameter "USE_HIL" is set to True, the UAV algorithms will publish control inputs to appropriate topics and get the state estimate from listening to appropriate topics. If it's set to false, the same linear model that is used in the MPC formulation will be used to simulate its dynamics. The dynamics of the USV are always simulated using the same model that is used in the MPC formulation. Dynamics and constraint parameters of the UAV and USV are defined in "scripts/IMPORT_UAV.py" and "scripts/IMPORT_USV.py" respectively.

The code is most easily understood by reading the files "scripts/UAV_simulation.py" and "scripts/USV_simulation.py", which contain the main classes that actually implement the algorithms. Start with the function "simulate_problem()" if you're curious about how the code is implemented. The optimisation problems solved in the algorithms are defined in "scripts/problemClasses.py".

When performing an experiment, data from it will be stored in a folder called "robbj_experiment_results" created in your home directory, on both the machine running main_UAV and main_USV. Data from each experiment will be stored in a separate subfolder named "Experiment_i", where i will be an incremented experiment index. To understand this data and the functions for visualising it, one should really understand the code in UAV_simulation.py and USV_simulation.py. However, if you run the scripts by writing "python path_to_file/data_analysis.py Experiment_i", where "Experiment_i" is the name of the folder for the experiment that you want to visualise, a top-view of the motion of the vehicle's will be plotted. **Note:** If the algorithms were ran on different machines, the data from the two "robbj_experiment_results"-folders need to be merged before plotting. Also, with default settings in data_analysis.py, the plotting will only be accurate if both algorithms were ran on the same machines or if the two machines running the algorithms had synchronised clocks. 

If the machines running the algorithms did not have synchronised clocks, one can go down to the bottom of "data_analysis.py" and change one of the arguments to "perspective = UAV" or "perspective = RAW". There one can also change which function is called. I recommend calling plot_3d() or plot_with_constraints() for interesting perspectives.

# Citing
If you find this work useful in your research, please cite the main paper. The paper will be published by IFAC in July 2020. 

**Text citation**
```
R. Bereza and L. Persson and B. Wahlberg, "Distributed Model Predictive Control for Cooperative Landing," 2020 Proceedings of IFAC World Congress, Berlin, 2020.
```

**BibTeX citation**
```
@inproceedings{berezapersson,
  title={Distributed Model Predictive Control for Cooperative Landing},
  author={Bereza, Robert and Persson, Linnea and Wahlberg, Bo},
  booktitle={2020 Proceedings of IFAC World Congress},
  year={2020},
  organization={IFAC},
  city={Berlin}
}
```
