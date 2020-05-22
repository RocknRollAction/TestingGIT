# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 15:13:11 2020

@author: wycital
"""

def EinlesenCSV(Dateiname):



#    Dateiname="Netz-STORAG-2019.csv"
        
    f =open(Dateiname, "r") 
    
    Punktnr=[]
    Rechtswert=[]
    Hochwert=[]
    Hoehe=[]
    Art=[]
    
    
    for line in f:
    
    
        a=line
        
        
        a=a.split(",")
    
        Punktnr.append(a[0])    
        Rechtswert.append((a[1]))
        Hochwert.append((a[2]))
        Hoehe.append((a[3]))
        Art.append((a[4]))   
        
        
        

    Rechtswert=[float(i) if i != "" else i for i in Rechtswert] #Wandelt Daten in String sind. Falls sie Leer sind übernimmt er sie so.
    Hochwert=[float(i) if i != "" else i for i in Hochwert]  
    Hoehe=[float(i) if i != "" else i for i in Hoehe]           
    Art=[float(i) if i != "" else i for i in Art] 
   
    
        
    return Punktnr, Rechtswert, Hochwert, Hoehe, Art