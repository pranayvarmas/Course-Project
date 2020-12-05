import numpy as np
import csv
import math

with open('mumbai_data.csv', newline='') as csvfile:
    data = np.array(list(csv.reader(csvfile)))
arr1=np.array(["Field","Tests","Infected","Recovered","Deceased"])
arr2=["Mean",3,4,5,6]
arr3=["Std. Dev.",4,5,6,7]
mean=0
i=1
for j in range(1,5):
   for k in range(1,8):
      mean=mean+int(data[k][j])
   a=mean/7
   arr2[i]=round(a,3)
   i=i+1
i=1


var=0
for j in range(1,5):
   for k in range(1,8):
      var=(int(data[k][j])-arr2[j])*(int(data[k][j])-arr2[j])+var
   b=var/7
   std=math.sqrt(b)
   arr3[i]=round(std,3)
   i=i+1
def print_table(table):
    col_width = [max(len(str(x)) for x in col) for col in zip(*table)]
    for line in table:
        print ("  " + "  ".join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line)))

table = [(str(arr1[i]), str(arr2[i]), str(arr3[i])) for i in range(5)]
print_table(table)
