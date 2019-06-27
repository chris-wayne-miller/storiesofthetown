import re
import sys
import numpy
import json

variant_high_e = [0.6, 0.3, 0.1]
variant_mid_e = [0.3, 0.6, 0.1]
variant_low_e = [0.1, 0.3, 0.6]
variant_d = [0.4, 0.4, 0.2]

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

def parse_pcfg(productions, start="origin"):
    # Probabilistically choose a production
    choice =  pick_with_probability(productions[start])
    # Search for all nonterminals within that production
    syntax_pattern = re.compile("#([a-zA-Z0-9]*)#")
    nonterminals = re.findall(syntax_pattern, choice)
    expansions = []
    # Recursively expand each nonterminal
    for nonterminal in nonterminals:
        if nonterminal in productions:
            expansions.append( (nonterminal, parse_pcfg(productions, start=nonterminal)) )
        else:
            print("Nonterminal {} not in productions".format(nonterminal))
    # Replace the tags with their expansions in the original string
    for nonterminal, expansion in expansions:
        choice = choice.replace("#" + nonterminal + "#", expansion, 1)
    return choice

def pluralize(verb):
    return verb + "s"

def remove_delimeter(word, delimeter="_"):
    return " ".join(word.split(delimeter))

def fetch_json(word, delimeter="_"):
    json_prefix = "".join(word.split(delimeter))
    path = "./personjsons/" + json_prefix + ".json"
    with open(path) as json_file:
        data = json.load(json_file)
        return data

def text_for_action(verb, predicates):
    if verb == "travel":
        subject = remove_delimeter(predicates[0])
        source = remove_delimeter(predicates[1] , delimeter="-")
        destination = remove_delimeter(predicates[2], delimeter="-")
        variant_probability = [0.3, 0.4, 0.3]
        variant1 = "{} traveled from {} to {}".format(subject, source, destination)
        variant2 = "{} was in {} and went to {}".format(subject, source, destination)
        variant3 = "{} went to {} from {}".format(subject, destination, source)
        travel_grammar = {
            "origin": [(variant1, variant_probability[0]),
                       (variant2 , variant_probability[1]), 
                       (variant3 , variant_probability[2])           
            ]
        }
        sentence = parse_pcfg(travel_grammar)
    elif verb == "retrieve":
        subject = remove_delimeter(predicates[0])
        obj = remove_delimeter(predicates[1])
        variant_probability = [0.3, 0.4, 0.3]
        variant1 = "{} picked up a {}".format(subject, obj)
        variant2 = "{} picked up a {} from the ground".format(subject, obj)
        variant3 = "A {} was lying on the ground. {} picked it up".format(obj, subject)
        pickup_grammar = {
            "origin": [(variant1, variant_probability[0]),
                       (variant2 , variant_probability[1]), 
                       (variant3 , variant_probability[2])           
            ]
        }
        sentence = parse_pcfg(pickup_grammar)
    elif verb == "vigorousdance":
        subject = remove_delimeter(predicates[0])
        subject_json_data = fetch_json(predicates[0])
        if(subject_json_data["high_o"] and subject_json_data["high_e"]):
            variant_probability = variant_high_e
        elif(subject_json_data["high_o"] and subject_json_data["low_e"]):
            variant_probability = variant_mid_e
        elif(subject_json_data["low_o"] and subject_json_data["low_e"]):
            variant_probability = variant_low_e
        else:
            variant_probability = variant_d
        '''
        print("high_o:", subject_json_data["high_o"])
        print("high_e:", subject_json_data["high_e"])
        print("low_e:", subject_json_data["low_e"])
        print(variant_probability)
        '''
        variant1 = "{} figured that the best way to boost their confidence would be try out some of the dance moves in the dance moves brochure.  {} spent several minutes learning the dance moves to the best of their ability.  {} is now brimming with confidence!".format(subject, subject, subject)
        variant2 = "{} took a peek at the dance moves in the dance moves brochure.  {} was a little embarassed at the idea of practing the dance moves but figured it was worth a shot.  After practing the moves, {} feels more confident!".format(subject, subject, subject)
        variant3 = "{} took a quick look at the dance moves brochure.  They reluctantly concluded that the fastest way for them to become more confident would be to practice the moves in the brochure.  {} feels kind of confident now.".format(subject, subject)
        dance_grammar = {
            "origin": [(variant1, variant_probability[0]),
                       (variant2 , variant_probability[1]), 
                       (variant3 , variant_probability[2])           
            ]
        }
        sentence = parse_pcfg(dance_grammar)
    elif verb == "give":
        # setup subject PCFG
        subject = remove_delimeter(predicates[0])
        subject_json_data = fetch_json(predicates[0])
        if(subject_json_data["high_o"] and subject_json_data["high_e"]):
            variant_probability = variant_high_e
        elif(subject_json_data["high_o"] and subject_json_data["low_e"]):
            variant_probability = variant_mid_e
        elif(subject_json_data["low_o"] and subject_json_data["low_e"]):
            variant_probability = variant_low_e
        else:
            variant_probability = variant_d
        '''
        print("high_o:", subject_json_data["high_o"])
        print("high_e:", subject_json_data["high_e"])
        print("low_e:", subject_json_data["low_e"])
        print(variant_probability)
        '''
        obj = remove_delimeter(predicates[2])
        # setup receiver PCFG
        receiver = remove_delimeter(predicates[1])
        receiver_json_data = fetch_json(predicates[1])
        if(receiver_json_data["high_o"] and receiver_json_data["high_e"]):
            receiver_variant_probability = variant_high_e
        elif(receiver_json_data["high_o"] and receiver_json_data["low_e"]):
            receiver_variant_probability = variant_mid_e
        elif(receiver_json_data["low_o"] and receiver_json_data["low_e"]):
            receiver_variant_probability = variant_low_e
        else:
            receiver_variant_probability = variant_d
        '''
        print("receiver_high_o:", receiver_json_data["high_o"])
        print("receiver_high_e:", receiver_json_data["high_e"])
        print("receiver_low_e:", receiver_json_data["low_e"])
        print(receiver_variant_probability)
        '''
        # expand subject PCFG
        subject_variant1 = "{} cheerfully greeted {}.  {} gave {} the {} they obtained.".format(subject, receiver, subject, receiver, obj)
        subject_variant2 = "{} gave {} the {} they had on them.".format(subject, receiver, obj)
        subject_variant3 = "{} shyly gave their {} to {}".format(subject, obj, receiver)
        give_grammar = {
            "origin": [(subject_variant1, variant_probability[0]),
                       (subject_variant2 , variant_probability[1]), 
                       (subject_variant3 , variant_probability[2])           
            ]
        }
        sentence = parse_pcfg(give_grammar)
        # expand receiver PCFG
        receiver_variant1 = "{} happily accepted {}'s gift.  {} now likes {}!".format(receiver, subject, receiver, subject)
        receiver_variant2 = "{} was a tad surprised but offered to accept {}'s sudden gift.  {} feels like they know {} a little better now.".format(receiver, subject, receiver, subject)
        receiver_variant3 = "{} awkwardly accepted {}'s gift.  However, {} still appreciated the nice gesture.".format(receiver, subject, receiver)
        give_grammar = {
            "origin": [(receiver_variant1, receiver_variant_probability[0]),
                       (receiver_variant2 , receiver_variant_probability[1]), 
                       (receiver_variant3 , receiver_variant_probability[2])           
            ]
        }
        # combine the subject-expanded sentence with the receiver-expanded sentence
        sentence = sentence + "  " + parse_pcfg(give_grammar)
    elif verb == "flirt":
        subject = remove_delimeter(predicates[0])
        subject_json_data = fetch_json(predicates[0])
        if(subject_json_data["high_o"] and subject_json_data["high_e"]):
            variant_probability = variant_high_e
        elif(subject_json_data["high_o"] and subject_json_data["low_e"]):
            variant_probability = variant_mid_e
        elif(subject_json_data["low_o"] and subject_json_data["low_e"]):
            variant_probability = variant_low_e
        else:
            variant_probability = variant_d
        '''
        print("high_o:", subject_json_data["high_o"])
        print("high_e:", subject_json_data["high_e"])
        print("low_e:", subject_json_data["low_e"])
        print(variant_probability)
        '''
        obj = remove_delimeter(predicates[2])
        # setup receiver PCFG
        receiver = remove_delimeter(predicates[1])
        receiver_json_data = fetch_json(predicates[1])
        if(receiver_json_data["high_o"] and receiver_json_data["high_e"]):
            receiver_variant_probability = variant_high_e
        elif(receiver_json_data["high_o"] and receiver_json_data["low_e"]):
            receiver_variant_probability = variant_mid_e
        elif(receiver_json_data["low_o"] and receiver_json_data["low_e"]):
            receiver_variant_probability = variant_low_e
        else:
            receiver_variant_probability = variant_d
        '''
        print("receiver_high_o:", receiver_json_data["high_o"])
        print("receiver_high_e:", receiver_json_data["high_e"])
        print("receiver_low_e:", receiver_json_data["low_e"])
        print(receiver_variant_probability)
        '''
        # expand subject PCFG
        location = remove_delimeter(predicates[2])
        subject_variant1 = "{} used their newfound confidence to flirt with {} at {}.  {} told a series of funny jokes and showed off their new dance moves with lots of flair!".format(subject, receiver, location, subject)
        subject_variant2 = "At {}, {} encountered {}.  Seizing the opportunity, {} decided to use their renewed sense of confidence to flirt with {}.".format(location, subject, receiver, subject, receiver)
        subject_variant3 = "{} noticed that {} was at {} as well.  {} mustered their newfound confidence to try to flirt with {} to the best of their ability.".format(subject, receiver, location, subject, receiver)
        flirt_grammar = {
            "origin": [(subject_variant1, variant_probability[0]),
                       (subject_variant2 , variant_probability[1]), 
                       (subject_variant3 , variant_probability[2])           
            ]
        }
        sentence = parse_pcfg(flirt_grammar)
        # expand receiver PCFG
        receiver_variant1 = "{} was really impressed by {}'s air of confidence.  {} is now smitten with {}!".format(receiver, subject, receiver, subject)
        receiver_variant2 = "{} was rather impressed by {}'s attempt at flirting.  {} likes {} a lot more now.".format(receiver, subject, receiver, subject)
        receiver_variant3 = "{} was initially taken aback by {}'s attempt at flirting.  After a lot of reflection on what just happened, {} decided to take a chance on {}.".format(receiver, subject, receiver, subject)
        flirt_grammar = {
            "origin": [(receiver_variant1, receiver_variant_probability[0]),
                       (receiver_variant2 , receiver_variant_probability[1]), 
                       (receiver_variant3 , receiver_variant_probability[2])           
            ]
        }
        sentence = sentence + "  " + parse_pcfg(flirt_grammar)
    elif verb == "persuadetodislike":
        persuader = remove_delimeter(predicates[0])
        persuaded = remove_delimeter(predicates[1])
        other = remove_delimeter(predicates[2])
        location = remove_delimeter(predicates[3], delimeter="-")
        variant_probability = [0.3, 0.4, 0.3]
        variant1 = "{} persuades {} to dislike {} at {} by spreading nasty rumors".format(persuader, persuaded, other, location)
        variant2 = "At {}, {} persuades {} to dislike {}".format(location, persuader, persuaded, other)
        variant3 = "{} meets {} at {} and persuades them to dislike {} through nasty rumors".format(persuader, persuaded, location, other)
        dislike_grammar = {
            "origin": [(variant1, variant_probability[0]),
                       (variant2 , variant_probability[1]), 
                       (variant3 , variant_probability[2])           
            ]
        }
        sentence = parse_pcfg(dislike_grammar)
    elif verb == "steal":
        subject = remove_delimeter(predicates[0])
        obj = remove_delimeter(predicates[1])
        other = remove_delimeter(predicates[2])
        location = remove_delimeter(predicates[3], delimeter="-")
        variant_probability = [0.3, 0.4, 0.3]
        variant1 = "{} steals {} from {} at {}".format(subject, obj, other, location)
        variant2 = "At {}, {} steals {} from {}".format(location, subject, obj, other)
        variant3 = "{} sees {} with {} at {} and steals it from them".format(subject, other, obj, location)
        steal_grammar = {
            "origin": [(variant1, variant_probability[0]),
                       (variant2 , variant_probability[1]), 
                       (variant3 , variant_probability[2])           
            ]
        }
        sentence = parse_pcfg(steal_grammar)
    return sentence
        

if len(sys.argv) > 1:
    path = sys.argv[1]
    with open(path) as solution_file:
        data = solution_file.read()
        data = data.strip()
        action_text = data.split(":steps")[1][:-2]
        actions = action_text.split("\n")
        actions = [a.strip().strip("(").strip(")").split() for a in actions]
        story = ""
        for action in actions:
            verb = action[0]
            predicates = action[1:]
            action_text = text_for_action(verb, predicates)
            story += action_text + ". " 
        print(story)
else:
    print("Error: Provide solution file path")

