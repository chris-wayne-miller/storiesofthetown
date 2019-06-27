import re
import sys

def pluralize(verb):
    return verb + "s"

def remove_delimeter(word, delimeter="_"):
    return " ".join(word.split(delimeter))

def text_for_action(verb, predicates):
    order = []
    if verb == "travel":
        order = [remove_delimeter(predicates[0]), "traveled", "from", remove_delimeter(predicates[1], delimeter="-"), "to", remove_delimeter(predicates[2], delimeter="-")]
    elif verb == "retrieve":
        order = [remove_delimeter(predicates[0]), "picked up", remove_delimeter(predicates[1])]
    elif verb == "vigorousdance":
        order = [remove_delimeter(predicates[0]), "engages in a vigorous dance.  After several minutes of dancing", remove_delimeter(predicates[0]), "feels ready to take on the world"]
    elif verb == "give":
        order = [remove_delimeter(predicates[0]), pluralize(verb), remove_delimeter(predicates[2]), "to", remove_delimeter(predicates[1])]
    elif verb == "flirt":
        order = [remove_delimeter(predicates[0]), pluralize(verb), "with", remove_delimeter(predicates[1]), "at", remove_delimeter(predicates[2], delimeter="-"), "by whispering sweet nothings into their ear.", remove_delimeter(predicates[1]), "is now smitten with", remove_delimeter(predicates[0])]
    elif verb == "persuadetodislike":
         order = [remove_delimeter(predicates[0]), "persuades", remove_delimeter(predicates[1]), "to dislike", remove_delimeter(predicates[2]), "at", remove_delimeter(predicates[3], delimeter="-"), "by spreading nasty rumors"]
    elif verb == "steal":
         order = [remove_delimeter(predicates[0]), pluralize(verb), remove_delimeter(predicates[2]), "from", remove_delimeter(predicates[1]), "at", remove_delimeter(predicates[3], delimeter="-")]
    return " ".join(order)
        

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
