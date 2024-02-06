import numpy as np
array6 = np.array([(1, 0), (1, -1)])
array7 = np.array([(1, -1), (0, -1)])
array8 = np.array([(-1, -1), (0, -1)])

direction_array = np.array([])
  
for dx, dy in [(-1, -1), (0, -1)]:
    direction_array = np.append(direction_array, np.array([dx, dy]))
direction_array = direction_array.reshape(-1, 2)
result1 = np.array_equal(array8, direction_array)
print(array8)
print(direction_array)
print(result1)