
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 16:51:30 2023

@author: kyogonagashima
"""
import os
import matplotlib.pyplot as plt

keyFound = False
step = 0
step_taken = 0
count = 0
dict = {}

def scanDir():
    from sys import argv
    path = argv[1]
    fileList = sorted(os.listdir(path))
    for file_name in fileList:
        if file_name.endswith('.out'):
            print(file_name)
            openFile(file_name, path)

def openFile(file_name, path):
    getInfo(open(path+'/'+file_name, 'r'))
    scanFile(open(path+'/'+file_name, 'r'))
    

def getInfo(file):
    global keyFound
    global count 
    global skipLines
    global step
    
    step = 0
    
    for line in file:
        
        line = line.strip()
        
        # Finding starting keyword

        if line=='Hirshfeld charges, spin densities, dipoles, and CM5 charges using IRadAn=      5:':
            step+=1


def scanFile(file):

    global keyFound
    global count
    global skipLines
    global step
    
    step_taken = 0
    skipLines = 0

    
    for line in file:
        line = line.strip()

        
        # Finding starting keyword
        if not keyFound:
            if line=='Hirshfeld charges, spin densities, dipoles, and CM5 charges using IRadAn=      5:':
                step_taken+=1
                if step==step_taken:
                    count+=1
                    
                keyFound = True
                continue
        
        # After starting keyword is found
        else:
            
            if line == 'Hirshfeld charges with hydrogens summed into heavy atoms:':
                keyFound = False
                continue
            else:
                if skipLines >= 1:
                    lineScan(line)
                else:
                    skipLines+=1

    file.close()    

def lineScan(line):
    list = line.split()
    atomNum = list[0]
    if atomNum == 'Tot':
        return
    atomNum = atomNum.strip()
    HQ = list[2]
    if dict.get(atomNum) is None:
        dict[atomNum] = []
        dict.get(atomNum).append(float(HQ))
    else:
        dict.get(atomNum).append(float(HQ))
        

def constrTable():
    global dict
    global count

    for k in range(len(dict)+1):
        print(k, end = ' ')
    
    print('\r')        
    for i in range(count):
        number = i+1
        print(number, end=' ')
        for value in dict.values():
            print(value[i], end=' ')
        print('\r')

        
def plot(atomNum):
    global dict
    global count
    
    x=[]
    
    from sys import argv
    #atomNum = argv[3]
    direction = argv[2]  
    
    y=dict.get(str(atomNum))
    
    if direction == 'forward':
        for i in range(count):
            x.append(i)
    if direction == 'backward':
        for i in range(count, 0, -1):
            x.append(i)
    plt.scatter(x, y)
    plt.ylabel('Hirshfeld Charges')
    plt.xlabel('IRC#')
    plt.title('BetaHydride_Pd_Ethylene_CH3_HQ: '+str(atomNum))
    plt.show()
    
    

def main():
    scanDir()
    constrTable()
    print(len(dict))
    for i in range(1,len(dict)+1,1):
        plot(i)

  

if __name__ == "__main__":
  main()










