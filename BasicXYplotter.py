# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:25:38 2019

@author: Espen
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['axes.formatter.useoffset'] = False

def Reader(filename,bindingEnergy, workFunc = 4.31, exEnergy = 1486.61): 
    #Leser inn alle plots som ligger i en xy-fil med navn filename
    # bindingEnergy: boolsk: vil du ha binding energy??
    x = []
    y = []
    f = open(filename,"r")
    xTemp=[]
    yTemp=[]
    for el in f.readlines():
        if el=='\n':
            x.append(xTemp)
            y.append(yTemp)
            xTemp=[]
            yTemp=[]
            continue
        elif el.split()[0]!="#" and float(el.split()[0]) and bindingEnergy:
            xTemp.append(exEnergy-float(el.split()[0]))
            yTemp.append(float(el.split()[1]))
        elif el.split()[0]!="#" and float(el.split()[0]) and not bindingEnergy:
            xTemp.append(float(el.split()[0]))
            yTemp.append(float(el.split()[1]))
    f.close()
    return averager(x,y, len(x))
    
def averager(_x,_y, N): 
    #Regner ut gjennomsnitt av alle cps-verdier, gjør det lettere å hanskes med
    #Input:
    # _x: liste med x-verdier (energier)
    # _y: liste med y-verdier (cps)
    # N: Antall scans N=(len(_x)) mest for debugging/analyse, ikke særlig viktig
    
    #Return:
    # 1D-liste med x-verdier
    # 1D-liste med gjennomsnitt av y-verdiene i hver scan
    av = True
    for i in range(1,len(_x)):
        if _x[0]!=_x[i]:
            av = False
            print("Not a match!")
            return None, None, None
    if av:
        yAvgTemp = []
        for i in range(len(_y[0])):
            s = 0
            for j in range(len(_y)):
                s +=_y[j][i]
            yAvgTemp.append(s/len(_y))
    #print(*yAvgTemp,sep="\n")
    return _x[0],yAvgTemp, N


def Plot(filename, size=(10,6),col="r", bindingEnergy=True, XPS=True, save=False):
    # XPS == True --> xps-data som input
    # XPS == False --> ups-data som input
    plt.style.use("default")
    #X,Y,cts = Reader(filename, bindingEnergy)
    if not XPS: 
        X,Y,cts = Reader(filename, bindingEnergy,exEnergy= 21.2182)
    else: 
        X,Y,cts = Reader(filename, bindingEnergy)
    print(f"{cts} scans")
    
    matplotlib.rcParams['axes.formatter.useoffset'] = False
    fig = plt.figure(figsize=size)
    plt.plot(X,Y,col,linewidth=0.5)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.ylim()
    plt.ylabel("Intensity [counts per second]")
    if bindingEnergy: 
        plt.gca().invert_xaxis()
        plt.xlabel("Binding energy [eV]")
    elif not bindingEnergy: plt.xlabel("Kinetic energy[eV]")

    if save:
        fig.savefig("imgs/"+str(filename.split("/")[3][:-3])+".png")
    
tech = "XPS"
folder = "2.oktober"

file = "TOOLS SI-doping 24-9-19 2019-10-02_17h54m47s 1"
    
Plot("xy/"+tech+"/"+folder+"/"+file+".xy",XPS = True)

folders = ["2.oktober","3.oktober","4.oktober",
           "10.oktober","11.oktober","18.oktober","19.oktober"]



import os

def getImages():
    for dirs in folders:
        for filename in os.listdir("xy/XPS/"+dirs):
            if filename.endswith(".xy"): 
                print(os.path.join("xy/XPS/"+dirs, filename))
                Plot("xy/XPS/"+dirs+"/"+filename, XPS = True, save = True)
            else:
                print("Oops")
                    
                    



