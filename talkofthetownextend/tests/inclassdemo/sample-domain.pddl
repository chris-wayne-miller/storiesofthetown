;;;
;;; A highly simplified version of the actions in Indiana Jones and the Raiders of the Lost Ark
;;; Created by Stephen G. Ware
;;; Originally used to test the Glaive Narrative Planner
;;;
(define (sample-domain)
  (:requirements :adl :domain-axioms :intentionality)
  (:types character place - object
          weapon - item)
  (:constants fireemblem - item)
  (:predicates (open ark)
               (alive ?character - character)
               (armed ?character - character)
               (knows-location ?character - character ?item - item ?place - place)
               (at ?character - character ?place - place)
               (has ?character - character ?item - item))
	       (hidden ?character - character))

  ;; A character travels from one place to another.
  (:action travel
    :parameters   (?character - character ?from - place ?to - place)
	:precondition (and (not (= ?from ?to))
                       (alive ?character)
                       (at ?character ?from))
	:effect       (and (not (at ?character ?from))
                       (at ?character ?to))
    :agents       (?character))

  ;; One character gives an item to another.
  (:action give
    :parameters   (?giver - character ?item - item ?receiver - character ?place - place)
	:precondition (and (not (= ?giver ?receiver))
                       (alive ?giver)
                       (at ?giver ?place)
                       (has ?giver ?item)
                       (alive ?receiver)
                       (at ?receiver ?place))
	:effect       (and (not (has ?giver ?item))
                       (has ?receiver ?item))
    :agents       (?giver ?receiver))

  ;; One character hides in a location
  (:action hide
    :parameters   (?character - character ?place - place)
    :precondition (and (alive ?character)
    		       (at ?character ?place)
		       (not (?hidden)))
    :effect	(hidden ?character)
    :agents 	(?character))

  ;; One character kills another.
  (:action kill
    :parameters   (?killer - character ?weapon - weapon ?victim - character ?place - place)
    :precondition (and (alive ?killer)
                       (at ?killer ?place)
		       (hidden ?killer)
                       (has ?killer ?weapon)
                       (alive ?victim)
                       (at ?victim ?place))
    :effect       (not (alive ?victim))
    :agents       (?killer))
  
  ;; One character takes an item from another at weapon-point.
  (:action take
    :parameters   (?taker - character ?item - item ?victim - character ?place - place)
	:precondition (and (not (= ?taker ?victim))
                       (alive ?taker)
                       (at ?taker ?place)
                       (or (not (alive ?victim))
                           (and (armed ?taker)
                                (not (armed ?victim))))
                       (at ?victim ?place)
                       (has ?victim ?item))
	:effect       (and (not (has ?victim ?item))
                       (has ?taker ?item))
    :agents       (?taker))

  ;; When a character has a weapon, they are armed.
  (:axiom
    :vars    (?character - character)
    :context (and (not (armed ?character))
                  (exists (?w - weapon)
                          (has ?character ?w)))
    :implies (armed ?character))

  ;; When a character does not have a weapon, they are unarmed.
  (:axiom
    :vars    (?character - character)
    :context (and (armed ?character)
                  (forall (?w - weapon)
                          (not (has ?character ?w))))
    :implies (not (armed ?character))))
