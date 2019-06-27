;;;
;;; A highly simplified problem for Indiana Jones and the Raiders of the Lost Ark
;;; Created by Stephen G. Ware
;;;
(define (problem get-sample)
  (:domain sample-domain)
  (:objects marth roy merric - character
            altea pherae askr - place
            sword - weapon)
  (:init (alive marth)
         (at marth altea)
	 (has marth sword)
         (intends roy (not (alive)))
         (alive roy)
         (at roy pherae)
         (alive merric)
         (at merric altea)
  (:goal (and (at marth altea)
              (not (alive roy)))))
