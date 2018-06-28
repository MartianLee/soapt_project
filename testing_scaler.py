
from sklearn import preprocessing
import numpy as np

res = []
listOfMorph = ['가','나','다','라','마']
similarity_dictionary = {}
similarity_array = []

similarity_dictionary['가'] = [0.5, 0.5]
similarity_dictionary['나'] = [0.3, 0.3]
similarity_dictionary['다'] = [0.1, 0.1]
similarity_dictionary['라'] = [0.8, 0.8]
similarity_dictionary['마'] = [0.9, 0.9]
similarity_array.append([0.5, 0.5])
similarity_array.append([0.3, 0.3])
similarity_array.append([0.1, 0.1])
similarity_array.append([0.8, 0.8])
similarity_array.append([0.9, 0.9])

# names = ['id','data']
# formats = ['f8','f8']
# dtype = dict(names = names, formats=formats)
# array = np.array(list(similarity_dictionary.items()), dtype=dtype)

similarity_array = np.array(similarity_array)
min_max_scaler = preprocessing.MinMaxScaler()
scaled_similarity_array = min_max_scaler.fit_transform(similarity_array)

print(similarity_array[0])
print(similarity_array[1])
print(similarity_array[2])

cnt = 0
for row in similarity_array:
  print(cnt, listOfMorph[cnt],listOfMorph[cnt], similarity_dictionary[listOfMorph[cnt]], similarity_array[cnt], row);
  cnt+=1

