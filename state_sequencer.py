import math
import numpy as np
import itertools


def graycode(state):
	nextstates = []
	for i in range(len(state)):
		a = list(state)
		a[i] = not (a[i])
		nextstates.append(tuple(a))
	#print (nextstates)
	return nextstates


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

	def state_assignment(self):  #no idea might need to alter
		encoding_list = list(itertools.product([False, True], repeat=int(self.noBits)))
		encoded_states = []
		assigned_states = [0]*self.noStates
		visited_states = []

		#max_attraction_states,attraction_sort = state_seq.max_attraction()

		for state in self.attraction_sort:
			#gray_list= graycode(state)
			if len(visited_states) == self.noStates:
				break

			if state not in visited_states:
				visited_states.append(state)
				#assign the state something
				for st in encoding_list:
					if (st not in encoded_states):
						encoded_states.append(st)
						assigned_states[state] = st
						break
	 
			for nextState in self.max_attraction_states[state]:
				if nextState not in visited_states:
					gray_list = graycode(assigned_states[state]) 
						#assign the next_states something
					#print(gray_list)
					for st in gray_list:
						if (st not in encoded_states):
							encoded_states.append(st)
							assigned_states[nextState] = st
							visited_states.append(nextState)
							break

		return assigned_states



class state:

	def __init__(self , nextState, inputs, outputs):
		self.state = [nextState,inputs,outputs]









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
state_assignment_try = state_seq1.state_assignment()
print(state_assignment_try)
		
#sequence would be of the form S1-> an array of states to show the connection in the finite state machine
#thus a list of list of next states corresponding to the indices representing the states