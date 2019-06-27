import json
import tracery
from tracery.modifiers import base_english

# Preprocess - Tracery Pipeline #

debug = True

# Load JSON file for the initial character in the story
rootchar = "./personjsons/ArleneAllington.json"
global rootjson

with open(rootchar) as json_data:
	rootjson = json.load(json_data)

if debug:
	print(rootjson)
	print("**********")

# Tracery Rules

mcfullname = [rootjson["full_name"]]
mcfirstname = [rootjson["first_name"]]
kids = [rootjson["kids"]]

if kids!=[[]]:
	s = ''.join(mcfullname)
	intro = [s+" wakes up and feeds their kids. After taking care of the kids #mainCharacter# #morningActivity#"]
else:
	s = ''.join(mcfullname)
	intro = ["#mainCharacter# wakes up and #morningActivity#"]

new_rules_us = {
 "origin": ["[mainCharacter:#character#] #intro#"],
 "character": mcfullname,
 "intro": intro,
 "morningActivity": ["brushes their teeth", "picks up the newspaper from the front door", "pours themself a cup of coffee"]
}

'''
characters = [rootjson["name"]]
occupation = [rootjson["occupation"]]
workplace = [rootjson["company"]]
coworkers = [rootjson["coworkers"]]
friends = [rootjson["friends"]]
enemies = [rootjson["enemies"]]

rules_us = {
  "origin": ["[mainCharacter:#character#] #intro# #conclusion#"],
  "character": characters,
  "intro": ["#mainCharacter# wakes up and #morningActivity#. #weatherDescription# #mainCharacterDescription#"],
  "mainCharacterDescription": ["#mainCharacter# is #adjective# person."],
  "adjective" : ["a happy", "a jolly", "a kind", "an antisocial", "a reclusive"],
  "morningActivity" :["brushes their teeth", "picks up the newspaper from the front door", "pours himself a cup of coffee"],
  "weatherDescription" :["The #newsSource# predicted that it's going to be #weather# today."],
  "weather" : ["rainy", "sunny", "cloudy", "warm", "cold", "hot", "freezing"],
  "newsSource" :["TV", "newspaper", "weather forecast"],
  "conclusion" : ["conclusion"],
  "event" : ["event"]
}
'''

grammar = tracery.Grammar(new_rules_us)
grammar.add_modifiers(base_english)
print(grammar.flatten("#origin#"))
