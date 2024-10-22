#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:58:33 2023

@author: kyogonagashima
"""

count = 0 #changed from 0
TS = 1
masterList = []
distances = []
PeriodicTable = {1:'H', 5:'B', 6:'C', 7:'N',8:'O', 9:'F', 15:'P', 16:'S', 17: 'Cl', 24:'Cr', 26:'Fe', 27:'Co', 28:'Ni', 35:'B', 42: 'Mo', 44: 'Ru', 45: 'Rh', 46:'Pd', 75:'Re', 77:'Ir', 78:'Pt'}

totalCount = 0
list=[] 


def openFile():
    from sys import argv
    path = argv[1]
    print(path) #/Users/kyogonagashima/Desktop/Files/IRC.txt
    
    
    print(getInfo(open(path, 'r'))) 
    
    scanIRC(open(path, 'r'))
    print('count: ', end ='')
    print(count)

def getInfo(file):
    global totalCount
    global TS
    reversePathComplete = False
    
    for line in file:
        
        line = line.strip()
        if line == 'Calculation of REVERSE path complete.':
            reversePathComplete = True
        if line == 'Calculation of FORWARD path complete.':
            print('first-half complete')
            if (TS == 1):
                TS += totalCount
                print('TS: ', end ='')
                print(TS)
            else:
                TS += 0 
        
        # Finding starting keyword
        if line=='Input orientation:' and not reversePathComplete:
            totalCount+=1
            
    return TS

def scanIRC(file):
    #variables
    global count
    global TS
    forwardPathComplete = False
    
    from sys import argv
    interval = int(argv[2])
    
    skippedFirst = False
    firstHalfDone = False
    midPoint = False
    index = totalCount - TS+1
    print('initial index: ', end = '')
    print(index)
    
    print('totalCount: ', end = '')
    print(totalCount)
    keyFound = False 
    skipLines = 0
    
    
    for line in file:
        line = line.strip()
        
        if line == 'Calculation of FORWARD path complete.':
            print('calculation of forward path complete')
            forwardPathComplete = True

        # Finding starting keyword 
        if not keyFound:
            
            if line == 'Input orientation:':
                
                # if not skippedFirst:
                #     skippedFirst= True
                #     continue
                
                # if firstHalfDone and not skippedSecond:
                #     skippedSecond = True
                #     continue
                
                
            
                count+=1 
                
                if not forwardPathComplete: #and firstHalfComplete
                    index+=1 
                else:
                    firstHalfDone = True
                    if midPoint == False:
                        midPoint = True
                        index = totalCount - TS +2  ##index = totalCount - TS -2 or try totalCount-TS
                        count = 2
                if firstHalfDone:
                    index-=1
                    
                if count%interval!=1: 
                    None
                else:
                    if index>0:
                        if index<10:
                            strIndex = '0'+'0'+str(index)
                        if index<100:
                            strIndex = '0'+str(index)
                        else:
                            strIndex = str(index)
                        fileName = 'You_Thioketone_S_6memring_'+strIndex+'.com'
                        with open(fileName, 'w') as txtFile:
                            txtFile.write('%nprocshared=10'+'\n'+'%mem=12GB'+'\n'+'# b3lyp/genecp empiricaldispersion=gd3 pop=hirshfeld'+'\n'+'\n'+'Title Card Require'+'\n'+'\n'+'0 1'+'\r')

                skipLines = 0
                keyFound = True
                continue
        
        
        
        # After starting keyword is found
        else:
            if line == 'Distance matrix (angstroms):'or line.split()[0] == 'Rotational':
                keyFound = False
                continue
            else:
                if skipLines >= 4:
                    if count%interval!=1: 
                            None 
                    else:
                        if index>0:
                            if line =='---------------------------------------------------------------------':
                                line = 'Pd Fe 0'+'\r'+'LANL2DZ'+'\r'+'****'+'\r'+'-C -H -P -Br -N -O -F -S 0'+'\r'+'def2svp'+'\r'+'****'+'\r'+'\r'+'Pd Fe 0'+'\r'+'LANL2DZ'+'\r'+'\r'+'\r'+'\r'+'\r'+'\r'
                            else:
                                
                                list = line.split()
                                atomNum= list[1]
                                element = PeriodicTable.get(int(atomNum))
                                
    
                                atomNum = atomNum.strip()
                                x = list[3]
                                y = list[4]
                                z = list[5]
                                
                                line =''
                        
                            with open(fileName, 'a') as txtFile:
                                
                                txtFile.write(element+'   '+x+'   '+y+'  '+z+'\n'+line)
                                
                                element = ''
                                x=''
                                y=''
                                z=''
                        
                else:
                    skipLines+=1
                   
    file.close()    


def main():
    openFile() 

  

if __name__ == "__main__":
  main()









