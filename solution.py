import sys, csv, math
from array import *

def calculateE(col):
    
    vrijednosti = {}
    rez =0
    for e in col:
        if e not in vrijednosti.keys():
            vrijednosti[e] = 1
        else:
            vrijednosti[e]+=1
    if len(vrijednosti)>1:
        for k,v in vrijednosti.items():
            rez += -(v/(len(col))*math.log2(v/(len(col))))

    return rez

def calculateIG(col, last_col, E):
    vrijednosti = {}
    
    rez =0
    for i in range (len(col)):
        if col[i] not in vrijednosti.keys():
            vrijednosti[col[i]] = []
            vrijednosti[col[i]].append(last_col[i])
        else:
            vrijednosti[col[i]].append(last_col[i])

    for k,v in vrijednosti.items():
        E2 = calculateE(v)
        
        rez += E2 * (len(v)/len(col))
        

    rez = E - rez
    return rez

def make_tree(header, rows, cvor, depth):
    
    last_col = []
    for e in rows:
        last_col.append(e[-1])
    E = calculateE(last_col)

    if E == 0:
        ispis = " " + rows[0][-1]
        while cvor.parent != None:
            ispis = " " + str(cvor.dubina)+ ":" + cvor.name + ispis
            cvor = cvor.parent
        ispis = str(cvor.dubina) + ":" + cvor.name + ispis
        tree.append(ispis)
        return 0
    else:
        max_IG = [0,0]
        for i in range (len(rows[0])-1):
            col = [sub[i] for sub in rows]
            IG = calculateIG(col, last_col, E)
            #print("IG: ",IG)
            if IG > max_IG[0]:
                max_IG[0] = IG
                max_IG[1] = i
        #print("max_IG: ", max_IG)
        vrijednosti = {}
        new_header = header.copy()
        name_CV = new_header.pop(max_IG[1])
        for i in range (len(rows)):
            if rows[i][max_IG[1]] not in vrijednosti.keys():
                vrijednosti[(rows[i][max_IG[1]])] = []
                k = rows[i].pop(max_IG[1])
                vrijednosti[k].append(new_header)
                vrijednosti[k].append(rows[i])
            else:
                k = rows[i].pop(max_IG[1])
                vrijednosti[k].append(rows[i])
        
        for k,v in vrijednosti.items():
            name = name_CV + "=" + k
            if cvor is None:
                cvor_new = Cvor(name, 1, cvor)
            else:
                cvor_new = Cvor(name, cvor.dubina+1, cvor)
            
            if((depth is not None) and (int(cvor_new.dubina) == int(depth))):
                #ispis=make_branch(cvor_new, vrijednosti)
                last_col = []
                for e in v[1:]:
                    last_col.append(e[-1])
                E = calculateE(last_col)
                if E == 0:
                    ispis = " " + v[1][-1]
                    
                else:
                    max_oc = 0
                    for e in last_col:
                        oc = last_col.count(e)
                        if oc > max_oc:
                            value = e
                            max_oc = oc
                        if oc == max_oc:
                            value = min(value, e)
                    ispis = " " + value
                    
                cvor2=cvor_new
                while cvor2.parent != None:
                    ispis = " " + str(cvor2.dubina)+ ":" + cvor2.name + ispis
                    cvor2 = cvor2.parent
                ispis = str(cvor2.dubina) + ":" + cvor2.name + ispis
                tree.append(ispis)
            else:
                
                make_tree(v[0], v[1:], cvor_new, depth)
            
def make_predictions(header, rows):
    branches= []
    predictions = []
    for e in tree:
        e2 = e.split(" ")
        branch = []
        for i in range (len(e2)-1):
            node = (e2[i].split(":"))
            branch.append(node[1])
        branch.append(e2[-1])    
        branches.append(branch)

   
    for i in range (len(rows)):
        item = []
        for j in range (len(header)-1):
            item.append(header[j]+"="+rows[i][j])
       
        for e in branches:
            prediction = e[-1]
            e = e[:-1]
            if all(x in item for x in e):
                predictions.append(prediction)
                break
            
    return predictions
        
def accuracy_cm(predictions, rows):
    matches = 0
    cm_hd = []
    for i in range (len(rows)):
        if rows[i][-1] not in cm_hd:
            cm_hd.append(rows[i][-1])
        if predictions[i] not in cm_hd:
            cm_hd.append(predictions[i])
        
        if rows[i][-1] == predictions[i]:
            matches+=1
    cm_hd.sort()
    r, c = (len(cm_hd), len(cm_hd))
    cm = [[0 for i in range(c)] for j in range(r)]
    
    for i in range (len(rows)):
        if rows[i][-1] == predictions[i]:
            index = cm_hd.index(rows[i][-1])
            cm[index][index]+=1
        else:
            index1 = cm_hd.index(rows[i][-1])
            index2 = cm_hd.index(predictions[i])
            cm[index1][index2]+=1
    acc = matches/len(rows)
    return acc, cm
    
def format_data(train_dataset):
    file = open(train_dataset)
    csvreader = csv.reader(file)
    header = next(csvreader)
    
    rows = []
    for row in csvreader:
        i = 0
        rows.append(row)
    file.close()
    return header, rows

class Cvor():
    def __init__(self, name, dubina, parent):
        self.name = name
        self.dubina=dubina
        self.parent=parent

class ID3():
    
    def fit(self,train_dataset):
        header, rows = format_data(train_dataset)
        if "depth" in globals():
            if (int(depth) == 0):
                last_col = []
                for e in rows:
                    last_col.append(e[-1])
                E = calculateE(last_col)
                if E == 0:
                    ispis = "" + v[1][-1]
                    
                else:
                    max_oc = 0
                    for e in last_col:
                        oc = last_col.count(e)
                        if oc > max_oc:
                            value = e
                            max_oc = oc
                        if oc == max_oc:
                            value = min(value, e)
                    ispis = "" + value
                tree.append(ispis)
            else:
                make_tree(header, rows, None, depth)
        else:
            make_tree(header, rows, None, None)
        print("[BRANCHES]:")
        print(*tree, sep = "\n")
        return 0
    
    def predict(self, test_dataset):
        header, rows = format_data(test_dataset)
        predictions = make_predictions(header, rows)
        print("[PREDICTIONS]:", end = " ")
        print(*predictions)
        acc, cm = accuracy_cm(predictions, rows)
        print("[ACCURACY]: {0:.5f}".format(acc))
        print("[CONFUSION_MATRIX]:")
        for row in cm:
            for val in row:
                print(str(val), end = " ")
            print()
        return 0
    
tree = []

n = len(sys.argv)
train_dataset = sys.argv[1]
test_dataset = sys.argv[2]
if n==4:
    depth = sys.argv[3]

model = ID3()
model.fit(train_dataset)
predictions = model.predict(test_dataset)

