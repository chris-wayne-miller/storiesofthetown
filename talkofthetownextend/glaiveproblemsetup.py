# File to set up a problem specification for the Glaive Narrative Planner

import os
import numpy
import json
import random
import sys

# Function definitions
def pick_with_equal_probability_no_dupes(items, selected_items):
	valid_candidate = False
	while not valid_candidate:
		individual_probability = 1/len(items)
		probabilities_array = [individual_probability]*len(items)
		item_chosen = numpy.random.choice(items, p=probabilities_array)
		if item_chosen not in selected_items:
			selected_items.append(item_chosen)
			valid_candidate = True

def main():
	# Command line option to specify what goals to add to the problem
        # Valid options are: likes, loves, or all
	goal_option = sys.argv[1]
	while True:
		# Number of people to include in a planning problem
		num_people = 5
		# Trackers for predicates
		num_dislikes = 0
		num_love_interests = 0
		num_worst_enemies_with_intent = 0
		if goal_option == "likes":
			min_num_dislikes = 2
			min_num_love_interests = 0
			min_num_worst_enemies_with_intent = 0
		elif goal_option == "loves":
			min_num_dislikes = 0
			min_num_love_interests = 1
			min_num_worst_enemies_with_intent = 0
		else:
			min_num_dislikes = 2
			min_num_love_interests = 1
			min_num_worst_enemies_with_intent = 1
                # Intent/goal trackers (these are "existential" booleans)
		# (e.g. love_goal = True -> there exists a love goal)
		loves_intent = False				# currently not in use
		loves_goal = False
		likes_intent = False				# currently not in use
		likes_goal = False
		enemy_persuade_to_dislike_intent = False	# currently not being used
		enemy_persuade_to_dislike_goal = False
		# Choose people for the planner problem
		files = []
		for file in os.listdir("personjsons"):
			if file.endswith(".json"):
				files.append(os.path.join("/personjsons", file))

		# TODO: Random number of people to select for character files
		character_files = []
		for step in range(num_people):
			pick_with_equal_probability_no_dupes(files, character_files)

		# Load character jsons into an array
		characters = []
		for i in character_files:
			character_file = "./{}".format(i)
			with open(character_file) as json_data:
				character_data_json = json.load(json_data)
				characters.append(character_data_json)

		# Produce predicate representations for each character
		# (:objects nameA nameB nameC - character)
		problem_character_objects = []
		for person in characters:
			# Append character name to character objects
			# Note: handled first due to the need to check for constants
			# before placing them into predicates
			name = person["first_name"]+"_"+person["last_name"]
			problem_character_objects.append(name)

		# List to store problem initial states
		problem_init = []
		# List to store problem agent intentions
		problem_init_intents = []
		# List to store narrative goals
		problem_goals = []

		# Pre-defined place constants 
		problem_places = ["Starlight-Park", "Sunset-Bistro", "Dawnbreak-Airport", "Hip-Hop-Dance-Studio"]
		# Pre-defined item locations at places
		problem_item_place_locations = ["(item_at flower Starlight-Park)", "(item_at panini Sunset-Bistro)", "(item_at overpriced_food Dawnbreak-Airport)", "(item_at sick_dance_moves_brochure Hip-Hop-Dance-Studio)"]
		for person in characters:
			name = person["first_name"]+"_"+person["last_name"]
			# print(name)

			# Add predicates to problem initial state
			'''
			# Add alive state
			alive = "(alive "+name+")"
			problem_init.append(alive)
			'''

			# Add at state for a random place
			place = problem_places[random.randint(0, len(problem_places)-1)]
			at = "(at "+name+" "+place+")"
			problem_init.append(at)

			# (love_interest A B) A's love interest is B
			if person["love_interest"] != "None":
				split = person["love_interest"].split()
				join = split[0]+"_"+split[1]
				love_interest = "(love_interest "+name+" "+join+")"
				if join in problem_character_objects:
					problem_init.append(love_interest)
					# Create an intent for A to get B to love A and a corresponding goal
					intent = "(intends "+name+" (loves "+join+" "+name+")"+")"
					problem_init_intents.append(intent)
					goal = "(loves "+join+" "+name+")"
					if not loves_goal and (goal_option == "loves" or goal_option == "all"):
						problem_goals.append(goal)
						loves_goal = True
					num_love_interests += 1
			'''	
			# (boss A B) A is the boss of B
			if person["boss"] != "None":
				split = person["boss"].split()
				join = split[0]+"_"+split[1]
				boss = "(boss "+name+" "+join+")"
				if join in problem_character_objects:
					problem_init.append(boss)
			'''
			'''
			# TODO If you want to use occupations they must be pre-defined as constants
			# in the planning file 
			# (occupation A B) A's occupation is B
			if person["occupation"] != "None":
				occupation = "(occupation "+name+" "+person["occupation"]+")"
				problem_init.append(occupation)
			'''
			# (extrovert A) A is a high ranking extrovert
			# Although ToT doesn't do this, if someone isn't a high_e I will force
			# them to be low_e for the sake of having more complete plans
			if person["high_e"]:
				extrovert = "(extrovert "+name+")"
				problem_init.append(extrovert)
			else:	
				# (introvert A) A is an introvert (i.e. low ranking extrovert)
				# if person["low_e"]:
				introvert = "(introvert "+name+")"
				problem_init.append(introvert)
			'''
			# (college_graduate A) A is a college graduate
			college_graduate = "(college_graduate "+name+")"
			problem_init.append(college_graduate)
			'''

			# (best_friend A B) A's best friend is B
			if person["best_friend"] != "None":
				split = person["best_friend"].split()
				join = split[0]+"_"+split[1]
				best_friend = "(best_friend "+name+" "+join+")"
				if join in problem_character_objects:
					problem_init.append(best_friend)

			# (worst_enemy A B) A's worst enemy is B
			if person["worst_enemy"] != "None":
				split = person["worst_enemy"].split()
				join = split[0]+"_"+split[1]
				worst_enemy = "(worst_enemy "+name+" "+join+")"
				if join in problem_character_objects:
					problem_init.append(worst_enemy)
					# Worst enemies intend to get someone a character likes to dislike that character
					enemy = join
					character = name
					# Worst enemy must check if there's someone defined in the problem who they can persuade
					possible_listeners = person["friends"]
					for i in possible_listeners:
						split_i = i.split()
						listener = split_i[0]+"_"+split_i[1]
						if listener in problem_character_objects:
							intends = "(intends "+enemy+" (dislikes "+listener+" "+character+"))"
							problem_init_intents.append(intends)
							num_worst_enemies_with_intent += 1
							if not enemy_persuade_to_dislike_goal and goal_option == "all":
								goal = "(persuadedtodislike "+enemy+")"
								intends = "(intends "+enemy+" (persuadedtodislike "+enemy+"))"
								problem_init_intents.append(intends)
								problem_goals.append(goal)
								enemy_persuade_to_dislike_goal = True


			# (likes A B) for A likes B
			likes = person["friends"]
			for i in likes:
				# Split and rejoin the name of a friend to match
				# the syntax for names above
				split = i.split()
				join = split[0]+"_"+split[1]
				likes_p = "(likes "+name+" "+join+")"
				if join in problem_character_objects:
					problem_init.append(likes_p)
			
			# (dislikes A B) for A dislikes B
			dislikes = person["enemies"]
			for i in dislikes:
				# Split and rejoin the name of an enemy to match 
				# the syntax for names
				split = i.split()
				join = split[0]+"_"+split[1]
				dislikes_p = "(dislikes "+name+" "+join+")"
				if join in problem_character_objects:
					problem_init.append(dislikes_p)
					# Create an intent for B to get A to like B and a corresponding goal
					intends = "(intends "+join+" (likes "+name+" "+join+")"+")"
					problem_init_intents.append(intends)
					
					goal = "(likes "+name+" "+join+")"
					if not likes_goal:
						problem_goals.append(goal)
						likes_goal = True
					num_dislikes += 1
			'''
			# (spouse A B) for A's spouse is B
			spouse = person["spouse"]
			if spouse != "None":
				split = spouse.split()
				join = split[0]+"_"+split[1]
				spouse_p = "(spouse "+name+" "+join+")"
				if join in problem_character_objects:
					problem_init.append(spouse_p)
			'''
		'''
		for p in problem_init:
			print(p)
		for p in problem_init_intents:
			print(p)
		for p in problem_goals:
			print(p)
		'''
		# Append item location predicates to problem_init
		for i in problem_item_place_locations:
			problem_init.append(i)

		# Re-execute problem setup if certain requirements haven't been met
		if num_dislikes >= min_num_dislikes and num_love_interests >= min_num_love_interests and num_worst_enemies_with_intent >= min_num_worst_enemies_with_intent:
			break

	# Write problem to a .pddl file for Glaive
	f = open("tot-problem.pddl", "w")
	# Header
	f.write(";;;\n")
	f.write(";;; Python generated problem description for a narrative based on Talk of the Town\n")
	f.write(";;;\n")
	# Problem definition
	f.write("(define (problem tot)\n")
	f.write("  (:domain tot-domain)\n")
	f.write("  (:objects ")
	for i in problem_character_objects:
		f.write(i+" ")
	f.write("- character\n")
	# Moved item/place constants to tot-domain.pddl
	'''
	f.write("	")
	for i in problem_places:
		f.write(i+" ")
	f.write("- place\n")
	f.write("  	flower panini overpriced_food sick_dance_moves_brochure - item\n")
	f.write("   	programmer - job")
	'''
	f.write(")\n")
	# Problem initialization
	# Predicates
	f.write("  (:init ")
	for i in range(len(problem_init)):
		if i==0:
			f.write(problem_init[i]+"\n")
		else:
			f.write("	 "+problem_init[i]+"\n")	
	# Intents
	for i in range(len(problem_init_intents)):
		if i==len(problem_init_intents)-1:
			f.write("	 "+problem_init_intents[i]+")\n")
		else:
			f.write("	 "+problem_init_intents[i]+"\n")
	# Goal
	if goal_option != "all":
		f.write("  (:goal ")
	else:
		f.write("  (:goal (and ")
	for i in range(len(problem_goals)):
		if i==0:
			f.write(problem_goals[i]+"\n")
		elif i==len(problem_goals)-1:
			f.write("	      "+problem_goals[i])
		else:
			f.write("	      "+problem_goals[i]+"\n")
	if goal_option != "all":
		f.write("))")
	else:
		f.write(")))")
	# Output information
	print("Created a plan with", num_dislikes, "dislikes", num_love_interests, "love interests", num_worst_enemies_with_intent,"worst enemies with intent")

if __name__ == "__main__":
	main()








