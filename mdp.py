#state : (x,y)
#action: A V < >
#transition function  T
debugF =False
import random
import time
import sys


accuracy =0.8
discountValue =0.9
obstaclestates = [(4,5),(6,5),(3,2)]

endState =(5,5)
deadState=(5,4)
liveReward = -0.1

def buildMap():
	# map , *value , policy
	eMap = [[(' ',0,' ') for x in range(11)] for y in range(11) ]
	#tresure
	eMap[2][0]=('Q',0,' ')
	eMap[endState[1]][endState[0]]=('T',0,'T')
	eMap[deadState[1]][deadState[0]]=('D',0,'D')
	for oState in obstaclestates:
		eMap[oState[1]][oState[0]]=(' ',0,' ')


	return eMap



def noiseAction(action):
	actionSet={'D':'U','U':'D','L':'R','R':'L'}
	rValue = random.randint(0,99)

	#noise
	if rValue/100.0> accuracy:
		subActionSet=[a for a in actionSet.keys() if a != action and a != actionSet[action] ]
		return subActionSet[rValue%2]
	else:
		return action


def printValue(eMap):
	print "\n\n"
	for row in eMap:
		print map(lambda x:x[1],row )



def reward(state):

	if state == endState:
		return 1
	elif state == deadState:
		return -1
	else:
		return liveReward

def transition(currentState,action,nextState,eMap):
	actionSet={'D':'U','U':'D','L':'R','R':'L'}

	if move(currentState,action,eMap) == nextState:
		return accuracy

	

	return (1-accuracy)/3


def updateValue(state,eMap):

	if state in [endState,deadState]+obstaclestates:
		return

	policyTlb = {'D':'V','U':'A','L':'<','R':'>'}

	maxValue =-1*sys.maxint
	policyAction=' ' 
	for a in ['U','D','L','R']:
		value = Q(state,a,eMap)
		if debugF: print "Q(",state,",",a,")=",value
		if value > maxValue:
			maxValue=value
			policyAction = policyTlb[a]


	eMap[state[1]][state[0]]=(eMap[state[1]][state[0]][0],round(maxValue,2),policyAction)


def getValue(state,eMap):
	return eMap[state[1]][state[0]][1]


def Q(state,action,eMap):
	res=0.0
	possibleStates = set([ move(state,a,eMap) for a in ['U','D','L','R']  ])
	if debugF: print "\nQ(",state,',',action,"): "

	for pState in possibleStates:
		res+=transition(state,action,pState,eMap)*(reward(pState)+discountValue*getValue(pState,eMap)   )
		if debugF: print pState,str(transition(state,action,pState,eMap))+"* ("+str(reward(pState))+"+"+str(discountValue)+"*"+str(getValue(pState,eMap))+")"
	return res


def move(currentState,action,eMap):

	if action is 'U' and currentState[1] >0  and (currentState[0],currentState[1]-1) not in obstaclestates:
			nextState = (currentState[0],currentState[1]-1)
			
	elif action is 'D' and currentState[1]<(len(eMap)-1) and (currentState[0],currentState[1]+1) not in obstaclestates:
			nextState = (currentState[0],currentState[1]+1)
		
	elif action is 'L' and 0 < currentState[0] and(currentState[0]-1,currentState[1]) not in obstaclestates :
			nextState = (currentState[0]-1,currentState[1])
		
	elif action is 'R' and currentState[0] < (len(eMap[0])-1) and (currentState[0]+1,currentState[1]) not in obstaclestates :
			nextState = (currentState[0]+1,currentState[1])

	else:
		nextState= currentState


	return nextState


def printPolicy(eMap):

	for row in eMap:
		print map(lambda x:x[2],row )





def MDP(epoch,initState=(0,2)):
	nextState=initState

	eMap = buildMap()
	actionSet={'D':'U','U':'D','L':'R','R':'L'}

	for idx in range(epoch):
		currentState = nextState
		
		#time.sleep(0.5)

		for y in range(len(eMap)):
			for x in range(len(eMap[0])):
				updateValue((x,y),eMap)
		
		printValue(eMap)
		print "========"
		printPolicy(eMap)
		

		




	#move
	
	'''
	rValue=random.randint(0,99)
	action = noiseAction(list(actionSet.keys())[rValue%4]  )
	nextState = move(currentState,action)
	eMap[currentState[1]][currentState[0]] = (' ',eMap[currentState[1]][currentState[0]][1])
	eMap[nextState[1]][nextState[0]] = ('Q',eMap[nextState[1]][nextState[0]][1])
	'''




MDP(100)

