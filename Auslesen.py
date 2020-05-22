# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:18:29 2020

@author: DrX
"""
from Klassen import *
from Einlesen import *
#from Klassen import getIndexPositions

def Auslesen(NivZuege,Justierung,Dateiname,DateinameOut):
       
    from Klassen import Flo2StrList   
    print("Auslesen")
    print(Justierung)
    
#Ablesung und Distanz zu String in richtigem Format umformen    
    if NivZuege==[]:
        raise Exception("Keine Datei eingelesen! Bitte zunächst Datei auswählen und auf Einlesen klicken.")      
    
    for i in range(len(NivZuege)):
        
        NivZuege[i].Ablesung=Flo2StrList(NivZuege[i].Ablesung,5)            
        NivZuege[i].Distanz=Flo2StrList(NivZuege[i].Distanz,3) 

      
#Dateien öffnen    
    w=open(DateinameOut, "x")
    f =open(Dateiname, "r") 
    
#Zugende/beginn abspeichern    
    Zugbeginn=[NivZuege[i].Zugbeginn for i in range(len(NivZuege))]  #Zugende/Beginn in Listen
    Zugende=[NivZuege[i].Zugende for i in range(len(NivZuege))]
#Beginn und Ende der Justierung 


    JustBeginn=Justierung[9]-4     #Detektiert Zubeginn/Ende/Zwischenblicke und Wiederholungen
    JustEnde=Justierung[9]
    
#Schleife für Datei schreiben    
    i=1                                 #Laufvariable Zeilennummer
    j=0
    ZugNr=str(j+1)                                 #Laufvariable der Zugnummer
    for line in f:
  
        a=line
        Adr=str(i)
        
#Schreibt Zeilen mit Justierung
        if(i>=JustBeginn and i<=JustEnde): 

            Abl=Justierung[i-JustBeginn]
            Dist=Justierung[i-JustBeginn+5]
            
            Zeile=a[0:12] + Adr.rjust(4)  +a[16:51] + Abl.rjust(15) + a[66:74] +Dist.rjust(15) + a[89:118] +"\n"
            w.write(Zeile)  
            
#Schreibt Zeilen mit Zügen
        elif(i>=Zugbeginn[j] and i<Zugende[j]):   
            
            Dist=NivZuege[j].Distanz[i-Zugbeginn[j]]
            Ablesung=NivZuege[j].Ablesung[i-Zugbeginn[j]]
            Stdabw=NivZuege[j].Stdabw[i-Zugbeginn[j]]

            Zeile=a[0:12] + Adr.rjust(4)  +a[16:44] + ZugNr.rjust(4) + a[48:51] + Ablesung.rjust(15) + a[66:74] +Dist.rjust(15) + a[89:97] + Stdabw.rjust(15) + a[112:118] +"\n"
#            w.write(str(NivZuege[j].Distanz[i-Zugbeginn[j]]))
            w.write(Zeile)  
            
#Wenn das Zugende erreicht wurde Zuvariable++ Zugende mit verbesserten Nummern            
        elif(Zugende[j]==i):                    
                       
            Zeile=a[0:12] + Adr.rjust(4)  +a[16:44] + ZugNr.rjust(4) + a[48:118]+"\n"   #Zugende mit verbesserten nummern
            w.write(Zeile)
            
            j=j+1
            ZugNr=str(j+1)
            
#Zeile aus Original + Angepasste Adresse und Zugnummer
        else:                                   #Wenn in keinem Zug>Zeile übernehmen                          
            Zeile=a[0:12] + Adr.rjust(4) +a[16:118]+"\n"
            w.write(Zeile)         
 
        i=i+1                                                  #Erhöhung der Laufvariable
    print("Datei wurde als "+ DateinameOut+ " ausgegeben.")
#    return Message

def Auslesen_Just(Dateiname, DateinameOut, Ablesung, Distanz, CIndex):
    
     
    JustBeginn=CIndex-4     #Detektiert Zubeginn/Ende/Zwischenblicke und Wiederholungen
    JustEnde=CIndex

    w=open(DateinameOut, "x")
    f =open(Dateiname, "r") 
    
    i=1                                 #Laufvariable Zeilennummer
    for line in f:
        
        
        a=line
        Adr=str(i)
        
        
        if(i>=JustBeginn and i<=JustEnde):   
            
            
            Abl=Ablesung[i-JustBeginn]
            Dist=Distanz[i-JustBeginn]
            
            Zeile=a[0:12] + Adr.rjust(4)  +a[16:51] + Abl.rjust(15) + a[66:74] +Dist.rjust(15) + a[89:118] +"\n"
#            w.write(str(NivZuege[j].Distanz[i-Zugbeginn[j]]))
            w.write(Zeile)           
            
            
        else:                                   #Wenn in keinem Zug>Zeile übernehmen                          
            
            Zeile=a[0:12] + Adr.rjust(4) +a[16:118]+"\n"
            w.write(Zeile)
    
       
        
        i=i+1                                                  #Erhöhung der Laufvariable
    return 