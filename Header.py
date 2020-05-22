# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 10:47:26 2020

@author: DrX
"""

from Klassen import *
from Einlesen import Einlesen
from Auslesen import *
from Hauptfunktionen import *
from tkinter import *
from tkinter import messagebox
from CSV import *
from LIN import *
from Klassen import getIndexPositions
#from Header import HeaderKorr
import string


#CSVName="test.lin"
#Dateiname="PET2009.dat"
#Out="Test.dat"
#Sollwert=10.0
#Header="Header.txt"


#A=ReadConfig(Dateiname)

#A=HeaderKorr(Header, Dateiname)






def HeaderKorr(DateinameHeader, DateinameDat):  
#    DateinameHeader="Header.txt"
    from Einlesen import EinlesenRoh 
    from Klassen import getIndexPositions

    Message=[]

    
    #Lädt Header.txt und zerlegt sie
    try:
        f =open(DateinameHeader, "r") 
        
        Zeile=[]
        
        for line in f:
        
        #    re.split()
            a=line       
        
            Zeile.append(a.strip())  
        
        Arbeitsnummer=Zeile[Zeile.index("Arbeitsnummer")+1]
        
        Beobachter=Zeile[Zeile.index("Beobachter")+1:Zeile.index("Instrument")]         
        Beobachter=[Beobachter[i].split() for i in range(len(Beobachter))]
        
        Instrument=Zeile[Zeile.index("Instrument")+1:Zeile.index("Lattenpaar")]
        Instrument=[Instrument[i].split() for i in range(len(Instrument))]
        
        Lattenpaar=Zeile[Zeile.index("Lattenpaar")+1:]
        Lattenpaar=[Lattenpaar[i].split() for i in range(len(Lattenpaar))]
    except:
        print("Keine richtige Header-Datei ausgewählt! Es können nur Werte geprüft werden, die keinen Bezug dazu haben.")
    
    
    
    #Lädt Dat-Datei und filert Headerdaten herasu
    Dat=EinlesenRoh(DateinameDat)
    
    Temp=Dat[2]
    
    Nr=Dat[1]
    NrSeg=[Nr[i][0:3] for i in range(len(Nr))]
    
    HeaderSeg=("01.","03.","05.","07.","09.","11.")
    
    HeaderInd=[getIndexPositions(NrSeg,HeaderSeg[i]) for i in range(len(HeaderSeg))]   #Gibt Indexe der Header zurück
    
      
   
    
    #Segment 2 Datum
    DatumInd=Nr.index("Justierung") +1   #Index des Datums
    DatumNiv=Nr[DatumInd]               
    DatumNiv=DatumNiv[0:10] 
    DatumNiv=DatumNiv.replace('.','')       #aus xx.xx.xxxx wird xxxxxxx                          
    DatumNiv=DatumNiv[0:4]+DatumNiv[6:8]           #20 aus Jahr 2000 wird entfernt
    
    try:
        Header01=(Nr[HeaderInd[0][0]]+Temp[HeaderInd[0][0]]) #Setzt Headerzeile wieder zusammen
        DatumHeader=Header01[13:]
        
        if(DatumHeader!=DatumNiv):
            Message.append("Datum falsch. Das Datum im Header "+ (DatumHeader) + " entspricht nicht dem Datum des Nivs."+ (DatumNiv)+"\n")
        else:
            Message.append("Datum richtig. Das Datum im Header "+ (DatumHeader) + " entspricht dem Datum des Nivs."+ (DatumNiv)+"\n")
    except:
        print("AAHHH. Im Header fehlt das Segment 02 Datum!")
        Message.append("Datei scheint keinen Header zu haben. Oder das Programm ist Müll.")
             
    
    
    #Segment 3
    
    
    

    Zugbeginn=getIndexPositions(Nr,"Zugbeginn")
    
    #Schleife   
    for j in range(len(Zugbeginn)):
        
        #Segment 07 Temperatur    
        try:
            TempHeader=Nr[HeaderInd[3][j]]
            TempHeader=float(TempHeader[3:5])    
            TempNivInd=None
            
            for i in range(len(Temp[Zugbeginn[j]:])):       #Findet erste Stelle in Temperatur die ein C enthält und somit die Starttemperatur
                if "C" in Temp[Zugbeginn[j]+i]:
                    TempNivInd=i+Zugbeginn[j]
                    break
                else:
                    pass
    
    
            try:            
                TempNiv=float(Temp[TempNivInd][0:4])
                
                if abs(TempNiv-TempHeader)>=3:
                    Message.append("Temperatur in Zug "+str(j+1) +" falsch >=3°. Die Temperatur im Header "+ str(TempHeader) + "° entspricht nicht der Temp der ersten Messung "+ str(TempNiv)+"°\n")
                else:
                    Message.append("Temperatur in Zug "+str(j+1) +" richtig <=3°. Die Temperatur im Header "+ str(TempHeader) + "° entspricht der Temp der ersten Messung "+ str(TempNiv)+"°\n")   
            except:
                print("Nivelliergerät hat scheinbar keine Temperaturen aufgezeichnet, oder dieses Programm ist scheiße!")
        except:
            print("AAHHH. Im Header von Zug "+str(j+1)+" fehlt das Segment 02 Datum!")
            
        #Segment 10 Anfangspunkt
        try:
            Header10=(Nr[HeaderInd[4][j]]+Temp[HeaderInd[4][j]])
            HeaderAnfangspunkt=Header10[13:18]
            
            NivAnfangspunktInd = Dat[4][Zugbeginn[j]:].index("Lr")+Zugbeginn[j]
            NivAnfangspunkt=Nr[NivAnfangspunktInd].split()
            NivAnfangspunkt=NivAnfangspunkt[0]
            
            if HeaderAnfangspunkt!=NivAnfangspunkt:
                Message.append("Anfangspunkt in Zug "+str(j+1) +" falsch. Der Anfangspunkt im Header "+ HeaderAnfangspunkt + " entspricht nicht dem Anfangspunkt im Header "+ HeaderAnfangspunkt +"\n")
            else:
                Message.append("Anfangspunkt in Zug "+str(j+1) +" richtig. Der Anfangspunkt im Header "+ HeaderAnfangspunkt + " entspricht dem Anfangspunkt im Header "+ HeaderAnfangspunkt +"\n")
        except:
            print("AAHHH. Im Header von Zug "+str(j+1)+" fehlt das Segment 10 Anfangspunkt!")
#        erster Lr im Zug
#        NivAnfangspunkt=
         #letzter Lr im Zug
         
         
        #Segment 11 Anfangspunkt
        try:
            Header10=(Nr[HeaderInd[5][j]])
            HeaderEndpunkt=Header10[3:8]
            
            NivEndpunktInd = getIndexPositions(Dat[4],"Sr")
            NivEndpunktInd=NivEndpunktInd[j]
            
            NivEndpunkt=Nr[NivEndpunktInd].split()                             #Entfernt mögliche Null am Ende
            NivEndpunkt=NivEndpunkt[0]
            
            if HeaderEndpunkt!=NivEndpunkt:
                Message.append("Endpunkt in Zug "+str(j+1) +" falsch. Der Endpunkt im Header "+ HeaderEndpunkt + " entspricht nicht dem Anfangspunkt im Header "+ HeaderEndpunkt +"\n")
            else:
                Message.append("Endpunkt in Zug "+str(j+1) +" richtig. Der Endpunkt im Header "+ HeaderEndpunkt + " entspricht dem Anfangspunkt im Header "+ HeaderEndpunkt +"\n")
        except:
            print("AAHHH. Im Header von Zug "+str(j+1)+" fehlt das Segment 11 Endpunkt!")
#        erster Lr im Zug
#        NivAnfangspunkt=
         #letzter Lr im Zug
        
        
        
        A=2
    return Message
    
    

    
    
    
    
    
    #Vorlauf, Nr, Temp, ZugNr, Art, Ablesung, Distanz, Stdabw