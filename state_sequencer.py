import math
import numpy as np

class state_sequencer:

	def __init__(self, noStates , noInputs , noOutputs, sequence): 
		
		self.noBits = math.ceil(math.log(noStates,2))
		self.noStates = noStates
		self.noInputs = noInputs
		self.noOutputs = noOutputs
		self.sequence = sequence
		self.nextStateSequence = [[0]*self.noStates]*self.noStates
		self.outputSequence = [[0]*self.noOutputs]*self.noStates

	def sequence_matrix(self):
		
		for i in range(self.noStates):
			for state in self.sequence[i]:
				self.nextStateSequence[i][state[0]]+=1
				for j in range(self.noOutputs):
					self.outputSequence[i][j]+=state[2][j]


		return self.nextStateSequence,self.outputSequence

	def attraction_matrix(self):
		nextStateSequence_np = np.array(self.nextStateSequence)
		outputSequence_np = np.array(self.outputSequence)

		self.attraction_matrix = self.noBits*np.matmul(nextStateSequence_np,nextStateSequence_np.T) + np.matmul(outputSequence_np,outputSequence_np.T)

		return self.attraction_matrix


class state:

	def __init__(self , nextState, inputs, outputs):
		self.state = [nextState,inputs,outputs]


h = state()

def state_assignment():
	visited_states = []

	max_attraction_states,attraction_sort = max_attraction(noBits,attraction_matrix)

	for state in attraction_sort:
		
		if len(visited_states) == noStates:
			break

		if state not in visited_states:
			visited_states.append(state)
			#assign the state something
			for nextState in max_attraction_states[state]:
				if next_state not in visited_states:
					visited_states.append(next_state)
					#assign the next_states something




def max_attraction(noBits,attraction_matrix):
	max_attraction_states = [] #states which are most attracted in decreasing order
	attraction_total = []
	
	for state_attraction in attraction_matrix:
		ind = np.argpartition(state_attraction,-2)[-2:]
		total = 0
		for index in ind:
			total += state_attraction[index]
		attraction_total.append(total)
		max_attraction_states.append(ind[np.argsort(-state_attraction[ind])])


	attraction_sort = np.argsort(-np.array(attraction_total))

	return max_attraction_states,attraction_sort

		
#sequence would be of the form S1-> an array of states to show the connection in the finite state machine
#thus a list of list of next states corresponding to the indices representing the states