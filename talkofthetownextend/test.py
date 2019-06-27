import sys
import os
import shutil
import time
import subprocess			# for command line calls for tracery
import json
from simulation import Simulation


# Generate a town! Oh boy
start_time = time.time()
sim = Simulation()  # Objects of the class Simulation are Talk of the Town simulations
# Simulate from the date specified as the start of town generation to the date specified
# as its terminus; both of these dates can be set in config/basic_config.py
try:
    sim.establish_setting()  # This is the worldgen procedure; it will simulate until the date specified in basic_config.py
    town = sim.town
except KeyboardInterrupt:  # Enter "ctrl+C" (a keyboard interrupt) to end worldgen early
    # In the case of keyboard interrupt, we need to tie up a few loose ends
    sys.stdout.write('\r{}'.format(' ' * 94))  # Clear out the last sampled event written to stdout
    sys.stdout.write('\rWrapping up...')
    sim.advance_time()
    for person in list(sim.town.residents):
        person.routine.enact()

# START HANDLING FOR EXTEND #
# Town generation was successful, so print out some basic info about the town
print "\nAfter {time_elapsed}s, town generation was successful!".format(
    time_elapsed=int(time.time()-start_time)
)

def createSymbolicEventLists(dictionary, events):
	# Events relevant for marriage-divorce story
	dictionary.update({"MDString": []})
	for e in list(events):
		s = str(e)
		if "Marriage" in s:
			dictionary["MDString"].append("M")
		if "Divorce" in s:
			dictionary["MDString"].append("D")
		if "Hiring" in s:
			dictionary["MDString"].append("H")
		if "Laying off" in s:
			dictionary["MDString"].append("L")

# Printing relevant information
print "*** Residents ***"
# Pre-emptively clear the json file folder before exporting jsons
try:
	shutil.rmtree("./personjsons")
except OSError as e:
	print "Error"
# Iterate through residents and export json files
for person in list(sim.town.residents):
	personDict = {}
	# Add person's name to the dictionary (full, first, last)
	personDict.update({"full_name": person.name})
	personDict.update({"first_name": person.first_name})
	personDict.update({"last_name": person.last_name})
	# Add person's spouse to the dictionary
	if person.spouse != None:
		personDict.update({"spouse": person.spouse.name})
	else:
		personDict.update({"spouse": "None"})
	# Add person's occupation to the dictionary
	if person.occupation != None:
		personDict.update({"occupation": person.occupation.vocation})
		personDict.update({"company": person.occupation.company.name})
	else:
		personDict.update({"occupation": "None"})
		personDict.update({"company": "None"})
	# Add person's love interest to the dictionary
	if person.love_interest != None:
		personDict.update({"love_interest": person.love_interest.name})
	else:
		personDict.update({"love_interest": "None"})
	# Add person's boss to the dictionary
	if person.boss != None:
		personDict.update({"boss": person.boss.name})
	else:
		personDict.update({"boss": "None"})
	# Add if person is a college graduate
	personDict.update({"college_graduate": person.college_graduate})
	# Add a person's best friend
	if person.best_friend != None:
		personDict.update({"best_friend": person.best_friend.name})
	else:
		personDict.update({"best_friend": "None"})
	# Add a person's worst enemy
	if person.worst_enemy != None:
		personDict.update({"worst_enemy": person.worst_enemy.name})
	else:
		personDict.update({"worst_enemy": "None"})
	
	
	'''
	# Add the person's life events to the dictionary as separate, identifiable events
	marriageCount = 1
	divorceCount = 1
	hiringCount = 1
	layOffCount = 1
	for e in list(person.life_events):
		s = str(e)
		if "Marriage" in s:
			personDict.update({"marriage"+`marriageCount`: s})
			marriageCount += 1
		if "Divorce" in s:
			personDict.update({"divorce"+`divorceCount`: s})
			divorceCount += 1
		if "Hiring" in s:
			personDict.update({"hiring"+`hiringCount`: s})
			hiringCount += 1
		if "Laying off" in s:
			personDict.update({"laying_off"+`layOffCount`: s})
			layOffCount += 1
	# Add the person's life events in sequential order
	personDict.update({"seq_life_events": []})
	for e in list(person.life_events):
		personDict["seq_life_events"].append(str(e))
	# Create symbolic event lists
	createSymbolicEventLists(personDict, person.life_events)
	'''
	# Add some personality information to the dictionary
	personDict.update({"high_e":person.personality.high_e})
	personDict.update({"low_e":person.personality.low_e})
	personDict.update({"high_o":person.personality.high_o})
	personDict.update({"low_o":person.personality.low_o})
	# Add the person's kids to the dictionary
	personDict.update({"kids": []})
	for p in list(person.kids):
		personDict["kids"].append(p.name)
	# Add the person's enemies to the dictionary
	personDict.update({"enemies": []})
	for p in list(person.enemies):
		personDict["enemies"].append(p.name)
	# Add the person's friends to the dictionary
	# Do not add enemies to the friends list in the event they show up
	personDict.update({"friends": []})
	for p in list(person.friends):
		if p not in list(person.enemies):
			personDict['friends'].append(p.name)
	# Add the person's coworkers to the dictionary
	personDict.update({"coworkers": []})
	for p in list(person.coworkers):
		personDict['coworkers'].append(p.name)
	# Export the dictionary for that person as a JSON file
	filename = "./personjsons/"+person.first_name+person.last_name+".json"
	dirname = os.path.dirname(filename)
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	with open(filename, 'w') as fp:
		json.dump(personDict, fp)

# Print out the town, population, and date
print "\nIt is now the {date}, in the town of {town}, pop. {population}.\n".format(
    date=sim.date[0].lower() + sim.date[1:],
    town=sim.town.name,
    population=sim.town.population
)
# Start excavating nuggets of dramatic intrigue from the raw emergent material produced
# during the simulation of the town's history
print "Excavating nuggets of dramatic intrigue..."
sim.story_recognizer.excavate()
# Save all this material to global variables, for convenience
unrequited_love_cases = sim.story_recognizer.unrequited_love_cases
love_triangles = sim.story_recognizer.love_triangles
extramarital_romantic_interests = sim.story_recognizer.extramarital_romantic_interests
asymmetric_friendships = sim.story_recognizer.asymmetric_friendships
misanthropes = sim.story_recognizer.misanthropes
sibling_rivalries = sim.story_recognizer.sibling_rivalries
business_owner_rivalries = sim.story_recognizer.business_owner_rivalries



# To simulate ahead in time, simply use the 'Simulation.simulate()' method (given
# that we binded a Simulation object to the variable 'sim' above, you can call this
# using sim.simulate()'), which takes the number of timesteps as its argument. There's 
# two timesteps for each day (one for daytime, one for nighttime), so Simulation.simulate(730) 
# will simulate one year, and so forth.

# To retrieve a person (i.e., the Python object in memory that represents them) by
# their name, use the command Simulation.find_person(string_of_their_full_name), e.g.,
# Simulation.find('James Ryan').

# Here's some other quick commands that you can use to explore your generated town.

def outline_businesses():
    """Outline all the businesses, past and present, in this town."""
    print '\nFormer businesses in {town}:'.format(town=sim.town.name)
    for c in sim.town.former_companies:
        print '\t{}'.format(c)
    print '\nCurrent businesses in {town}:'.format(town=sim.town.name)
    for c in sim.town.companies:
        print '\t{}'.format(c)


def outline_character_locations():
    """Outline the locations in town, and who is currently at each one."""
    for location in sim.town.companies|sim.town.dwelling_places:
        print location
        if not location.people_here_now:
            print '\tno one here'
        else:
            for character in location.people_here_now:
                if character.routine.working:
                    print "\t{} (working as {})".format(character, character.routine.occasion, character.occupation.vocation)
                else:
                    print "\t{} ({})".format(character, character.routine.occasion)


def outline_gravestones():
    """Print out all the gravestones in the town."""
    for d in sim.town.deceased:
        print d.gravestone.description


def outline_character_social_network(person):
    """Print out a character's relationships to everyone else in the town."""
    for resident in sim.town.residents:
        print person.relation_to_me(resident)


def outline_relationship(person, other_person):
    """Outline the unidirectional relationships between these two."""
    if other_person not in person.relationships:
        print None
    else:
        print "\t{}'s relationship toward {}:".format(person, other_person)
        print person.relationships[other_person].outline()
        print '\n'
        print "\t{}'s relationship toward {}:".format(other_person, person)
        print other_person.relationships[person].outline()

def list_attributes(entity):
	"""Print out a list of attributes that an entity has.

	This will specifically print out a list of attributes that the object passed for
	the 'entity' argument has. You can then see what values are held in these attributes by
	using simple dot-notation commands. For instance, if a person has the attribute 'neighbors',
	you can see what's held in that attribute by using a command like 'print entity.neighbors'.

	The listing of attributes won't give an exhuastive account of the kinds of data that are
	stored for most entities, since some attributes will hold objects that themselves have
	attributes. For example, 'person.face' will hold a Face object, which itself will have 
	attributes holding objects pertaining to components of the face. Generally, though, the 
	listing	produced by this function should give you a good idea of some of the kinds of data 
	that are stored (some of which may be narratively potent).

	Additionally, any attributes that are computed dynamically (by using Python @property
	decorators) won't show up. Here's a current list of those kinds of attributes for Person
	objects:
		age_and_gender_description
		basic_appearance_description
		boss
		dead
		description
		first_home
		full_name
		full_name_without_suffix
		honorific
		is_captivated_by
		kids_at_home
		life_events
		name
		nametag
		next_of_kin
		nuclear_family
		object_pronoun
		possessive_pronoun
		present
		queer
		reflexive_pronoun
		requited_love_interest
		subject_pronoun
		year_i_moved_here
		years_i_lived_here
	"""
	for attribute in sorted(vars(entity).keys()):  # Prints them out in alphabetical order
		print attribute


def outline_physical_description(person):
	"""Outline a person's physical description."""
	print person.description


def outline_personality(person):
	"""Outline a person's physical description."""
	str = "\nFive-factor personality model of {}:\n\n".format(person.name)
	str += "\tOpenness: {}{}\n".format(
		person.personality.component_str('o'),
		'' if not person.personality.o.inherited_from else 
		' (takes after {})'.format(person.personality.o.inherited_from.name)
	)
	str += "\tConscientiousness: {}{}\n".format(
		person.personality.component_str('c'),
		'' if not person.personality.c.inherited_from else 
		' (takes after {})'.format(person.personality.c.inherited_from.name)
	)
	str += "\tExtroversion: {}{}\n".format(
		person.personality.component_str('e'),
		'' if not person.personality.e.inherited_from else 
		' (takes after {})'.format(person.personality.e.inherited_from.name)
	)
	str += "\tAgreeableness: {}{}\n".format(
		person.personality.component_str('a'),
		'' if not person.personality.a.inherited_from else 
		' (takes after {})'.format(person.personality.a.inherited_from.name)
	)
	str += "\tNeuroticism: {}{}\n".format(
		person.personality.component_str('n'),
		'' if not person.personality.n.inherited_from else 
		' (takes after {})'.format(person.personality.n.inherited_from.name)
	)
	print str


def outline_love_life(person):
	"""Outline a person's love life, including their strongest love interest and anyone else they are
	very interested in romantically.
	"""
	spouse = person.spouse
	other_love_interests = sorted(person.is_captivated_by, key=lambda li: person.relationships[li].spark, reverse=True)
	if spouse in other_love_interests:
		other_love_interests.remove(spouse)
	str = "\nRomantic life of {}:\n\n".format(person.name)
	if person.spouse:
		str += "\tSpouse: {name} ({person_spark_for_them} {heart_emoji} {their_spark_for_person})\n".format(
			name=spouse.name,
			person_spark_for_them=person.relationships[person.spouse].spark,
			heart_emoji='\xe2\x9d\xa4',
			their_spark_for_person=person.spouse.relationships[person].spark
		)
	else:
		str += "\tSpouse: none\n"
	if other_love_interests:
		str += "\tOther love interests: {}\n".format(
			', '.join('{name} ({person_spark_for_them} {heart_emoji} {their_spark_for_person})'.format(
				name=other_love_interest.name,
				person_spark_for_them=person.relationships[other_love_interest].spark,
				heart_emoji='\xe2\x9d\xa4',
				their_spark_for_person=other_love_interest.relationships[person].spark
			) for other_love_interest in other_love_interests)
		)
	else:
		str += "\tOther love interests: none\n"
	print str


def outline_family(person):
	"""Outline a person's family members."""
	str = "\nFamily of {}:\n".format(person.name)
	str += "\tSpouse: {}\n".format(person.spouse.name if person.spouse else 'none')
	str += "\tChildren: {}\n".format(', '.join(x.name for x in person.kids) if person.kids else 'none')
	str += "\tGrandchildren: {}\n".format(', '.join(x.name for x in person.grandchildren) if person.grandchildren else 'none')
	str += "\tGrandchildren: {}\n".format(', '.join(x.name for x in person.greatgrandchildren) if person.greatgrandchildren else 'none')
	str += "\tParents: {}\n".format(', '.join(x.name for x in person.parents) if person.parents else 'none')
	str += "\tBrothers: {}\n".format(', '.join(x.name for x in person.brothers) if person.brothers else 'none')
	str += "\tSisters: {}\n".format(', '.join(x.name for x in person.sisters) if person.sisters else 'none')
	str += "\tGrandparents: {}\n".format(', '.join(x.name for x in person.grandparents) if person.grandparents else 'none')
	str += "\tGreatgrandparents: {}\n".format(', '.join(x.name for x in person.greatgrandparents) if person.greatgrandparents else 'none')
	str += "\tAunts: {}\n".format(', '.join(x.name for x in person.aunts) if person.aunts else 'none')
	str += "\tUncles: {}\n".format(', '.join(x.name for x in person.uncles) if person.uncles else 'none')
	str += "\tNieces: {}\n".format(', '.join(x.name for x in person.nieces) if person.nieces else 'none')
	str += "\tNephews: {}\n".format(', '.join(x.name for x in person.nephews) if person.nephews else 'none')
	str += "\tCousins: {}\n".format(', '.join(x.name for x in person.cousins) if person.cousins else 'none')
	print str


def list_ancestors(person):
	"""List all of a person's ancestors."""
	for ancestor in person.ancestors:
			print ancestor


def list_work_history(person):
	"""List out a person's occupational history."""
	for o in person.occupations:
			print o
        
