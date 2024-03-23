import numpy as np

filenames = ["1.ABC.txt", "2.wowo.doc", "3. yeye.man"]
print(filenames)

#filenames = np.asarray(filenames)
filenames = np.asarray([file.replace(".", "-", 1) for file in filenames])

#for i in range(len(filenames)):
  #  filenames[i] = 1

for file in filenames:
    file = file.replace(".", "-", 1)
print(filenames)