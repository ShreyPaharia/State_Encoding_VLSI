import numpy as np
arr = np.array((1,3,2,5,4,7,8))
print(arr[:4])

arr1 = (0,0,1)

print(arr1[0])

header = ['Brand', 'Modell', 'Year', 'Color']

car = ['Ford','Mustang','1966','red']

print("\t".join(header) + "\n" + "\t".join(car))
##just wanna add a line