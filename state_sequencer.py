import math
import numpy as np

class state_sequencer:

	def __init__(self, noStates , noInputs , noOutputs, sequence): 
		
		self.noBits = math.ceil(math.log(noStates,2))
		self.noStates = noStates
		self.noInputs = noInputs
		self.noOutputs = noOutputs
		self.sequence = sequence

	def sequence_matrix(self):
		
		nextStateSequence = [[0]*noStates]*noStates
		outputSequence = [[0]*noOutputs]*noStates
		
		for i in range(noStates):
			for state in self.sequence[i]:
				nextStateSequence[i][state[0]]+=1
				for j in range(noOutputs):
					outputSequence[i][j]+=state[2][j]

		return nextStateSequence,outputSequence

	def attraction_matrix(nextStateSequence,outputSequence,noBits):
		nextStateSequence_np = np.array(nextStateSequence)
		outputSequence_np = np.array(outputSequence)

		attraction_matrix = noBits*np.matmul(nextStateSequence_np,nextStateSequence_np.T) + np.matmul(outputSequence_np,outputSequence_np.T)

		return attraction_matrix


class state:

	def __init__(self , nextState, inputs, outputs):
		self.state = [nextState,inputs,outputs]




def state_assignment():



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