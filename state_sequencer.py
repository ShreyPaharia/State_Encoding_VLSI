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
		
		#This is the manimum number of bits required to encode any number of states
		self.noBits = int(math.ceil(math.log(noStates,2)))       
		
		self.noStates = noStates
		self.noInputs = noInputs
		self.noOutputs = noOutputs
		self.sequence = sequence

		#Initialising the following matrices as numpy zeros matrices
		#This matrix is such that present state represents rows and next state represents column - the entries are the number of inputs for which the present state goes to next state
		self.nextStateSequence = np.zeros((self.noStates,self.noStates))

		#This matrix is such that present state represents rows and outputs while going to the next state represents column - the entries are the number of times an output becomes 1 while going out from the present state      
		self.outputSequence = np.zeros((self.noStates,self.noOutputs))

		#This matrix is such that next state represents rows and inout required for any state to goto next state represents column - the entries are the number of times an input comes for which the present state goes to next state
		self.inputSequence = np.zeros((self.noStates,int(math.pow(2,self.noInputs))))


	def sequence_matrix(self): #Func to find the nextStateSequence, inputSequence and outputSequence
		
		for i in range(self.noStates):
			for state in self.sequence[i]:

				self.nextStateSequence[i][state[0]]+=1
				
				for j in range(self.noOutputs):
					self.outputSequence[i][j]+=state[2][j]

				input_deci = 0 # variable to convert a binary number in the form of tuple into decimal number for input sequence matrix 
				for j in range(self.noInputs):
					input_deci+= state[1][j]*math.pow(2,self.noInputs-j-1)
				self.inputSequence[state[0]][int(input_deci)]+=1

		return self.nextStateSequence,self.outputSequence,self.inputSequence

	def attraction_matrix(self): #Func to find out the attraction matrix for FANIN and FANOUT algorithms

		# The attraction matrix is = (number of bits)*nextStateSequence*(Transpose of nextStateSequence) for fanout and (number of bits)*(Transpose of nextStateSequence)*nextStateSequence for fanin 
		attraction_matrix_fanout = self.noBits*np.matmul(self.nextStateSequence,self.nextStateSequence.T) + np.matmul(self.outputSequence,self.outputSequence.T)
		attraction_matrix_fanin = self.noBits*np.matmul(self.nextStateSequence.T,self.nextStateSequence) + np.matmul(self.inputSequence,self.inputSequence.T)

		return attraction_matrix_fanout,attraction_matrix_fanin

	def max_attraction(self,attraction_matrix): #Func to find out the max_attraction_states & attraction_total
		# max_attraction_states => Has states as rows and the ordered list of n most attracted states in decreasing order corresponding to them
		max_attraction_states = []

		# attraction_total => Sum of the attraction of the n most attracted states corresponding to each state
		attraction_total = []
		i=0
	
		for state_attraction in attraction_matrix:
			# argpartition is used to get the n+1 states(state number) from attraction matrix having maximum attraction using max heap sort 
			ind = np.argpartition(state_attraction,-(self.noBits+1))[-(self.noBits+1):]
			# argsort is used to order the indices in decreasing order of attraction. The whole process has a complexity of log(n)+klog(k) -- n = total number and k = number required
			attraction_states = ind[np.argsort(-state_attraction[ind])]	
			
			#the below if condition is used to ensure that the same state is not in the list of maximum attracted states corresponding to it
			if i in attraction_states:	
				index_1 = np.argwhere(attraction_states == i)
				attraction_states = np.delete(attraction_states, index_1)
			i=i+1	
			attraction_state_n = attraction_states[:self.noBits]

			#appending the sorted rows in a common list 
			max_attraction_states.append(attraction_state_n)

			#find the sum of attraction of the n most attracted states and then sorting them according to the sum using argsort function
			total = 0
			for index in attraction_state_n:
				total += state_attraction[index]

			attraction_total.append(total)

		attraction_sort = np.argsort(-np.array(attraction_total))

		return max_attraction_states,attraction_sort

	def state_assignment(self,max_attraction_states,attraction_sort):  #no idea might need to alter
		encoding_list = list(itertools.product([False, True], repeat=int(self.noBits)))
		encoded_states = []
		assigned_states = [0]*self.noStates
		visited_states = []

		#max_attraction_states,attraction_sort = state_seq.max_attraction()

		for state in attraction_sort:
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
	 
			for nextState in max_attraction_states[state]:
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



# Each instance of state class has a single variable => state represented by a tuple of NextState - integer, inputs - tuple of binary inputs, outputs - tuple of binary outputs
class state:

	def __init__(self , nextState, inputs, outputs):
		self.state = [nextState,inputs,outputs]




def print_state_assignment(state_assignment):

	#encoding_print used to store the list of encodings for each state
	encoding_print = []

	for encoding in state_assignment:
		#used to append either 1 or 0 according to the boolean values in encoding
		encoding_print_element =''
		for bit in encoding:
			if(bit):
				encoding_print_element+='1'
			else:
				encoding_print_element+='0'

		encoding_print.append(encoding_print_element)

	for i in range(len(state_assignment)):
		print("S"+str(i)+" : "+encoding_print[i])




# each sequence has a list of states with a list of state class object corresponding to them

#state_seq=[[[1,(0,0),(0,0)],[2,(1,0),(1,1)]],[[1,(1,0),(0,1)],[2,(0,1),(1,0)]],[[0,(1,1),(0,0)]]]

#Example number-9 page 365 H.L. Somanji
state_seq=[[[0,(0,0),(1,)],[0,(0,1),(1,)],[4,(1,1),(0,)],[1,(1,0),(1,)]],[[0,(0,0),(1,)],[3,(0,1),(0,)],[2,(1,1),(0,)],[2,(1,0),(0,)]],[[2,(0,0),(1,)],[3,(0,1),(0,)],[3,(1,1),(0,)],[3,(1,0),(0,)]],[[0,(0,0),(0,)],[4,(0,1),(0,)],[4,(1,1),(0,)],[0,(1,0),(0,)]],[[2,(0,0),(1,)],[4,(0,1),(0,)],[4,(1,1),(0,)],[0,(1,0),(0,)]]]

# An instance of a state_sequencer class using the constructor defined above
state_seq1=state_sequencer(5,2,1,state_seq)

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

print("STATES SORTED ACCORDING TO ATTRACTION OF N MOST ATTRACTED STATES")
#print(max_attraction_states_try)
print(attraction_sort_try)
print("\n")


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
print("STATES SORTED ACCORDING TO ATTRACTION OF N MOST ATTRACTED STATES")
#print(max_attraction_states_try)
print(attraction_sort_try)
print("\n")

state_assignment_try = state_seq1.state_assignment(max_attraction_states_try,attraction_sort_try)
print("STATE_ASSIGNMENT")
print_state_assignment(state_assignment_try)


		
#sequence would be of the form S1-> an array of states to show the connection in the finite state machine
#thus a list of list of next states corresponding to the indices representing the states