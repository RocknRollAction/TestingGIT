# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 20:28:46 2020

@author: udowy
"""
from Klassen import getIndexPositions
import numpy as np
#Dijkstra Motherfucker!

class City:
    
        def __init__(self,ID,Name,Nachbarn,NachbarDistanzen):  
            self.ID=ID
            self.Name=Name
            self.Nachbarn=Nachbarn
            self.NachbarDistanzen=NachbarDistanzen

    
#            self.SummeV=SummeV
            

Neighbour=[2,1]
Distanzen=[4,1]
Oldenburg=City(0,"Oldenburg",Neighbour,Distanzen)

Neighbour=[0,2,4]
Distanzen=[1,5,8]
Bremen=City(1,"Bremen",Neighbour,Distanzen)

Neighbour=[0,1,3]
Distanzen=[4,5,4]
Essen=City(2,"Essen",Neighbour,Distanzen)

Neighbour=[2,1,4,5]
Distanzen=[4,9,10,9]
Frankfurt=City(3,"Frankfurt",Neighbour,Distanzen)

Neighbour=[3,1,5]
Distanzen=[10,8,11]
Berlin=City(4,"Berlin",Neighbour,Distanzen)

Neighbour=[3,4]
Distanzen=[9,11]
Muenchen=City(5,"Muenchen",Neighbour,Distanzen)


Netz=[Oldenburg,Bremen,Essen,Frankfurt,Berlin,Muenchen]
Entfernungen=np.array([999] * len(Netz))


VisitedCitys=[0]
Entfernungen[0]=0
Start=0         #Position in Liste Netz
Origin=0
Origin2Start=0
Netz[Start].Name
for j in range(len(Netz)):
    Entfernung2Origin=Netz[Origin].NachbarDistanzen
    
    for i in range(len(Entfernung2Origin)):                                     #befüllt Liste der Entfernungen
        if(Entfernungen[Netz[Origin].Nachbarn[i]]> Entfernung2Origin[i]):
            Entfernungen[Netz[Origin].Nachbarn[i]]=Entfernung2Origin[i]
    
    NotVisitedCitys=list(set(range(len(Netz)))-set(VisitedCitys)) 
        
    Entfernungen[NotVisitedCitys]+=Origin2Start
#    Entfernungen=np.array([k+Origin2Start for k in Entfernungen[NotVisitedCitys]]   )     

    EntfernungenOhneVisited=Entfernungen[NotVisitedCitys]

    DistOrigin2Start=Entfernungen[np.where(Entfernungen==min(EntfernungenOhneVisited))]   #Ohne VisitedCitys bestimmen
    

    Origin=np.where(Entfernungen==min(EntfernungenOhneVisited))                   #Stadt mit min Distanz die noch nicht besucht wurde
    
    Origin=int(Origin[0][-1])
    VisitedCitys.append(Origin)
    
    
    
    



