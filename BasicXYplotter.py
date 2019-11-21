# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:25:38 2019

@author: Espen
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['axes.formatter.useoffset'] = False

folders = ["2.oktober", "3.oktober", "4.oktober", "10.oktober", "11.oktober", "18.oktober", "19.oktober"]
import os

def getXPS():
    for dirs in folders:
        for filename in os.listdir("xy/XPS/"+dirs):
            if filename.endswith(".xy"): 
                print(os.path.join("xy/XPS/"+dirs, filename))
                Plot("xy/XPS/"+dirs+"/"+filename, XPS = True, save = True, close = True)
            else:
                print("Oops")
				 
def getUPS():
    for filename in os.listdir("xy/UPS/"):
        if filename.endswith(".xy"):
            Plot("xy/UPS/"+filename,XPS = False, save=True, close = True)

def Reader(filename,bindingEnergy, workFunc = 4.31, exEnergy = 1486.61): 
    #Leser inn alle plots som ligger i en xy-fil med navn filename
    # bindingEnergy: boolsk: vil du ha binding energy??
    x = []
    y = []
    f = open(filename,"r")
    xTemp=[]
    yTemp=[]
    reg = ""
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
        elif el.split()[0]=="#" and len(el.split())>=3:
            if el.split()[1]=="Region:":
                reg = el.split()[2]
                #print(reg)
    f.close()
    return averager(x,y, len(x), reg)
    
def averager(_x,_y, N, reg): 
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
    return _x[0],yAvgTemp, N, reg


def Plot(filename, size=(10,6), col="r", bindingEnergy=True, XPS=True, save=False, close = False):
    # XPS == True --> xps-data som input
    # XPS == False --> ups-data som input
    plt.style.use("default")
    #X,Y,cts = Reader(filename, bindingEnergy)
    if not XPS: 
        X,Y,cts,reg = Reader(filename, bindingEnergy,exEnergy= 21.2182)
    else: 
        X,Y,cts, reg = Reader(filename, bindingEnergy)
    print(f"{cts} scans")
    
    matplotlib.rcParams['axes.formatter.useoffset'] = False
    fig = plt.figure(figsize=size)
    plt.plot(X,Y,col,linewidth=0.5)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.title(reg)
    plt.ylabel("Intensity [counts per second]")
    if bindingEnergy: 
        plt.gca().invert_xaxis()
        plt.xlabel("Binding energy [eV]")
    elif not bindingEnergy: plt.xlabel("Kinetic energy [eV]")

    if save and XPS:
        fig.savefig("imgs/"+str(filename.split("/")[3][:-3])+".png")
    elif save and not XPS:
        fig.savefig("imgs/"+str(filename.split("/")[2][:-3])+".png")
    if close: plt.close()

def MultiPlot(filenames, size=(10,6), bindingEnergy=True, XPS=True, save=False, close = False, lim = False, leg = True, col = None):
    # filenames is a list of filenames
    # XPS == True --> xps-data som input
    # XPS == False --> ups-data som input
    plt.style.use("default")
    xVals = []
    yVals = []
    for name in filenames:
        if not XPS:
            X,Y,cts, reg = Reader(name, bindingEnergy,exEnergy= 21.2182)
            xVals.append(X), yVals.append(Y)
        else: 
            X,Y,cts, reg = Reader(name, bindingEnergy)
            xVals.append(X), yVals.append(Y)
    matplotlib.rcParams['axes.formatter.useoffset'] = False
    fig = plt.figure(figsize=size)
    print("Last 10 yVals in each plot:")
    for i in range(len(filenames)):
        plt.plot(xVals[i],yVals[i],label=filenames[i].split("/")[2][6:-3], color = col)
        print(yVals[i][-10:])
    plt.ylabel("Intensity [counts per second]")
    if leg:
	    plt.legend()
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    if not XPS: 
        plt.axvline(0,0,0.25e6,color="black",linestyle="dashed", alpha=0.5)
        if lim:
            plt.xlim(-0.5,1)
            plt.ylim(1.0e5,2e5)
    if bindingEnergy: 
        plt.gca().invert_xaxis()
        plt.xlabel("Binding energy [eV]")
    elif not bindingEnergy: plt.xlabel("Kinetic energy [eV]")
    
    
    if save:
        fig.savefig("imgs/multiplot.png")
    if close: plt.close()
    
tech = "XPS"
folder = "11.oktober"
file = "TOOLS SI-doping 24-9-19 2019-10-11_13h05m21s 2"
    
#Plot("xy/"+tech+"/"+folder+"/"+file+".xy",XPS = True)

#Plot("xy/"+tech+"/"+file+".xy",XPS = False)

filer = ["04-10-Pure Si.xy",
		 "11-10-Post Al deposit.xy",
		 "18-10-Post Si on Al.xy",
		 "19-10-Post anneal.xy"
		 ]

zfilerXPS=["02-10-Post flash anneal.xy",
		   "03-10-Post Si deposit 10 min.xy",
		   "04-10-Post Si deposit (30 min total).xy",
		   "10-10-Post Al deposit 10 min.xy", 
		   "10-10-Post Al deposit 32 min total.xy",
		   "11-10-Post Al deposit 62 min total.xy",
		   "11-10-Post Al deposit 71 min total.xy",
		   "18-10-Post Si on Al.xy",
		   "19-10-Post final anneal.xy"]

filerXPS=["02-10-Post flash anneal.xy",
		  "04-10-Post Si deposit.xy", 
		  "11-10-Post Al deposit.xy",
		  "18-10-Post Si on Al.xy",
		  "19-10-Post final anneal.xy"
		  ]

fileDir = "rapportdata/XPS/"

MultiPlot([fileDir+i for i in filerXPS],XPS = True, save = False)#, size=(5,3))

MultiPlot([fileDir + "19-10-Post final anneal.xy"], leg = False, size=(5,3), col = "red")
