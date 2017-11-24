import math
import numpy as np

class state_sequencer:

	def __init__(self, noStates , noInputs , noOutputs, sequence): 
		
		self.noBits = math.ceil(math.log(noStates,2))
		self.noStates = noStates
		self.noInputs = noInputs
		self.noOutputs = noOutputs
		self.sequence = sequence
		self.nextStateSequence = np.zeros((self.noStates,self.noStates))
		self.outputSequence = np.zeros((self.noStates,self.noOutputs))

	def sequence_matrix(self):
		
		for i in range(self.noStates):
			for state in self.sequence[i]:
				self.nextStateSequence[i][state[0]]+=1
				for j in range(self.noOutputs):
					self.outputSequence[i][j]+=state[2][j]
		


		return self.nextStateSequence,self.outputSequence

	def attraction_matrix(self):

		self.attraction_matrix = self.noBits*np.matmul(self.nextStateSequence,self.nextStateSequence.T) + np.matmul(self.outputSequence,self.outputSequence.T)

		return self.attraction_matrix

	def max_attraction(self):
		self.max_attraction_states = [] #states which are most attracted in decreasing order
		attraction_total = []
		i=0
	
		for state_attraction in self.attraction_matrix:
			ind = np.argpartition(state_attraction,-(self.noBits+1))[-(self.noBits+1):]
			
			attraction_states = ind[np.argsort(-state_attraction[ind])]	
			
			if i in attraction_states:	
				index_1 = np.argwhere(attraction_states == i)
				attraction_states = np.delete(attraction_states, index_1)
			i=i+1	
			
			attraction_state_n = attraction_states[:self.noBits]
			self.max_attraction_states.append(attraction_state_n)

			total = 0
			for index in attraction_state_n:
				total += state_attraction[index]

			attraction_total.append(total)

		print(attraction_total)
		self.attraction_sort = np.argsort(-np.array(attraction_total))
		return self.max_attraction_states,self.attraction_sort


class state:

	def __init__(self , nextState, inputs, outputs):
		self.state = [nextState,inputs,outputs]



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






state_seq=[[[1,(0,0),(0,0)],[2,(1,0),(1,1)]],[[1,(1,0),(0,1)],[2,(0,1),(1,0)]],[[0,(1,1),(0,0)]]]
state_seq1=state_sequencer(3,2,2,state_seq)
nextStateSequence_try,outputSequence_try=state_seq1.sequence_matrix()
print(nextStateSequence_try)
print(outputSequence_try)
attraction_matrix_try = state_seq1.attraction_matrix()
print(attraction_matrix_try)
max_attraction_states_try,attraction_sort_try = state_seq1.max_attraction()
print(max_attraction_states_try)
print(attraction_sort_try)
		
#sequence would be of the form S1-> an array of states to show the connection in the finite state machine
#thus a list of list of next states corresponding to the indices representing the states