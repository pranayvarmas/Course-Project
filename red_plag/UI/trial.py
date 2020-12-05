import sys
import numpy as np
import re
import zipfile
import csv
from os import listdir
from os.path import isfile, join
if(len(sys.argv)>1):
    with zipfile.ZipFile(sys.argv[1], 'r') as zip_ref:
        zip_ref.extractall('.')
    files = [join(sys.argv[1].__str__()[0:len(sys.argv[1].__str__())-4], f) for f in listdir(sys.argv[1].__str__()[0:len(sys.argv[1].__str__())-4]) if isfile(join(sys.argv[1].__str__()[0:len(sys.argv[1].__str__())-4], f))]

lines = []
word_count_vector = []
lengths = []
def merge(l):
   ans = ""
   for i in l:
      ans = ans + i
   return ans.replace('\n', ' ')
for file in files:
    with open(file, 'r') as f:
        #data = f.read().replace('\n', ' ')
        #print(data)
        dat = f.readlines()
        #print(dat)
        for i in range(len(dat)):
            ind = dat[i].find("#")
            #print(ind)
            if (ind != -1) :
               dat[i] = dat[i][0:ind] + "\n"
            #print(l)
        #print(dat)
        data = merge(dat)
        #print(data)
        data = re.sub(r'[^\w]', ' ', data)
        lines.append(data)
        words = data.split(' ')
        words_unique = list(np.unique(np.array(words)))
        freq = {w : 0 for w in words_unique}
        for word in words:
            freq[word] = freq[word] + 1
        freq.pop('')
        word_count_vector.append(list(freq.values()))
        lengths.append(len(freq))
#print(word_count_vector)
#print(lengths)
if(len(sys.argv)<=1):
    print("ADD ARGUMENTS")
if(len(lengths)!=0):
    final_length = max(lengths)
    for w in word_count_vector:
        if (len(w) == final_length):
            w.sort()
            continue
        else:
            num = final_length - len(w)
            for i in range(num):
                w.append(0)
            w.sort()

#print(word_count_vector)
    final_word_count = [[] for j in range(final_length)]

    for w in word_count_vector:
        for i in range(final_length):
            final_word_count[i].append(w[i])

    means = [np.mean(np.array(final_word_count[j])) for j in range(final_length)]
    stds = [np.std(np.array(final_word_count[j])) for j in range(final_length)]
#print(means)
#print(stds)
    for w in word_count_vector:
        for i in range(final_length):
            if (stds[i] == 0):
                continue
            w[i] = (w[i] - means[i])/stds[i]

#print(word_count_vector)
    an = [0 for i in range(len(word_count_vector))]
    ad = [an for i in range(len(word_count_vector))]
    final = np.array(ad, dtype=float)
    for i in range(len(word_count_vector)):
        for j in range(len(word_count_vector)):
            if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))!=0):
                val = np.dot(np.array(word_count_vector[i]), np.array(word_count_vector[j])) / (np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))
            if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))==0):
                val = 1
            final[i][j] = val
print(final)
final = final.astype('str')
#print(np.dot(np.array(word_count_vector[0]), np.array(word_count_vector[0])) / (np.linalg.norm(np.array(word_count_vector[0]))*np.linalg.norm(np.array(word_count_vector[0]))))
file = open('comparision.csv', 'wb')
file1 = open('comparision.csv', 'a+', newline ='')
l = [i for i in range(0,len(lengths)+1)]
for i in range(0, len(l)):
    if(i==0):
        l[i] = 'files'
    if(i!=0): 
        l[i] = 'w.r.t file'+str(l[i])
arr = [i for i in range(1,len(lengths)+1)]
for i in range(0,len(arr)):
    arr[i] = 'file' + str(arr[i])
print(arr)
arr = np.array(arr)
result = np.hstack((final, np.atleast_2d(arr).T))
for i in range(len(lengths)):
    result[:, [len(lengths)-i, len(lengths)-i-1]] = result[:, [len(lengths)-i-1, len(lengths)-i]]
print(result) 
# writing the data into the file
i=0
with file1:
    if(i==0):
        write = csv.writer(file1) 
        write.writerow(l) 
        i=1
    if(i!=0):        
        write = csv.writer(file1) 
        write.writerows(result)