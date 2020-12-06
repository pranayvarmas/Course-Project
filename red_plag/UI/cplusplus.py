import sys
import numpy as np
import re
files = sys.argv[1:]
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
            #print(l)
        data = merge(dat)
        #print(data)
        #data = data.replace("\t", " ")
        #data = data.replace("_", "a")
        #data = re.sub(r'[^\w]', ' ', data)
        ind7 = data.find("int main")
        #print(ind7)
        globa = data[0:ind7]
        functions = {}
        ind = globa.find("{")
        #print(ind)
        #count = 0
        #print(len(globa))
        while (ind != -1):
            if (globa[(ind+1):].find("{") < globa[(ind+1):].find("}")):
                ind1 = ind+1 + globa[(ind+1):].find("}")
                #print(ind1, "hi")
                while (globa[(ind1+1):].find("{") < globa[(ind1+1):].find("}")):
                    #print
                    count=globa[(ind1+1):].find("}")
                    k=1
                    while (globa[(ind1+1):].find("{") < count):
                        count=count-globa[(ind1+1):].find("{")
                        ind1 = ind1+1 + globa[(ind1+1):].find("{")
                        k=k+1
                        #print k
                    for i in range(k):
                        ind1 = ind1+1 + globa[(ind1+1):].find("}")
                    #print(ind1)
                ind1 = ind1+1 + globa[(ind1+1):].find("}")
                #print(ind1)
            else:
                ind1 = ind1+1 + globa[(ind+1):].find("}")
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
            print(function, globa[(ind+1):ind1])
            print("break")
            globa = globa[0:ind4]+" "+globa[(ind1+1):]
            #print(len(globa), "jk")
            ind = globa.find("{")
            #print(ind)
        #print(data)
        data = globa + " " + data[ind7:]
        #print("hi")
        for w in list(functions.keys()):
            data = data.replace(w, functions[w])
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
        val = np.dot(np.array(word_count_vector[i]), np.array(word_count_vector[j])) / (np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))
        final[i][j] = val
print(final)
#print(np.dot(np.array(word_count_vector[0]), np.array(word_count_vector[0])) / (np.linalg.norm(np.array(word_count_vector[0]))*np.linalg.norm(np.array(word_count_vector[0]))))
