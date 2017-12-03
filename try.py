import numpy as np

import numpy_indexed as npi

a = np.array([[8,7,3],[9,1,4],[ 21,3,8]])

b = np.array([[1,2,3],[1,2,3],[ 1,2,3]]) 

array = np.vstack(([a.T], [b.T])).T

i=0
ind = []
tot = []

for a_1 in a:
	ind_1 = np.argpartition(a_1,-2)[-2:]
	total = 0
	for index in ind_1:
		total += a_1[index]
	tot.append(total)
	ind.append(ind_1[np.argsort(-a_1[ind_1])])

sorted_ind = np.argsort(-np.array(tot))


print(ind)
print(tot)
print(sorted_ind)
#array.sort(order=index,axis=1)


array_new = []
# for i in range(5):
# 	array_new.append((i,array[i]))

#print(array)


# print(a1)

# print(a[npi.argsort((a[:,1], -a[:,0]))])


# arr1 = [0]*5

# arr2 = [arr1]*5

# arr2_1 = np.array(arr2)

# my_array = np.array([(1,2,3),(2,3,4),(3,4,5)])

# ans = np.matmul(arr2_1,arr2_1.T)

# print(arr1)

# print(arr2)

# print(ans)
#adding a line
#adding a line#adding a line again
#adding line for experiment branch
