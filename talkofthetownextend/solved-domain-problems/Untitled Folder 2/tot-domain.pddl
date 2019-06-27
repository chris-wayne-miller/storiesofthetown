;;; 
;;; Sample domain for Talk of the Town planning narrative
;;;

(define (domain tot-domain)
  (:requirements :adl :domain-axioms :intentionality)
  (:types character job - object
	item
	place
  )
  (:constants Starlight-Park Sunset-Bistro Dawnbreak-Airport Hip-Hop-Dance-Studio - place
  flower panini overpriced_food sick_dance_moves_brochure - item)

  (:predicates 
  	       (likes ?character - character ?characterb - character)
	       (dislikes ?character - character ?characterb - character)
	       (love_interest ?character - character ?characterb - character)
	       (best_friend ?character - character ?characterb - character)
	       (worst_enemy ?character - character ?characterb - character)
	       (at ?character - character ?place - place)
	       (extrovert ?character - character)
	       (introvert ?character - character)
	       (item_at ?item - item ?place - place)
	       (loves ?character - character ?characterb - character)
	       (has ?character - character ?item - item))
  		
   ;; A character travels from one place to another.
  (:action travel
    :parameters   (?character - character ?from - place ?to - place)
    :precondition (at ?character ?from)
    :effect       (and (at ?character ?to)
                       (not (at ?character ?from)))
    :agents       (?character))

  ;; A character retrieves an item from a location
  (:action retrieve
   :parameters (?character - character ?item - item ?place - place)
   :precondition (and	(at ?character ?place)
   			(item_at ?item ?place))
   :effect	 (and (has ?character ?item)
   			(not (item_at ?item ?place)))
   :agents 	 (?character))

  ;; A character gives an item to another character
  (:action give
    :parameters (?giver - character ?recipient - character ?item - item ?place - place)
    :precondition (and 	(not (= ?giver ?recipient))
			(has ?giver ?item)
			(at ?giver ?place)
			(at ?recipient ?place))
    :effect	  (and (not (has ?giver ?item))
    			(likes ?recipient ?giver)
			(not (dislikes ?recipient ?giver))
			(has ?recipient ?item))
    :agents	  (?giver))

  ;; A character steals an item from another character
  (:action steal
    :parameters (?thief - character ?victim - character ?item - item ?place - place)
    :precondition (and 	(not (= ?thief ?victim))
			(has ?victim ?item)
			(not (has ?thief ?item))
			(not (likes ?thief ?victim))
			(not (intends ?thief (likes ?victim ?thief)))
			(not (intends ?thief (loves ?victim ?thief)))
			(at ?thief ?place)
			(at ?victim ?place))
    :effect	  (and (has ?thief ?item)
    			(not (has ?victim ?item)))
    :agents 	  (?thief))

   ;; A character transforms themselves into an extrovert via vigorous dancing
   ;; Also "consumes" the dance brochure
   (:action vigorousdance 
     :parameters 	(?actor - character)
     :precondition 	(and (at ?actor Hip-Hop-Dance-Studio)
     				(introvert ?actor)
     				(has ?actor sick_dance_moves_brochure))
     :effect		(and (extrovert ?actor)
     			  (not (introvert ?actor))
			  (not (has ?actor sick_dance_moves_brochure)))
     :agents		(?actor))

   ;; A character flirts with another character to make them love them
   (:action flirt
     :parameters (?flirter - character ?flirtee - character ?place - place)
     :precondition (and (likes ?flirtee ?flirter)
     			(at ?flirter ?place)
			(at ?flirtee ?place)
			(not (dislikes ?flirtee ?flirter))
			(extrovert ?flirter))
     :effect	  (loves ?flirtee ?flirter)
     :agents	  (?flirter))



)






