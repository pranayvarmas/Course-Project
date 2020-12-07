import sys ,os
import numpy as np
import re
import zipfile
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir
from os.path import isfile, join
x = 0
def unzip(fil):
    
    with zipfile.ZipFile(fil, 'r') as zip_ref:
        zip_ref.extractall('.')
    files = [join(fil.__str__()[0:len(fil.__str__())-4], f) for f in listdir(fil.__str__()[0:len(fil.__str__())-4]) if isfile(join(fil.__str__()[0:len(fil.__str__())-4], f))]
    return files

#lines = []
def merge(l):
   ans = ""
   for i in l:
      ans = ans + i
   return ans.replace('\n', ' ')

def eliminate_comments(dat):
    for i in range(len(dat)):
        ind = dat[i].find("#")
        #print(ind)
        if (ind != -1) :
            dat[i] = dat[i][0:ind] + "\n"
    return dat
def set_globvar(lengths):
    global x   # Needed to modify global copy of globvar
    x = len(lengths)
def find_signature(files):
    word_count_vector = []
    lengths = []
    for file in files:
        with open(file, 'r') as f:
        #data = f.read().replace('\n', ' ')
        #print(data)
            dat = f.readlines()
        #print(dat)
            dat = eliminate_comments(dat)
            #print(l)
        #print(dat)
            data = merge(dat)
        #print(data)
            data = re.sub(r'[^\w]', ' ', data)
        #lines.append(data)
            words = data.split(' ')
            words_unique = list(np.unique(np.array(words)))
            freq = {w : 0 for w in words_unique}
            for word in words:
                freq[word] = freq[word] + 1
            freq.pop('')
            word_count_vector.append(list(freq.values()))
            lengths.append(len(freq))
            set_globvar(lengths)
    return [word_count_vector, lengths]
#print(word_count_vector)
#print(lengths)
def sort_pad(lengths, word_count_vector):
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
    return [word_count_vector, final_length]

#print(word_count_vector)
def normalize(word_count_vector, final_length):
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
    return word_count_vector
#print(word_count_vector)
def similar(word_count_vector):
    an = [0 for i in range(len(word_count_vector))]
    ad = [an for i in range(len(word_count_vector))]
    final = np.array(ad, dtype=float)
    for i in range(len(word_count_vector)):
        for j in range(len(word_count_vector)):
            if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))!=0):
                val = np.dot(np.array(word_count_vector[i]), np.array(word_count_vector[j])) / (np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))
            if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))==0):
                val=1.0;
            final[i][j] = val
    return final

def evaluate(zip):
    files = unzip(zip)
    [word_count_vector, lengths] = find_signature(files)
    [word_count_vector, final_length] = sort_pad(lengths, word_count_vector)
    word_count_vector = normalize(word_count_vector, final_length)
    final = similar(word_count_vector)
    return final
#print(np.dot(np.array(word_count_vector[0]), np.array(word_count_vector[0])) / (np.linalg.norm(np.array(word_count_vector[0]))*np.linalg.norm(np.array(word_count_vector[0]))))
final = evaluate(sys.argv[1])
zip = zipfile.ZipFile(sys.argv[1])
# available files in the container
LIST = zip.namelist()[:]
del LIST[0]
def csv_write(final):
    file = open('comparision.csv', 'wb')
    file1 = open('comparision.csv', 'a+', newline ='')
# writing the data into the file
    l = [i for i in range(0,x+1)]
    for i in range(0, len(l)):
        if(i==0):
            l[i] = 'files'
        if(i!=0): 
            l[i] = 'w.r.t '+str(LIST[i-1])
    arr = [i for i in range(1,x+1)]
    for i in range(0,len(arr)):
        arr[i] = str(LIST[i])
    arr = np.array(arr)
    result = np.hstack((final, np.atleast_2d(arr).T))
    for i in range(x):
        result[:, [x-i, x-i-1]] = result[:, [x-i-1, x-i]] 
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
def plots(final):
    ax = sns.heatmap(final, linewidth=0.5,cmap="hot")
    ax.set_xticks(np.arange(len(LIST)))
    ax.set_yticks(np.arange(len(LIST)))
# ... and label them with the respective list entries
    ax.set_xticklabels(LIST)
    ax.set_yticklabels(LIST)

# Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), rotation=360, ha="right",
        rotation_mode="anchor")

    plt.show()

# Loop over data dimensions and create text annotations.
    ax.set_title("RESULT")
    plt.show()
plots(final)
final = final.astype('str')
csv_write(final)

