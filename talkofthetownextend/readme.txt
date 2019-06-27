Readme File for Stories of the Town:
======================================

The entire process of generating character models via Talk of the Town, extracting them to JSON files, creating planning problems using characters from the JSON files, executing the problem plan solver, and generating a narrative is outlined in this file.  The process is delineated as follows and terminal commands for each step will be provided below:

================

Programs Needed to Execute Every Process:
	1. Tracery	(PCFG)
	2. Python2	(Talk of the Town)
	3. Python3	(all of the other Python scripts)
		- Libraries needed (Can be installed using pip install library_name:
		  a) tracery
		  b) numpy
		  c) networkx (optional, for visualization)
		  d) matplotlib (optional, for visualization)
	4. Java 	(Glaive)
	5. Jupyter (PCFG experimentation)

================

================

Process Overview:
	1. Run Talk of the Town via test.py (Python2)
	2. Run the problem generator via glaiveproblemsetup.py
	3. Solve the generated problem via Glaive
	4. Translate the outputted solution to a narrative via plan_to_text.py

Process Commands:
	1. $ python test.py 		  (written in Python 2)
	2. $ python glaiveproblemsetup.py [likes, loves, all]  (written in Python 3)
		(e.g. $ python glaiveproblemsetup.py likes)
	3. $ java -jar glaive.jar -d tot-domain.pddl -p tot-problem.pddl -o tot-solution.txt
	4. $ python plan_to_text.py ./tot-solution.txt	(written in Python 3)


***We have also provided a shell script to automate the steps described above.  The shell script is named "run.sh"***
================

1. Running the following command will run Talk of the Town with some hooks added in to extract character models as JSON objects.  The "hooks" start at Line 54 with the comment header "# Iterate through residents and export json files". Any information relevant to person objects as defined by Talk of the Town can be extracted in this section of the code.  Talk of the Town was originally written in Python 2 so Python 2 is required to execute this command.  This step only produces the JSON files for generated characters in the folder "personjsons".  Given that we have submitted our project with "personjsons" folder with some existing JSONs from previous test.py executions, this step can be skipped unless the folder does not exist for some reason.  Feel free to skip this command if you don't want to re-generate person JSON files.

2. Running this command will produce a planning problem based on the JSON objects from Step 1 that can be solved via Glaive.  When executing this command please select ONE of the options in the brackets.  These influence the goals that are written to the problem file.  The options in order of increasing plan-solving complexity are: likes, loves, all.  (Please note that "all" is more likely to yield no solutions due to higher complexity than the other options while the others are far more likely to be solvable and solved faster). This script will write the generated problem to the file "tot-problem.pddl".  Feel free to skip this command if you don't want to re-generate a problem definition file.

3. Running this command instructs Glaive to solve the planning problem from Step 2 while also using a problem domain file we have crafted.  The domain file is named "tot-domain.pddl".  The option flag towards the end of the command writes the problem solution to the file "tot-solution.txt". 

4. Running this last command will execute a script to parse the solution file from Step 3 and translate the verb-subject(s) pairs in the solution into a easily readable story.  The second parameter to this command is the file path to the outputted solution from Step 3.

Note: The probabilistic context-free grammar can be tested via the Jupyter notebook called Tracery_and_PCFG_experiments.ipynb. Executing the PCFG will require having Jupyter and tracery for python installed as given above. We chose to use a separate Jupyter notebook for this part since it was mostly experimental and not a part of the final pipeline. 

Note: If you are unable to successfully solved a problem with the "all" flag, there are solvable domain-problem files in the folder solved-domain-problems/Untitled Folder 3 with a domain and problem description file.  If you copy-paste the domain and problem to the root of the "talkofthetownextend" root folder, Glaive will be able to solve and produce a narrative for the problem.  If you decide to do this, just execute Step 3 and Step 4 after copying the files.

================

Author Contact:

cwmille6@ncsu.edu
