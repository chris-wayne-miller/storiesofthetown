#!/bin/bash

# Script to execute the simulation-narrative generation process
# for the CSC 791: Generative Methods final project

clear

echo -n "Enter your Python Version 2 name (e.g. python, python2, etc.): "
read python2name
echo -n "Enter your Python Version 3 name (e.g. python, python3, etc.): "
read python3name
echo "Please select a problem generation complexity option for the automated plan generator script"
echo -n "Your options are [likes], [loves], or [all]  (no brackets): "
read option

echo "Running Talk of the Town simulation..."
$python2name test.py
echo "Generating a problem definition for Glaive..."
echo "Please be patient, executing a random search process..."
$python3name glaiveproblemsetup.py $option
echo "Executing Glaive... "
echo "If this step takes more than 30s minute it might be unsolvable..."
echo "If this occurs, I recommend re-executing this script or glaiveproblemsetup.py"
java -jar glaive.jar -d tot-domain.pddl -p tot-problem.pddl -o tot-solution.txt
echo "Outputting a narrative..."
$python3name plan_to_text.py ./tot-solution.txt
