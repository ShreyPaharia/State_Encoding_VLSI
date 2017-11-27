import math
import numpy as np
import itertools


def graycode(state):                # Returns a list of encodings that differ at one bit from the given encoding (gray code)
	nextstates = []
	for i in range(len(state)):
		a = list(state)
		a[i] = not (a[i])           #complementing one bit a time
		nextstates.append(tuple(a))
	return nextstates


class state_sequencer:

	def __init__(self, noStates , noInputs , noOutputs, sequence): 
		
		#This is the manimum number of bits required to encode any number of states
		self.noBits = int(math.ceil(math.log(noStates,2)))       
		
		self.noStates = noStates
		self.noInputs = noInputs
		self.noOutputs = noOutputs
		self.sequence = sequence

		#This matrix is such that present state represents rows and next state represents column - the entries are the number of inputs for which the present state goes to next state
		self.nextStateSequence = np.zeros((self.noStates,self.noStates))

		#This matrix is such that present state represents rows and outputs while going to the next state represents column - the entries are the number of times an output becomes 1 while going out from the present state      
		self.outputSequence = np.zeros((self.noStates,self.noOutputs))

		#This matrix is such that next state represents rows and inout required for any state to goto next state represents column - the entries are the number of times an input comes for which the present state goes to next state
		self.inputSequence = np.zeros((self.noStates,int(math.pow(2,self.noInputs))))


	def sequence_matrix(self): #Func to find the nextStateSequence, inputSequence and outputSequence
		
		for i in range(self.noStates):
			for state in self.sequence[i]:
				input_deci = 0
				self.nextStateSequence[i][state[0]]+=1
				
				for j in range(self.noOutputs):
					self.outputSequence[i][j]+=state[2][j]

				for j in range(self.noInputs):
					input_deci+= state[1][j]*math.pow(2,self.noInputs-j-1)
				self.inputSequence[state[0]][int(input_deci)]+=1

		return self.nextStateSequence,self.outputSequence,self.inputSequence

	def attraction_matrix(self): #Func to find out the attraction matrix for FANIN and FANOUT algorithms

		attraction_matrix_fanout = self.noBits*np.matmul(self.nextStateSequence,self.nextStateSequence.T) + np.matmul(self.outputSequence,self.outputSequence.T)
		attraction_matrix_fanin = self.noBits*np.matmul(self.nextStateSequence,self.nextStateSequence.T) + np.matmul(self.inputSequence,self.inputSequence.T)


		return attraction_matrix_fanout,attraction_matrix_fanin

	def max_attraction(self,attraction_matrix): #Func to find out the max_attraction_states & attraction_total
		# max_attraction_states => Has states as rows and the ordered list of n most attracted states in decreasing order corresponding to them
		max_attraction_states = []

		# attraction_total => Sum of the attraction of the n most attracted states corresponding to each state
		attraction_total = []
		i=0
	
		for state_attraction in attraction_matrix:
			ind = np.argpartition(state_attraction,-(self.noBits+1))[-(self.noBits+1):]
			
			attraction_states = ind[np.argsort(-state_attraction[ind])]	
			
			if i in attraction_states:	
				index_1 = np.argwhere(attraction_states == i)
				attraction_states = np.delete(attraction_states, index_1)
			i=i+1	
			
			attraction_state_n = attraction_states[:self.noBits]
			max_attraction_states.append(attraction_state_n)

			total = 0
			for index in attraction_state_n:
				total += state_attraction[index]

			attraction_total.append(total)

		attraction_sort = np.argsort(-np.array(attraction_total))
		return max_attraction_states,attraction_sort

	def state_assignment(self,max_attraction_states,attraction_sort):  #no idea might need to alter
		encoding_list = list(itertools.product([False, True], repeat=int(self.noBits))) #Generates all possible encodings of noBits , e.g. ((0,0),(0,1),(1,0),(1,1)) for noBits = 2
		encoded_states = []                                                             #List of encodins which are used
		assigned_states = [0]*self.noStates												#Final list of encoding, index be the state that is encoded 					
		visited_states = []																#List of States that are being encoded				

		for state in attraction_sort:                                                   
			
			if len(visited_states) == self.noStates:						# Break out of the loop if all states are visited
				break

			if state not in visited_states:									#If state not in visited state, append it to the list 
				visited_states.append(state)
				#assign the state something
				for st in encoding_list:									#Chose a state encoding from the encoding_list
					if (st not in encoded_states):							#If that state encoding is not used then 
						encoded_states.append(st)                           #add it to encoded_state list
						assigned_states[state] = st                         #add it to assigned state final list
						break
	 
			for nextState in max_attraction_states[state]:					#now we will move on to the neighbours of the state chosen
				if nextState not in visited_states:							#if not encoded
					gray_list = graycode(assigned_states[state]) 			#find the list of all the encoding that differes in only one place from given state
					
					for st in gray_list:									#for each such gray code
						if (st not in encoded_states):						#if not used early
							encoded_states.append(st)
							assigned_states[nextState] = st                 #use it to encode
							visited_states.append(nextState)
							break                                           #Break out of the loop otherwise

		return assigned_states                                              #return final list of encodings




class state:

	def __init__(self , nextState, inputs, outputs):
		self.state = [nextState,inputs,outputs]




def print_state_assignment(state_assignment):
	encoding_print = []
	for encoding in state_assignment:
		encoding_print_element =''
		for bit in encoding:
			if(bit):
				encoding_print_element+='1'
			else:
				encoding_print_element+='0'

		encoding_print.append(encoding_print_element)

	for i in range(len(state_assignment)):
		print("S"+str(i)+" : "+encoding_print[i])





state_seq=[[[1,(0,0),(0,0)],[2,(1,0),(1,1)]],[[1,(1,0),(0,1)],[2,(0,1),(1,0)]],[[0,(1,1),(0,0)]]]
state_seq1=state_sequencer(3,2,2,state_seq)

nextStateSequence_try,outputSequence_try,inputSequence_try =state_seq1.sequence_matrix()

print("NEXT STATE SEQUENCE")
print(nextStateSequence_try)
print("\n")
print("OUTPUT SEQUENCE")
print(outputSequence_try)
print("\n")
print("INPUT SEQUENCE")
print(inputSequence_try)
print("\n")


attraction_matrix_fanout_try,attraction_matrix_fanin_try = state_seq1.attraction_matrix()

print("FANOUT ALGORITHM:")
print("\n")
print("ATTRACTION_MATRIX")
print(attraction_matrix_fanout_try)
print("\n")

max_attraction_states_try,attraction_sort_try = state_seq1.max_attraction(attraction_matrix_fanout_try)

#print(max_attraction_states_try)
#print(attraction_sort_try)

state_assignment_try = state_seq1.state_assignment(max_attraction_states_try,attraction_sort_try)
print("STATE_ASSIGNMENT")
print_state_assignment(state_assignment_try)
print("\n")

print("FANIN ALGORITHM:")
print("\n")
print("ATTRACTION_MATRIX")
print(attraction_matrix_fanin_try)
print("\n")

max_attraction_states_try,attraction_sort_try = state_seq1.max_attraction(attraction_matrix_fanin_try)
#print(max_attraction_states_try)
#print(attraction_sort_try)

state_assignment_try = state_seq1.state_assignment(max_attraction_states_try,attraction_sort_try)
print("STATE_ASSIGNMENT")
print_state_assignment(state_assignment_try)


		
#sequence would be of the form S1-> an array of states to show the connection in the finite state machine
#thus a list of list of next states corresponding to the indices representing the state