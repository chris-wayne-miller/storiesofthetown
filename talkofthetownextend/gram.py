import json
import tracery
from tracery.modifiers import base_english
import numpy
import os

# Helper function #

def pick_with_equal_probability(items):
    individual_probability = 1 / len(items)
    probabilities_array = [individual_probability] * len(items)
    item_chosen = numpy.random.choice(items, p=probabilities_array)
    return item_chosen
    
def pick_with_probability(items_with_probabilities):
    probabilties = []
    items = []
    for item, probability in items_with_probabilities:
        items.append(item)
        probabilties.append(probability)
    item_chosen = numpy.random.choice(items, p=probabilties)
    return item_chosen

def event_occurs(event_probability):
    choice = numpy.random.choice([True, False], p=[event_probability, 1 - event_probability])
    return choice

def getDemoStoryLunchEventProbabilities(high_e, low_e, high_o, low_o, notEnemies):
    # invite_to_lunch_p = 0.7 smile_and_wave_p = 0.2 ignore_p = 0.075 stare_down_p = 0.025
    if notEnemies:
        if high_e and high_o:
            return [0.7, 0.2, 0.075, 0.025]
        if high_e and low_o:
            return [0.5, 0.4, 0.075, 0.025]
        if low_e and high_o:
            return [0.2, 0.7, 0.075, 0.025]
        if low_e and low_o:
            return [0.1, 0.1, 0.75, 0.05]
        # Default return value
        return [0.25, 0.65, 0.05, 0.05]
    else:
        if high_e and high_o:
            return [0.025, 0.075, 0.2, 0.7]
        if high_e and low_o:
            return [0.075, 0.025, 0.2, 0.7]
        if low_e and high_o:
            return [0.025, 0.075, 0.7, 0.2]
        if low_e and low_o:
            return [0.075, 0.025, 0.7, 0.2]
        # Default return value
        return [0.05, 0.05, 0.45, 0.45]

'''
# Currently commented out because Python kept crying about positional argument errors for notEnemies
# The workaround has embedded this logic directly into the conditional for lunch episodes

def getDemoStoryLunchEpisodeProbabilities(high_e, low_e, high_o, low,_o, notEnemies):
    # enjoys_lunch_p = 0.2, know_better_p = 0.5 stares_down_p = 0.05 sits_quietly_p = 0.25
    if notEnemies:
        if high_e and high_o:
            return [0.2, 0.7, 0.075, 0.025]
        if high_e and low_o:
            return [0.6, 0.3, 0.075, 0.025]
        if low_e and high_o:
            return [0.4, 0.3, 0.05, 0.25]
        if low_e and low_o:
            return [0.5, 0.2, 0.05, 0.25]
        # Default return value
        return [0.45, 0.45, 0.05, 0.05]
    else:
        if high_e and high_o:
            return [0.025, 0.075, 0.7, 0.2]
        if high_e and low_o:
            return [0.075, 0.025, 0.2, 0.7]
        if low_e and high_o:
            return [0.025, 0.050, 0.025, 0.9]
        if low_e and low_o:
            return [0.025, 0.025, 0.50, 0.9]
        # Default return value
        return [0.05, 0.05, 0.40, 0.50]
'''

###################

# Preprocess - Tracery Pipeline #

def generate_narrative():
    files = []
    for file in os.listdir("personjsons"):
        if file.endswith(".json"):
            files.append(os.path.join("/personjsons", file))
    # Randomly pick a character and load JSON file for the initial character in the story
    file_picked = pick_with_equal_probability(files)
    character_file = "./{}".format(file_picked)

    with open(character_file) as json_data:
        character_data_json = json.load(json_data)

    # Prints data in JSON in readable format
    # print(json.dumps(character_data_json, indent=4))

    # Data extraction from character to use in story template
    mcFullname = character_data_json["full_name"]
    mcFirstname = character_data_json["first_name"]
    mcKids = character_data_json["kids"]

    mcCoworkers = character_data_json["coworkers"]
    mcFriends = character_data_json["friends"]
    mcEnemies = character_data_json["enemies"]
    mcSpouse = character_data_json["spouse"]

    mcCompany = character_data_json["company"]
    mcOccupation = character_data_json["occupation"]
    
    mcHighExtroversion = character_data_json["high_e"]
    mcLowExtroversion = character_data_json["low_e"]
    
    mcHighOpentoExperience = character_data_json["high_o"]
    mcLowOpentoExperience = character_data_json["low_o"]
    
    ### TEMPORARY FIX FOR MISSING DATA ###
    if not mcCoworkers:
        return "No coworkers."
    
    # Derive more knowledge about relationship with coworkers
    mcFriendlyCoworkers = []
    mcEnemyCoworkers = []
    mcNeutralCoworkers = []
    for c in mcCoworkers:
        if c in mcFriends:
            mcFriendlyCoworkers.append(c)
    #         print(c, "Friendly Worker")
        elif c in mcEnemies:
            mcEnemyCoworkers.append(c)
    #         print(c, "Enemy Worker")
        else:
            mcNeutralCoworkers.append(c)
    #         print(c, "Neutral Worker")


    # Story branching based on randomisation or previously engineered knowledge in story graph

    # Demo Story graph 1

    # 0) Choose probabilities for certain events:

    late_probability = 0.3
    traffic_probability = 0.3 
    run_into_coworker_probability = 0.7

    
    
    # 1) Create Intro
    # Choose intro based on whether mc has kids
    if mcKids:
        intro = "#mainCharacterFullname# wakes up and feeds their kids. After taking care of the kids, #mainCharacter# #morningActivity#."
    else:
        s = mcFullname
        intro = "#mainCharacterFullname# wakes up and #morningActivity#."

    # Add Weather description to intro
    intro += "#weatherDescription#"

    # Add character description to intro
    intro += "#mainCharacterDescription#"

    intro += "#mainCharacter# gets ready for work."

    # Randomize whether mc is late for work and let mc leave for work
    if event_occurs(late_probability):
        intro += "#mainCharacter# realizes they are late for work. They rush to #mcCompany# where they work as a #mcOccupation#."
    else:
        intro += "#mainCharacter# looks at the clock and realizes they are on time for work."
        if mcSpouse != "None":
            intro += "#mainCharacter# says goodbye to their spouse, #mcSpouse#."
        if mcKids:
            intro += "#mainCharacter# says goodbye to their kids."
        intro += "#mainCharacter# heads out the door to go to #mcCompany# where they work as a #mcOccupation#."

    # Simulate traffic
    if event_occurs(traffic_probability):
        intro += "#mainCharacter# arrives to work late"
    else:
        intro += "#mainCharacter# arrives to work on time."

    episode = "#mainCharacter# works for a few hours and then takes a lunch break."


    # Probabilities could be based on personality traits
    if event_occurs(run_into_coworker_probability):
        coworker = pick_with_equal_probability(mcCoworkers)
        if coworker in mcFriendlyCoworkers:
            demo_lunch_p = getDemoStoryLunchEventProbabilities(mcHighExtroversion, mcLowExtroversion, mcHighOpentoExperience, mcLowOpentoExperience, True)
        elif coworker in mcEnemyCoworkers:
            demo_lunch_p = getDemoStoryLunchEventProbabilities(mcHighExtroversion, mcLowExtroversion, mcHighOpentoExperience, mcLowOpentoExperience, False)
        else:
            demo_lunch_p = getDemoStoryLunchEventProbabilities(mcHighExtroversion, mcLowExtroversion, mcHighOpentoExperience, mcLowOpentoExperience, True)

        print(mcFullname)
        print(demo_lunch_p)
        invite_to_lunch_p = demo_lunch_p[0]
        smile_and_wave_p = demo_lunch_p[1]
        ignore_p = demo_lunch_p[2]
        stare_down_p = demo_lunch_p[3]
            
        invite_episode = "#mainCharacter# invites {} to lunch.".format(coworker)
        smile_episode = "#mainCharacter# smiles and waves at {}.".format(coworker)
        ignore_episode = "#mainCharacter# ignores {} and walks past them.".format(coworker)
        stares_down_episode = "#mainCharacter# stares {} down.".format(coworker)

        episode_chosen = pick_with_probability([(invite_episode, invite_to_lunch_p), (smile_episode, smile_and_wave_p), (ignore_episode, ignore_p), (stares_down_episode, stare_down_p)])
        episode += episode_chosen
        
        if episode_chosen == invite_episode:
            if coworker in mcFriendlyCoworkers:
                notEnemies = True
            elif coworker in mcEnemyCoworkers:
                notEnemies = False
            else:
                notEnemies = True
                
            high_e = mcHighExtroversion
            low_e = mcLowExtroversion
            high_o = mcHighOpentoExperience
            low_o = mcLowOpentoExperience
            
            if notEnemies:
                if high_e and high_o:
                    demo_lunch_episode_p = [0.2, 0.7, 0.075, 0.025]
                elif high_e and low_o:
                    demo_lunch_episode_p = [0.6, 0.3, 0.075, 0.025]
                elif low_e and high_o:
                    demo_lunch_episode_p = [0.4, 0.3, 0.05, 0.25]
                elif low_e and low_o:
                    demo_lunch_episode_p = [0.5, 0.2, 0.05, 0.25]
                else:
                    # Default
                    demo_lunch_episode_p = [0.45, 0.45, 0.05, 0.05]
            else:
                if high_e and high_o:
                    demo_lunch_episode_p = [0.025, 0.075, 0.7, 0.2]
                elif high_e and low_o:
                    demo_lunch_episode_p = [0.075, 0.025, 0.2, 0.7]
                elif low_e and high_o:
                    demo_lunch_episode_p = [0.025, 0.050, 0.025, 0.9]
                elif low_e and low_o:
                    demo_lunch_episode_p = [0.025, 0.025, 0.50, 0.9]
                else:
                    # Default
                    demo_lunch_episode_p = [0.05, 0.05, 0.40, 0.50]

            #demo_lunch_episode_p = getDemoStoryLunchEpisodeProbabilities(mcHighExtroversion, mcLowExtroversion, mcHighOpentoExperience, mcLowOpentoExperience, True)
            print(demo_lunch_episode_p)
            enjoys_lunch_p = demo_lunch_episode_p[0]
            know_better_p = demo_lunch_episode_p[1]
            stares_down_p = demo_lunch_episode_p[2]
            sits_quietly_p = demo_lunch_episode_p[3]

            enjoys_lunch_episode = "#mainCharacter# enjoys lunch with {}.".format(coworker)
            know_better_episode = "#mainCharacter# talks to {} and gets to know them better.".format(coworker)
            stares_down_episode = "#mainCharacter# stares {} down during the entire lunch.".format(coworker)
            sits_quietly_episode = "#mainCharacter# sits quietly through the entire lunch."

            episode_chosen = pick_with_probability([(enjoys_lunch_episode, enjoys_lunch_p), (know_better_episode, know_better_p), (sits_quietly_episode, sits_quietly_p), (stares_down_episode, stares_down_p)])
            episode += episode_chosen
        else:
#             print(episode_chosen, invite_episode, type(episode_chosen), type(invite_episode),episode_chosen is invite_episode)
            episode += "#mainCharacter# proceeds to get lunch on their own."

    conclusion = "#mainCharacter# returns back home and finshes up their day."
        
    # Grammar creation
    characters = mcFriends + mcEnemies
    character_adjectives = ["a happy", "a jolly", "a kind", "an antisocial", "a reclusive"]
    morning_activities = ["brushes their teeth", "picks up the newspaper from the front door", "pours themself a cup of coffee", "makes breakfast"]
    weathers = ["rainy", "sunny", "cloudy", "warm", "cold", "hot", "freezing"]
    news_sources = ["TV", "newspaper", "weather forecast"]
    activities = ["said hey", "ignored #mainCharacter#", "greeted #mainCharacter#", "threatened #mainCharacter#", "asked #mainCharacter# out for lunch"]
    relationships = ["friends", "foes", "partners", "rivals", "strangers", "colleagues", "siblings"]
    occupation_workplace = [("Barber", "Hair Salon"), ("Mechanic", "Garage"), ("Accountant", "Bank"), ("Professor", "College"), ("Chef", "Restaurant")]
    rules_us = {
      "origin": ["#intro# #episode# #conclusion#"],
      "mainCharacter": [mcFirstname],
      "mainCharacterFullname" : [mcFullname],
      "mcSpouse" : mcSpouse,
      "mcCompany": mcCompany,
      "mcOccupation" : mcOccupation,
      "mcKids" : mcKids,
      "mcCoworkers": mcCoworkers,
      "character": characters,
      "intro": [intro],
      "mainCharacterDescription": ["#mainCharacter# is #adjective# person."],
      "adjective" : character_adjectives,
      "morningActivity" : morning_activities,
      "weatherDescription" :["The #newsSource# predicted that it's going to be #weather# today."],
      "weather" : weathers,
      "newsSource" : news_sources,
      "episode": [episode],
      "conclusion" : [conclusion]
    }

    grammar = tracery.Grammar(rules_us)
    grammar.add_modifiers(base_english)
    generated_narrative = grammar.flatten("#origin#")
    if generated_narrative is None:
        print(json.dumps(character_data_json, indent=4))
    return generated_narrative

with open("sample_generation.txt", "w") as sample_file:
    for i in range(193):
        print("Narrative {}:". format(i+1))
        generated_narrative = generate_narrative()
        print(generated_narrative)
        sample_file.write("Narrative {}:\n". format(i+1))
        sample_file.write(generated_narrative + "\n")
