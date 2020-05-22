# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:34:06 2020

@author: DrX
"""
from Klassen import *


def Einlesen(Dateiname):
    
    
    import Klassen  #  Import von Klassenobjekten 
    from Klassen import getIndexPositions
    from Klassen import Str2Flo
    from Klassen import NivZug

#Datei öffnen und zerlegen
    f =open(Dateiname, "r")   #r = read only
   
    Nr=[""]
    Temp=[""]
    ZugNr=[""]
    Art=[""]
    Ablesung=[""]
    Distanz=[""]
    Stdabw=[""]
    
    
    for line in f:
    
    
        a=line
     
        fieldnr=(a[21:35])                 #Pnr ist nur 21:29, aber um "Zugbeginn" komplett zu sehen hier länger               
        fieldtemp=a[35:44]                #separiert die Zeile nach Positionen
        fieldZugNr=a[45:48]
        fieldart=a[49:51]
        fieldhoehe=a[51:66]
        fielddist=a[82:89]
        fieldstdabw=a[97:112]
        
        
        Nr.append(fieldnr.strip())     #FÃ¼gt Nummer zu Nummernliste hinzu und entfernt Leerzeichen
        Temp.append((fieldtemp.strip()))
        ZugNr.append(fieldZugNr.strip())
        Art.append(fieldart.strip())
        Ablesung.append(Str2Flo(fieldhoehe.strip()))
        Distanz.append(Str2Flo(fielddist.strip()))
        Stdabw.append(fieldstdabw.strip())
       
#Zugbeginn/Ende wird ermittelt.
    Zugbeginn=getIndexPositions(Nr,'Zugbeginn')      #Detektiert Zubeginn/Ende/Zwischenblicke und Wiederholungen
    Zugende=getIndexPositions(Nr,'Zugende')       

    if (len(Zugbeginn) !=  len(Zugende)):                                     #Bei unvollständigen Zügen wird abgebrochen
        print("Anzahl Zugbeginn und Zugende ist nicht gleich. Falls Fehler entsehen unvollständigen Zug vorher löschen.")
    
    if (len(Zugbeginn) !=  len(Zugende)):            #Prüft ob Züge vollständig sind
        for i in range(len(Zugbeginn)-1):             #Wenn nicht, wird die Stelle des letzten Zugbeginns-1 als Zugende gesetzt
            if Zugende[i] != Zugbeginn[i+1]-1:
                Zugende.insert(i ,Zugbeginn[i+1]-1)
                i+=1                               #erhöht Laufvariable um eingeschobenen Wert zu kompensieren. Sonst hört er zu früh auf.
                        
        if Zugende[-1] !=len(Nr)-1:                   #Prüft ob das letzte Zugende vorhanden ist und setzt ggf. Zugende auf letzte Zeile
            Zugende.append(len(Nr))
            
#Justierung extrahieren                      
    try:    
        CInd=getIndexPositions(Art, "c_")                                             #Findet Index letzte Justierung
        CInd=CInd[-1]
        C=Ablesung[CInd]
        try:
            Abl_A1=Ablesung[CInd-4]
            Abl_B1=Ablesung[CInd-3]
            Abl_B2=Ablesung[CInd-2]
            Abl_A2=Ablesung[CInd-1]
            
            Dist_A1=Distanz[CInd-4]
            Dist_B1=Distanz[CInd-3]
            Dist_B2=Distanz[CInd-2]
            Dist_A2=Distanz[CInd-1]
        except:
            print("Keine Justierungsmessung vorhanden. Ein C-Wert ist aber vorhanden.") #Falls keine Justiermessungen vorhanden sind
            Abl_A1=""
            Abl_B1=""
            Abl_B2=""
            Abl_A2=""
                   
            Dist_A1=""
            Dist_B1=""
            Dist_B2=""
            Dist_A2=""             
    except:
        print("Keine Justierung vorhanden! ")                                   #Falls gar keine Justierung vorhanden ist
        C=""
        Abl_A1=""
        Abl_B1=""
        Abl_B2=""
        Abl_A2=""
               
        Dist_A1=""
        Dist_B1=""
        Dist_B2=""
        Dist_A2=""  
        
#    Abl_A1=Ablesung[CInd-4]
#    Abl_B1=Ablesung[CInd-3]
#    Abl_B2=Ablesung[CInd-2]
#    Abl_A2=Ablesung[CInd-1]
#    
#    Dist_A1=Distanz[CInd-4]
#    Dist_B1=Distanz[CInd-3]
#    Dist_B2=Distanz[CInd-2]
#    Dist_A2=Distanz[CInd-1]        
        

    Justierung=[Abl_A1, Abl_B1,Abl_B2,Abl_A2,Dist_A1,Dist_B1,Dist_B2,Dist_A2,C,CInd]  
    print(CInd)
     
#Anlegen Leeres Niv
    AnzahlZuege=len(Zugende)
    NivZuege=[]                 #Liste fÃ¼r Daten des Typs NivZug
   
    Niv_Zug=[]                  #Variable der Klasse NivZug
    
    Niv_PNr=[]                  #Werte die obige Variable fÃ¼llen
    Niv_Art=[]
    Niv_Temp=[]
    Niv_ZugNr=[]
    Niv_Ablesung=[]
    Niv_Distanz=[]
    Niv_Stdabw=[]
    Wiederholung=[]  

#Postionen der Header ermitteln    
    NrSeg=[Nr[j][0:3] for j in range(len(Nr))]
    HeaderSeg=("01.","03.","05.","07.","09.","11.")
    HeaderInd=[getIndexPositions(NrSeg,HeaderSeg[j]) for j in range(len(HeaderSeg))]   #Gibt Indexe der Header zurück    
    Headers=[]
    
    i=0
    while i < AnzahlZuege:     #Schleife für Header und NivZuege
        
#Header der Züge werden extrahiert 
        Header=[]
        HeaderSegmente=[]
        for j in range(6):
            try:            
                Header=Nr[HeaderInd[j][i]]+Temp[HeaderInd[j][i]]              #setzt Zeile wieder zusammen
                HeaderSegmente.append(Header[3:9])                            #extrahiert Inhalte
                HeaderSegmente.append(Header[13:19]) 
            except:
                HeaderSegmente.append("")                                       #Falls der Header Leer ist, wird eine leere Zeile eingefügt
                HeaderSegmente.append("")
                
        Headers.append(HeaderSegmente)
        
#Züge werden ausgegeben 
        Niv_PNr=Nr[Zugbeginn[i]:Zugende[i]]   
        Niv_Art=Art[Zugbeginn[i]:Zugende[i]]
        Niv_Temp=Temp[Zugbeginn[i]:Zugende[i]]
        Niv_ZugNr=ZugNr[Zugbeginn[i]:Zugende[i]]
        Niv_Ablesung=Ablesung[Zugbeginn[i]:Zugende[i]]
        Niv_Distanz=Distanz[Zugbeginn[i]:Zugende[i]]
        Niv_Stdabw=Stdabw[Zugbeginn[i]:Zugende[i]]
        
#Fehlstellen werden ermittelt        
        WiederholungM=getIndexPositions(Niv_PNr, "Wiederholung M")           #Wiederholungen Messungen
        WiederholungM=([x-1 for x in WiederholungM]) + WiederholungM
        
        WiederholungS=getIndexPositions(Niv_PNr, "Wiederholung S")           #Wiederholungen Standpunkt
        WiederholungS2=[x-2 for x in WiederholungS]
        WiederholungS1=[x-1 for x in WiederholungS]
        WiederholungS=WiederholungS+WiederholungS1+WiederholungS2
        
        Wiederholung= WiederholungM + WiederholungS                         #Alle Indexe die Wiederholungen sind


        Zwischenblick=getIndexPositions(Niv_PNr, "Zwischenblicke")
        ZwischenblickE=getIndexPositions(Niv_PNr, "Ende Zwischenb")
        Zwischenblick= Zwischenblick + ZwischenblickE
        
        Fehlstellen =  Zwischenblick+Wiederholung
        Fehlstellen.sort()

#NivZüge werden zusammengestellt        
        Niv=NivZug(Niv_ZugNr[0],"","",Niv_Ablesung[-1],Niv_Distanz[-1],Niv_PNr,Niv_Art,Niv_Temp,Niv_Ablesung,Niv_Distanz,Niv_Stdabw, Fehlstellen, Zugbeginn[i], Zugende[i])
        NivZuege.append(Niv)
        i=i+1                       #IndexerhÃ¶hung
  
        Niv_Zug=[]
        Niv_PNr=[]                   # Setzt Variablen fÃ¼r zweiten Durchlauf zurÃ¼ck
        Niv_Art=[]
        Niv_Temp=[]
        Niv_ZugNr=[]
        Niv_Ablesung=[]
        Niv_Distanz=[]
        Niv_Stdabw=[]
    
#Ausgabe    
    print("Datei "+Dateiname+ " wurde erfolgreich eingelesen.")
    return NivZuege, Headers, Justierung



def EinlesenRoh(Dateiname):
    
    from Klassen import Str2Flo
    #f =open("WYC.dat", "r")   #r = read only
    f =open(Dateiname, "r")   #r = read only
    #print(AA)


    
    #M1=Messung(999,2,3,4,5)
    #M1.Druck()
    Vorlauf=[""]
    Nr=[""]
    Temp=[""]
    ZugNr=[""]
    Art=[""]
    Ablesung=[""]
    Distanz=[""]
    Stdabw=[""]
    
    
    for line in f:
    
    
        a=line
        fieldVorlauf=(a[0:21])
        fieldnr=(a[21:35])                 #Pnr ist nur 21:29, aber um "Zugbeginn" komplett zu sehen hier länger               
        fieldtemp=a[35:44]                #separiert die Zeile nach Positionen
        fieldZugNr=a[45:48]
        fieldart=a[49:51]
        fieldhoehe=a[51:66]
        fielddist=a[82:89]
        fieldstdabw=a[97:112]
        
        Vorlauf.append(fieldVorlauf)
        Nr.append(fieldnr.strip())     #FÃ¼gt Nummer zu Nummernliste hinzu und entfernt Leerzeichen
        Temp.append((fieldtemp.strip()))
        ZugNr.append(fieldZugNr.strip())
        Art.append(fieldart.strip())
        Ablesung.append(Str2Flo(fieldhoehe.strip()))
        Distanz.append(Str2Flo(fielddist.strip()))
        Stdabw.append(fieldstdabw.strip())    

    return Vorlauf, Nr, Temp, ZugNr, Art, Ablesung, Distanz, Stdabw