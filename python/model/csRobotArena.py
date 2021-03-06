#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# >>> import modules

from partiallyObservableMarkovDecisionProcess import *
from explicitMarkovDecisionProcess import *
from distribution import Distribution
import itertools as it
import onTheFlyModelChecking as otf
import random

# >>> code

def simulation(pomdp, init, prior, gamma, it, height,width):
   """
   Robot scenario simulation
      pomdp: model
      init: initial concrete state
      prior: initial belief state
      gamma: goal formula
      it: number of iterations
      height: height of the arena
      width: width of the arena
   """

   currentState = init
   currentBelief = prior
   printArena(init,[],height,width)
   #if currentState[0] in currentState[1:]:
   #   cc[run,0] += 1     
   for i in range(it):
      print 'ITERATION',str(i)
      action = gamma(currentBelief)
      currentState = stepAction(pomdp, currentState, action)
      currentBelief = beliefUpdate(pomdp,currentBelief,action,weighted_choice(pomdp.observationFunction[pomdp.inv_states[currentState]]))
      printArena(currentState,[],height,width)



# ======================
# == SIMULATION UTILS ==
# ======================

def printArena(current,goalPos,height,width):
   """
   Print the current state of the arena scenario
      current: current concrete state
      goalPos: goal positions
      height: height of the arena
      width: width of the arena
   """
   arena = ""
   for l in range(height-1,-1,-1):
      for w in range(width):
         if (l,w) == current[0]:
            arena += 'o'
         elif (l,w) in current:
            arena += 'x'
         elif (l,w) in goalPos:
            arena += '#'
         else:
            arena += '.'
      arena += '\n'
   print arena

def stepAction(pomdp,current,action):
   """
   Simulation of action execution
      pomdp: model
      current: current concrete state
      action: action to perform
      return: the new concrete state
   """
   return pomdp.states[
      weighted_choice(
         pomdp.transitionFunction[(pomdp.inv_states[current],action)])
      ]

def stepObservation(pomdp,current):
   """
   Simulation of the observation
      pomdp: model
      current: current concrete state
      return: the received observation
   """
   return weighted_choice(pomdp.observationFunction[pomdp.inv_states[current]])

def weighted_choice(choices):
    """ 
    Weighed extraction
      choices: discrete distribution dictionary with elements as keys 
         and probabilities as values (it must be sum 1)
      return: the chosen element
    """
    r = random.uniform(0, 1)
    upto = 0
    for st,pr in choices.iteritems():
        if upto + pr > r:
            return st
        upto += pr
    assert False, "Shouldn't get here"

# ===========
# == MODEL ==
# ===========

def robotPomdp(height,width):
   """
   Visual representation of the robot scenario, environmental robots 
   are represented as 'x' and can move only to the left or to the 
   right remaining in the same level.

   small example
   .#x.
   x...
   .o..

   """
   # status of the main agent
   s = [set(it.product(set(range(height)),set(range(width))))]
   # status of environmental robots
   for l in range(height):
      s.append(set(it.product([l],range(width))))
   # states
   S = set(it.product(*s))

   # actions
   A = {'right','forward','left','backward'}

   # observations
   #  0..sight-1 : environmental robots observations
   #  sight : goal observation
   O = set(it.product({True,False},repeat=5))

   # define transition function
   T = dict()
   for s in S:
      for a in A:
         env = [envRobotDistr(pos[0],pos[1],width) for pos in s[1:]]
         nextStates = list(it.product(*[el.keys() for el in env]))
         if not nextStates:
            continue
         T[(s,a)] = dict()
         for n in nextStates:
            x = (mainRobotNext(s[0][0],s[0][1],a,height,width),) + n
            T[(s,a)][x] = transitionProb(s,x,height,width)

   # define observation function
   Z = dict()
   for s in S:
      # in place observation
      obs = (s[0] in s[1:],)
      # north observation
      obs += ((s[0][0],s[0][0]+1) in s[1:],)
      # east observation
      obs += ((s[0][0]+1,s[0][0]) in s[1:],)
      # south observation
      obs += ((s[0][0],s[0][0]-1) in s[1:],)
      # west observation
      obs += ((s[0][0]-1,s[0][0]) in s[1:],)
      Z[s] = { obs : 1 }
   return PartiallyObservableMarkovDecisionProcess(S, A, T, O, Z)

def transitionProb(s1,s2,levels,width):
   prob = 1.
   for l in range(1,levels-1):
      d2 = envRobotDistr(s1[l][0],s1[l][1],width)
      prob *= d2[(s2[l][0],s2[l][1])]
   return prob

def mainRobotNext(r,c,a,levels,width):
   if a == "left":
      return (r,max(c-1,0))
   elif a == "right":
      return (r,min(width-1,c+1))
   elif a == "forward":
      return (min(r+1,levels-1),c)
   elif a == "backward":
      return (max(r-1,0),c)
   elif a == "stand":
      return (r,c)
   raise Exception('Unknown action')

def envRobotDistr(r,c,width):
   if c == 0:
      return {(r,0) : 0.5, (r,1) : 0.5}
   elif c == width-1:
      return {(r,width-1) : 0.5, (r,width-2) : 0.5}
   else:
      return {(r,c) : 1/3., (r,c-1) : 1/3., (r,c+1) : 1/3.}

if __name__ == '__main__':
   random.seed(1)
   height = 4
   width = 4
   initPos = (1,1)
   concreteInitPos = (initPos,(0,0),(1,2),(2,1),(3,3))
   iterations = 10
   # partially observable model
   pomdp = robotPomdp(height, width)
   # initial states
   init = set(map(lambda s: pomdp.inv_states[s], filter(lambda s: s[0] == initPos, pomdp.states.values())))
   #init = filter(lambda s: s[0] == initPos, pomdp.states.values())
   # initial belief
   prior = Distribution(set(pomdp.states.keys()),\
      lambda el,dom: Distribution.restrictedUniformPdf(el,dom,init))
   #prior = Distribution(set(pomdp.states.keys()), Distribution.uniformPdf)
   # prior belief updated to the first observation
   #prior = beliefUpdateObservation(pomdp,prior,pomdp.inv_observations[(False,False,False)])
   
   # generate explicit MDP
   print 'emdp construction'
   emdp = ExplicitMarkovDecisionProcess(pomdp,prior)
   print 'end (emdp empty)'

   # observation classes
   collision = filter(lambda o: o[0], pomdp.observations.values())
   notCollision = filter(lambda o: not o[0], pomdp.observations.values())
   sensing = filter(lambda o: reduce(lambda a,b: a or b, o), pomdp.observations.values())
   anyObs = filter(lambda o: True, pomdp.observations.values())
   sensAndNotCollide = [o for o in pomdp.observations.values() if (o in sensing and o in notCollision)]

   # MAX PMIN ( X notCollision )
   #gamma = \
   #   lambda b : MaxGoalProb(emdp, \
   #      lambda b1,o1 : PminNext(emdp, \
   #         lambda b2,o2 : PObs(emdp,notCollision,b2,o2), \
   #         b1,o1),
   #      b)

   # MAX P ( notCollision )
   #gamma = lambda b : MaxGoalProb(emdp, lambda b1,o1 : PObs(emdp,notCollision,b1,o1),b)

   # MIN P ( collision )
   #gamma = lambda b : MinGoalProb(emdp, lambda b1,o1 : PObs(emdp,collision,b1,o1),b)

   # MIN PMAX ( X collision )
   #gamma = \
   #   lambda b : MinGoalProb(emdp, \
   #      lambda b1,o1 : PmaxNext(emdp, \
   #         lambda b2,o2 : PObs(emdp,collision,b2,o2), \
   #         b1,o1),
   #      b)

   # MAX P ( sense and not collide )
   #gamma = lambda b : MaxGoalProb(emdp, \
   #   lambda b1,o1 : PObs(emdp,sensAndNotCollide,b1,o1),b)

   # MAX PMIN ( sense and not collide U<=1 not collide )
   #steps = 1
   #gamma = \
   #   lambda b : MaxGoalProb(emdp, \
   #      lambda b1, o1 : PmaxUntil(emdp, \
   #         lambda b2, o2 : PObs(emdp, sensAndNotCollide, b2, o2), \
   #         lambda b3, o3 : PObs(emdp, notCollision, b3, o3), \
   #         steps, b1, o1),\
   #      b)

   # MAX PMIN ( X sense and not collision )
   g1 = \
      lambda b : MaxGoalProb(emdp, \
         lambda b1,o1 : PminNext(emdp, \
            lambda b2,o2 : PObs(emdp,sensAndNotCollide,b2,o2), \
            b1,o1),
         b)

   # MAX PMIN ( X sense and not collision )
   g2 = \
      lambda b : MaxGoalProb(emdp, \
         lambda b1,o1 : PmaxNext(emdp, \
            lambda b2,o2 : PObs(emdp,sensAndNotCollide,b2,o2), \
            b1,o1),
         b)

   # MAX PMIN ( * U<=n goalObs )
   #steps = 3
   #gamma = \
   #   lambda b : MaxGoalProb(emdp, \
   #      lambda b1, o1 : PmaxUntil(emdp, \
   #         lambda b2, o2 : PObs(emdp, notCollision, b2, o2), \
   #         lambda b3, o3 : PObs(emdp, goalObs, b3, o3), \
   #         steps, b1, o1),\
   #      b)

   simulation(pomdp, concreteInitPos, prior, g1, iterations, height, width)


#  # model checking
#  goalObs = filter(lambda o: o[sight] == True, pomdp.observations.values())
#  collision = filter(lambda o: o[0] == True, pomdp.observations.values())
#  notCollision = filter(lambda o: o[0] == False, pomdp.observations.values())

#  # MAXMIN do not collide
#  pathFormula = lambda b,o : PObs(emdp,notCollision,b,o)
#  act = MaxGoalProb(emdp,pathFormula,prior)
#  print 'MAX P( notCollision | prior) = ', str(pomdp.actions[act])
#  # MINMAX do not collide
#  act = MinGoalProb(emdp,pathFormula,prior)
#  print 'MIN P( notCollision | prior) = ', str(pomdp.actions[act])

#  # MAXMIN do not collide at the next step
#  pathFormula = lambda b1,o1 : PminNext(emdp,lambda b2,o2: \
#     PObs(emdp,notCollision,b2,o2),b1,o1)
#  act = MaxGoalProb(emdp,pathFormula,prior)
#  print 'MAX Pmin( X notCollision | prior) = ', str(pomdp.actions[act])

#  # MINMAX do not collide at the next step
#  pathFormula = lambda b1,o1 : PmaxNext(emdp,lambda b2,o2: \
#     PObs(emdp,collision,b2,o2),b1,o1)
#  act = MinGoalProb(emdp,pathFormula,prior)
#  print 'MIN Pmax( X collision | prior) = ', str(pomdp.actions[act])

#  # MAXMAX do not collide at the next step
#  pathFormula = lambda b1,o1 : PmaxNext(emdp,lambda b2,o2: \
#     PObs(emdp,collision,b2,o2),b1,o1)
#  act = MaxGoalProb(emdp,pathFormula,prior)
#  print 'MAX Pmax( X collision | prior) = ', str(pomdp.actions[act])

#  # MINMIN do not collide at the next step
#  pathFormula = lambda b1,o1 : PminNext(emdp,lambda b2,o2: \
#     PObs(emdp,notCollision,b2,o2),b1,o1)
#  act = MinGoalProb(emdp,pathFormula,prior)
#  print 'MIN Pmin( X notCollision | prior) = ', str(pomdp.actions[act])

#   prob = PmaxNext(emdp,lambda b,o: PObs(emdp,notCollision,b,o),\
#      prior,pomdp.inv_observations[(False,False,False)])
#   print 'Pmax( X notCollision | prior, (F,F,T,F)) = ', str(prob)
#
#   steps = 3
#   pathFormula = lambda b1,o1: PmaxUntil(emdp,\
#      lambda b,o: PObs(emdp,notCollision,b,o),\
#      lambda b,o: PObs(emdp,emdp.pomdp.observations,b,o),\
#      steps,b1,o1)
#   act = MaxGoalProb(emdp,pathFormula,prior)
#   print 'act =', emdp.pomdp.actions[act]

#   steps = 4
#   prob = PminUntil(emdp,\
#      lambda b,o: PObs(emdp,notCollision,b,o),\
#      lambda b,o: PObs(emdp,goal,b,o),\
#      steps,prior, pomdp.inv_observations[(False,False,True,False)])
#   print 'Pmin( notCollision U<='+str(steps)+' goal | prior, (F,F,T,F)) = ', str(prob)
#   
#   prob = PmaxUntil(emdp,\
#      lambda b,o: PObs(emdp,notCollision,b,o),\
#      lambda b,o: PObs(emdp,goal,b,o),\
#      steps,prior, pomdp.inv_observations[(False,False,True,False)])
#   print 'Pmax( notCollision U<='+str(steps)+' goal | prior, (F,F,T,F)) = ', str(prob)

#   print 'initial belief: ',prior
#   p = PminUntil(emdp, 
#      lambda b,o: PObs(emdp,{'hl','hr','W','L'},b,o), 
#      lambda b,o: PObs(emdp,{'W','hr','hl'},b,o), 
#      3, b0, 0)
#   print 'Pmin( * U<=3 {W,L,hl} | b0,hl) = ', str(p)



# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"