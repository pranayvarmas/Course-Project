import sys ,os
import numpy as np
import re
import zipfile
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir
from os.path import isfile, join
global z
z=[]
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

def edit_functions(dat):
    functions = {}
    for i in range(len(dat)-1):
        if (dat[i].find("def") != -1):
            ind1 = dat[i].find("def") + 3
            for k in range(ind1+1, len(dat[i])):
                if (dat[i][k] != " "):
                    ind1 = k
                    break
            ind2 = 0
            for k in range(ind1, len(dat[i])):
                if (dat[i][k] == " " or dat[i][k] == "("):
                    ind2 = k - 1
                    break
            function = dat[i][ind1:(ind2+1)]
            ind3 = dat[i].find(":")
            definition = ""
            for k in range(ind3+1, len(dat[i])-2):
                if (dat[i][k] != " "):
                    ind4 = i
                    definition = dat[i][ind4:]
                    break
            if (definition != ""):
                functions[function] = definition
                dat[i]= dat[i][0:ind1] + "\n"
                continue
            else:
                for k in range(len(dat[i+1])):
                    if (dat[i+1][k] != " "):
                        ind4 = k
                        break

                ind6 = 0
                for k in range(i+1, len(dat)):
                    for l in range(len(dat[k])):
                        if (dat[k][l] != " "):
                            ind5 = l
                            break
                    if (ind4 > ind5):
                        ind6 = k - 1
                        break
                definition = merge(dat[i:(ind6+1)])
                #print(function, "hi")
                functions[function] = definition
                #print(function, definition)
                dat[i]= dat[i][0:ind1] + "\n"
                for g in range(i+1, ind6+1):
                    dat[g] = "\n"
    return [dat, functions]

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
            [dat, functions] = edit_functions(dat)
            data = merge(dat)
            for w in list(functions.keys()):
                data.replace(w, functions[w])
            #print(w)
            #print(data)
            #print(functions)
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
            #if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))!=0):
             #   val = np.dot(np.array(word_count_vector[i]), np.array(word_count_vector[j])) / (np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))
            #if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))==0):
             #   val=1.0;
            val = 1-np.linalg.norm(np.array(word_count_vector[i]) - np.array(word_count_vector[j]))/max(np.linalg.norm(np.array(word_count_vector[i])), np.linalg.norm(np.array(word_count_vector[j])))
            final[i][j] = val*100
            if(final[i][j]>100):
                final[i][j]=100
    return final
def evaluate(zip):
    files = unzip(zip)
    [word_count_vector, lengths] = find_signature(files)
    [word_count_vector, final_length] = sort_pad(lengths, word_count_vector)
    #word_count_vector = normalize(word_count_vector, final_length)
    final = similar(word_count_vector)
    #print(final)
    return final
#print(np.dot(np.array(word_count_vector[0]), np.array(word_count_vector[0])) / (np.linalg.norm(np.array(word_count_vector[0]))*np.linalg.norm(np.array(word_count_vector[0]))))
[final,LIST] = evaluate(sys.argv[1])
LIST=os.listdir(str((sys.argv[1][:(len(sys.argv[1]))-4])))
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
    ax = sns.heatmap(final, linewidth=0.5,cmap="hot",vmin =0,vmax =100,annot =True,fmt='g')
    ax.set_xticks(np.arange(len(LIST)))
    ax.set_yticks(np.arange(len(LIST)))
# ... and label them with the respective list entries
    ax.set_xticklabels(LIST)
    ax.set_yticklabels(LIST)
    ax.set_title("RESULT")
# Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), rotation=360, ha="right",
        rotation_mode="anchor")
    fig.savefig('REDPLAG.png', bbox_inches='tight', dpi=150)

# Loop over data dimensions and create text annotations.
    plt.show()
final = final.astype('int')
plots(final)
csv_write(final)
