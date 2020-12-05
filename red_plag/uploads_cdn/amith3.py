import numpy as np
import csv
import math

with open('mumbai_data.csv', newline='') as csvfile:
    data = np.array(list(csv.reader(csvfile)),dtype='object')
with open('mumbai_unlock.csv', newline='') as csvfile:
    dat = np.array(list(csv.reader(csvfile)),dtype='object')
data[0][1]="Infected(Unlock)"
data[0][2]="Infected(Lock)"
data[0][3]="Positivity Rate(Lock)"
data[0][4]="Positivity Rate(UnLock)"
for i in range(1,8):
   b=int(data[i][2])/int(data[i][1])
   data[i][3]=format(b,'0.3f')
for i in range(1,8):
   data[i][1]=dat[i][2]
for i in range(1,8):
   b=int(dat[i][2])/int(dat[i][1])
   data[i][4]=format(b,'0.3f')
with open("info_combine.csv", 'w+') as f:
    write = csv.writer(f)
    for i in range(8):
       write.writerow(data[i])

