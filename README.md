Runnable files are "scripts/main_UAV.py" and "scripts/main_USV.py". To perform a test, both of these have to be running in their own terminal. The scripts communicate with each other through ROS, so make sure that roscore is also running in a terminal. In these files, the prediction horizon for the algorithms can be set, but one has to manually make sure that the UAV and USV use the same prediction horizon. Other settings, such as which of the three algorithms (centralised, distributed, and cascading) should be used, can be set in "scripts/IMPORT_ME.py". Dynamics and constraint parameters are defined in "scripts/matrices_and_paramters.py". 

The code is most easily understood by reading the files "scripts/UAV_simulation.py" and "scripts/USV_simulation.py", which contain the main classes that actually implement the algorithms. The optimisation problems solved in the algorithms are defined in "scripts/problemClasses.py".



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
