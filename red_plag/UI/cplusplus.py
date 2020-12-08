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
#files = sys.argv[1:]
#lines = []
#word_count_vector = []
#lengths = []
def unzip(fil):
    with zipfile.ZipFile(fil, 'r') as zip_ref:
        zip_ref.extractall('.')
    files = [join(fil.__str__()[0:len(fil.__str__())-4], f) for f in listdir(fil.__str__()[0:len(fil.__str__())-4]) if isfile(join(fil.__str__()[0:len(fil.__str__())-4], f))]
    return files

def merge(l):
   ans = ""
   for i in l:
      ans = ans + i
   return ans.replace('\n', ' ')

def eliminate_comments(dat):
    for i in range(len(dat)):
        ind = dat[i].find("/*")
        #print(ind)
        if (ind != -1) :
            #dat[i] = dat[i][0:ind] + "\n"
            j = i
            ind1 = dat[j].find("*/")
            while (ind1 == -1) :
                j = j + 1
                ind1 = dat[j].find("*/")
            #dat[i] = dat[i][0:ind] + "\n"
            for k in range(i+1, j):
                dat[k] = "\n"
            #dat[j] = dat[j][(ind1+1):]
            if (j == i) :
                dat[i] = dat[i][0:ind] + " " + dat[i][(ind1+2):]
            else :
                dat[i] = dat[i][0:ind] + "\n"
                dat[j] = dat[j][(ind1+2):]


    for i in range(len(dat)):
        ind = dat[i].find("//")
        #print(ind)
        if (ind != -1) :
            dat[i] = dat[i][0:ind] + "\n"
    return dat

def remove_functions(data):
    ind7 = data.find("int main")
    #print(ind7)
    globa = data[0:ind7]
    globa = globa + "{"
    functions = {}
    ind = globa.find("{")
    #print(ind)
    #count = 0
    #print(len(globa))
    while (ind != -1):
        if (globa[(ind+1):].find("}")==-1):
            break
        if (globa[(ind+1):].find("{") < globa[(ind+1):].find("}")):
            ind1 = ind
            #print(ind1, "hi")
            while (globa[(ind1+1):].find("{") < globa[(ind1+1):].find("}")):
                #print
                count=ind1+1+globa[(ind1+1):].find("}")
                k=0
                while (ind1+1+globa[(ind1+1):].find("{") < count):
                    #count=count-globa[(ind1+1):].find("{")
                    ind1 = ind1+1 + globa[(ind1+1):].find("{")
                    k=k+1
                    #print k
                for i in range(k):
                    ind1 = ind1+1 + globa[(ind1+1):].find("}")
                #print(ind1)
            ind1 = ind1+1 + globa[(ind1+1):].find("}")
            #print(ind1)
        else:
            ind1 = ind+1 + globa[(ind+1):].find("}")
            #print(ind1)
        #print(ind1)
        #print(ind, "ind")
        ind2 = globa[0:ind].rfind("(")
        #print(ind2, "ind2")
        #print(ind2)
        #count = count + 1
        #if (count == 10):
        #   break
        ind3 = 0
        ind4 = 0
        for c in range(ind2 - 1, 0, -1):
            if (globa[c] != " "):
                ind3 = c
                break
        for c in range(ind3, 0, -1):
            #print(c, "c")
            if (globa[c] == " "):
                ind4 = c + 1
                break
        #print(ind4, ind1+1)
        function = globa[ind4:(ind3+1)]
        functions[function] = globa[(ind+1):ind1]
        #print(function, globa[(ind+1):ind1])
        #print("break")
        globa = globa[0:ind4]+" "+globa[(ind1+1):]
        #print(len(globa), "jk")
        ind = globa.find("{")
        #print(ind)
    #print(data)
    data = globa + " " + data[ind7:]
    #print("hi")
    for w in list(functions.keys()):
        data = data.replace(w, functions[w])
    return data

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
            data = remove_functions(data)
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

def similar(word_count_vector):
    an = [0 for i in range(len(word_count_vector))]
    ad = [an for i in range(len(word_count_vector))]
    final = np.array(ad, dtype=float)
    for i in range(len(word_count_vector)):
        for j in range(len(word_count_vector)):
            #if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))!=0):
             #   val = np.dot(np.array(word_count_vector[i]), np.array(word_count_vector[j])) / (np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))
            #if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))==0):
             #   val=1.0;
             val = 1-np.linalg.norm(np.array(word_count_vector[i]) - np.array(word_count_vector[j]))/max(np.linalg.norm(np.array(word_count_vector[i])), np.linalg.norm(np.array(word_count_vector[j])))
             final[i][j] = val
    return final

def evaluate(zip):
    files = unzip(zip)
    [word_count_vector, lengths] = find_signature(files)
    [word_count_vector, final_length] = sort_pad(lengths, word_count_vector)
    #word_count_vector = normalize(word_count_vector, final_length)
    final = similar(word_count_vector)
    print(final)
    return final
final = evaluate(sys.argv[1])
y = str(sys.argv[1])
z = len(y)-4
LIST = os.listdir(y[:z])
print(LIST)
def csv_write(final):
    file = open('REDPLAG.csv', 'wb')
    file1 = open('REDPLAG.csv', 'a+', newline ='')
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
    fig = plt.figure()
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
    fig.savefig('REDPLAG.png', bbox_inches='tight', dpi=150)

# Loop over data dimensions and create text annotations.
    ax.set_title("RESULT")
    plt.show()
plots(final)
final = final.astype('str')
csv_write(final)
