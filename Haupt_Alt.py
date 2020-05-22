# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 12:56:59 2020

@author: wycital
"""
from Klassen import *
from Einlesen import *
from Auslesen import *


"""
Randbedingungen
"""
#Dateiname="2019-09-05-JFI-191004.DAT"     #Evtl als eigene Klasse um Funktionsaufruf zu erleichtern
#DateinameK="K.dat"
#
#VarMaxDelta1=2                            #Maximale DeltaSummeRV wenn unter Streckengrenze
#VarMaxDelta2=3                            #Maximale DeltaSummeRV wenn über Streckengrenze
#StreckenGrenze=400                        #Strecke ab der sich VarMaxDelta ändert
#MaxDistanz=40                             #Maximale Stecke
#MaxLrLvDelta=1                            #Maximales Delta zwischen LR und LV Päärchen
#              
#MinAblesung=1                             #Minimale Ablesung
#MaxAblesung=3                             #Maximale Ablesung
#
##Startfehlstellen=2                        #Zeilen die nach "Zugbeginn" irrelevant sind 
#
#a=KorrDstAbl(Dateiname,DateinameK,VarMaxDelta1,VarMaxDelta2,StreckenLimit,MaxDist,MaxLrLvDelta,MinAbl,MaxAbl)

def KorrDstAbl(Dateiname, DateinameK, VarMaxDelta1,VarMaxDelta2,StreckenGrenze,MaxDistanz,MaxLrLvDelta,MinAblesung,MaxAblesung):
#    try:
#        return float(s)
#    except ValueError:
#        return s



    """
    Einlesen
    """
    NivZuege=Einlesen(Dateiname)     #List Datei ein und gibt NivZuege aus
    
    
    for i in range(len(NivZuege)):
        
        """
        Bereinigen
        """
        Niv=NivZuege[i]
        
        StartDistanz=(list(Niv.Distanz))                                           #Ursprungswerte werden gespeichert/ Als String mit.5 um späteren Nullfehler zu vermeiden
       
          
        StartAblesung=list(Niv.Ablesung)                                             #Ursprungswerte werden gespeichert/ Als String mit.5 um späteren Nullfehler zu vermeiden
        
        Startfehlstellen=Niv.Art.index("Lr")    
        StartArt=list(Niv.Art)
        
        
        Distanz=delFehlstellen(Niv.Distanz,Niv.Fehlstellen,Startfehlstellen)                #Löscht Wiederholungen/Zwischenblick, Startfehlstellen              
        Ablesung=delFehlstellen(Niv.Ablesung,Niv.Fehlstellen,Startfehlstellen)
        Art=delFehlstellen(Niv.Art,Niv.Fehlstellen,Startfehlstellen)
        
        
        
        Lr=getIndexPositions(Art,"Lr")
        Lv=getIndexPositions(Art,"Lv")
        
    
        """________________________________________________________________________________________________________________________________________
        Korrektur Distanzen
        """
        
        """
        Korrektur SummeRVfehler
        """
        MaxDelta=VarMaxDelta2
        DeltaSummeRV=Niv.SummeR-Niv.SummeV
        
        if (Niv.SummeR+Niv.SummeV) < StreckenGrenze:             #Bestimmt welche maximale Streckendiff angewendet werden mus
           MaxDelta=VarMaxDelta1      
           
        # Hier evtl noch Random einbaue, sodass manchmal 0.25 m verwendet und manchmal 0.5m werden   
        SummenKorrektur=(DeltaSummeRV-MaxDelta+0.5) - ((DeltaSummeRV-MaxDelta+0.5)%0.5)      #Zu korrigierendes Delta mit Überhang auf 0.25M Werte normalisiert
           
           
           
        if DeltaSummeRV>MaxDelta:                                  #Summe Rückblicke ist größer und überschreitet Grenzwert
            
            LvDist = [ Distanz[i] for i in Lv]                         #nimmt nur Distanzen der Beobachtungsart LV
            MinLv=min(LvDist)                                            #findet min Distanz von LV
            
            MinDistInd=getIndexPositions(Distanz,MinLv)                    #Findet Ind des Min Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
            MinDistInd=list(set(MinDistInd)-(set(MinDistInd)-set(Lv)))                  #Verschneidet DistanzenInd mit LVInd> Ergebnis minimale(r) LvWertInd        
            MinDistInd=MinDistInd[0]                                       #Falls mehrere gleiche minimale Lv vorhanden
            
            Distanz[MinDistInd]=Distanz[MinDistInd]+SummenKorrektur
            Niv.SummeV=Niv.SummeV+SummenKorrektur 
            Distanz[-1]=Niv.SummeV
            print("Bei Zug Nr." + Niv.ZugNr + " DeltaSummeRV angepasst: Rückblicke um "+ str(SummenKorrektur) +"m vergrößert")
            
            
        elif (-1)*DeltaSummeRV>MaxDelta:                                    #SummeR<SummeL
            
            LrDist = [ Distanz[i] for i in Lr]                         #nimmt nur Distanzen der Beobachtungsart Lr
            MinLr=min(LrDist)                                            #findet min Distanz von Lr
            
            MinDistInd=getIndexPositions(Distanz,MinLr)                    #Findet Ind des Min Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
            MinDistInd=list(set(MinDistInd)-(set(MinDistInd)-set(Lr)))                  #Verschneidet DistanzenInd mit LrInd> Ergebnis minimale(r) LrWertInd        
            MinDistInd=MinDistInd[0]                                       #Falls mehrere gleiche minimale Lr vorhanden
            
            Distanz[MinDistInd]=Distanz[MinDistInd]+SummenKorrektur
            Niv.SummeR=Niv.SummeV+SummenKorrektur
            Ablesung[-1]=Niv.SummeR
            
            print("Bei Zug Nr." + Niv.ZugNr + " DeltaSummeLr angepasst: Vorblicke um "+ str(SummenKorrektur) +"m  vergrößert")
        #    Distanz(MinDistIndex)=Distanz(MinDistIndex)
        else:
           
            print("Bei Zug Nr." + Niv.ZugNr + " keinen Summenfehler festgestellt")
        
        """
        Korrektur MaxDistanz Lr
        """
        
        
        FehlerDistanz=True
        
        while(FehlerDistanz==True):                                                    #Schleife über MaxDistanzLrLv und RVDelta, Bei der Summe reicht ein Durchlauf
        
            LrDist = [ Distanz[i] for i in Lr]                                         #Berechnet MaxLr
            MaxLr=max(LrDist)
            while(MaxLr>MaxDistanz):
                if MaxLr> MaxDistanz :
                    
                    DistKorrektur=(MaxLr-MaxDistanz+0.25) - ((MaxLr-MaxDistanz+0.25)%0.25)     #Der Wert um den korrigiert wird in 0.25er Schritten
                    
                    MaxDistInd=getIndexPositions(Distanz,MaxLr)                        #Findet Ind des Max Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
                    MaxDistInd=list(set(MaxDistInd)-(set(MaxDistInd)-set(Lr)))         #Verschneidet DistanzenInd mit LrInd> Ergebnis Maximale(r) LrWertInd        
                    MaxDistInd=MaxDistInd[0]  
                    
                    
                    LrDist = [ Distanz[i] for i in Lr]                                 #nimmt nur Distanzen der Beobachtungsart Lr
                    MinLr=min(LrDist)                                                  #findet min Distanz von Lr
                    
                    MinDistInd=getIndexPositions(Distanz,MinLr)                        #Findet Ind des Min Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
                    MinDistInd=list(set(MinDistInd)-(set(MinDistInd)-set(Lr)))         #Verschneidet DistanzenInd mit LrInd> Ergebnis minimale(r) LrWertInd        
                    MinDistInd=MinDistInd[0] 
                    
                    Distanz[MinDistInd]=Distanz[MinDistInd]+DistKorrektur              #Kleiner Wert erhält Aufschlag
                    
                    Distanz[MaxDistInd]=Distanz[MaxDistInd]-DistKorrektur              #Großer Wert erhält Abschlag
                    
#                    print("Bei Zug Nr." + str(Niv.ZugNr) + "ist die Lr Distanz in Zugzeile "+ MaxDistInd + "zu groß. Sie wird um "+ str(DistKorrektur) +"m  verkleinert")
#                    print("Als Ausgleich wurde in Zugzeile "+ str(MinDistInd) +"um "+ str(DistKorrektur)+ "verringert ")
                                        
                    LrDist = [ Distanz[i] for i in Lr]                                 #Änderung der SChleifenvariable
                    MaxLr=max(LrDist)
            
            """
            Korrektur MaxDistanz Lv
            """ 
            LvDist = [ Distanz[i] for i in Lv]
            MaxLv=max(LvDist)
            
            
            while(MaxLv>MaxDistanz):
                if MaxLv> MaxDistanz :
                    
                    DistKorrektur=(MaxLv-MaxDistanz+0.25) - ((MaxLv-MaxDistanz+0.25)%0.25)   #Der Wert um den korrigiert wird in 0.25er Schritten
                    
                    MaxDistInd=getIndexPositions(Distanz,MaxLv)                       #Findet Ind des Max Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
                    MaxDistInd=list(set(MaxDistInd)-(set(MaxDistInd)-set(Lv)))        #Verschneidet DistanzenInd mit LvInd> Ergebnis Maximale(r) LvWertInd        
                    MaxDistInd=MaxDistInd[0]  
                    
                    
                    LvDist = [ Distanz[i] for i in Lv]                                #????? nimmt nur Distanzen der Beobachtungsart Lv
                    MinLv=min(LvDist)                                                 #findet min Distanz von Lv
                    
                    MinDistInd=getIndexPositions(Distanz,MinLv)                       #Findet Ind des Min Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
                    MinDistInd=list(set(MinDistInd)-(set(MinDistInd)-set(Lv)))        #Verschneidet DistanzenInd mit LvInd> Ergebnis minimale(r) LvWertInd        
                    MinDistInd=MinDistInd[0] 
                    
                    Distanz[MinDistInd]=Distanz[MinDistInd]+DistKorrektur             #Kleiner Wert erhält Aufschlag
                    
                    Distanz[MaxDistInd]=Distanz[MaxDistInd]-DistKorrektur             #Großer Wert erhält Abschlag
                    
#                    print("Bei Zug Nr." + str(Niv.ZugNr) + "ist die Lv Distanz in Zugzeile "+ str(MaxDistInd) + "zu groß. Sie wird um "+ str(DistKorrektur) +"m  verkleinert")
#                    print("Als Ausgleich wurde in Zugzeile "+ str(MinDistInd) + "um "+ str(DistKorrektur)+ "verringert ")
                    
                    LvDist = [ Distanz[i] for i in Lv]                                #Änderung der SChleifenvariable
                    MaxLv=max(LvDist)
                     
            """
            Korrektur RVDelta
            """
            DeltaLrLv=[None] * len(Lr)    
            for i in range(len(Lr)):                                                   #Berechnen der LrLv Deltas                                   
                DeltaLrLv[i]=Distanz[Lr[i]]-Distanz[Lv[i]]    
                
            
            DeltaLrLvMax=max(DeltaLrLv, key=abs)
            while(DeltaLrLvMax>=MaxLrLvDelta):                                         #Delta > Grenzwert?
            
                
                Korrektur = (DeltaLrLvMax-MaxLrLvDelta+0.1)-((DeltaLrLvMax-MaxLrLvDelta+0.1)%0.1)   #Berechnung notwendige Korrektur der Beobachtung
               
                DeltaLrLvMaxInd=DeltaLrLv.index(DeltaLrLvMax)    
                if(DeltaLrLvMax>=0):                                     #Delta Positiv   Lr>Lv Lr muss kleiner werden 
                    DeltaLrLvGegenInd=DeltaLrLv.index(min(DeltaLrLv))        
                    
                    Distanz[Lr[DeltaLrLvMaxInd]]=Distanz[Lr[DeltaLrLvMaxInd]]-Korrektur        #Delta das zu groß ist nach unten
                    Distanz[Lr[DeltaLrLvGegenInd]]=Distanz[Lr[DeltaLrLvGegenInd]]+Korrektur    #und auf den Wert der es am ehesten vertägt aufaddiert 
                    
                    
                    
                else:                                                   #Delta<0  Lv>Lr=> Lv muss kleiner werden (Theoretisch auch mit LR möglich. Dann +Korrektur)
                    DeltaLrLvGegen=DeltaLrLv.index(max(DeltaLrLv))
                    
                    Distanz[Lv[DeltaLrLvMaxInd]]=Distanz[Lv[DeltaLrLvMaxInd]]-Korrektur        #Delta das zu groß ist nach unten
                    Distanz[Lv[DeltaLrLvGegenInd]]=Distanz[Lv[DeltaLrLvGegenInd]]+Korrektur    #und auf den Wert der es am ehesten vertägt aufaddiert 
                
                for i in range(len(Lr)):                                             #Berechnen der LrLv Deltas                                   
                    DeltaLrLv[i]=Distanz[Lr[i]]-Distanz[Lv[i]]  
                DeltaLrLvMax=max(DeltaLrLv, key=abs)                                #Neubestimmung der Schleifenvariable
                    
            """
            Prüfungen
            """
            
            LrDist = [ Distanz[i] for i in Lr]                          
            MaxLr=max(LrDist)
            LvDist = [ Distanz[i] for i in Lv]                               
            MaxLv=max(LvDist)
            
            if(MaxLr <= MaxDistanz and MaxLv <= MaxDistanz):            #Anpassung Schleifenvariable
                FehlerDistanz=False
        """
         Die obige Prüfvariable enthält nur MaxDistanz, da Korrektur RVDelta solange durchgeführt wird bis es korrekt ist. 
        """    
        
        
        """________________________________________________________________________________________________________________________________________
        Korrektur Ablesung
        """
        
        """
        Korrektur AblesungLr
        """
            
        AblesungLr=[None] * len(Lr)    
        
        for i in range(len(Lr)):                                                                                 
            AblesungLr[i]=Ablesung[Lr[i]]                                              #Alle Lr Ablesungen         
        MaxLr=max(AblesungLr)
        
        
        while(MaxLr>MaxAblesung):
            while(MaxLr>MaxAblesung):
            
                MaxLrInd=AblesungLr.index(MaxLr)                                    #Index Maximale LrAblesung
                Korrektur = (MaxLr-MaxAblesung+0.1)-((MaxLr-MaxAblesung+0.1)%0.1)   #Berechnet Korrekturwert   
                Ablesung[Lr[MaxLrInd]]=Ablesung[Lr[MaxLrInd]]-Korrektur             #Korrigiert maximalen Lr Wert
                
                MinLr=min(AblesungLr)
                MinLrInd=AblesungLr.index(MinLr)
                Ablesung[Lr[MinLrInd]]=Ablesung[Lr[MinLrInd]]+Korrektur             #Niedrigste LrAblesung erhält Korrektur
                
                
                for i in range(len(Lr)):                                                                                 
                    AblesungLr[i]=Ablesung[Lr[i]]                                   #Neuberechnung Schleifenvariable        
                MaxLr=max(AblesungLr)   
            
            
            
            
            
            
            MinLr=min(AblesungLr) 
               
            while(MinLr<MinAblesung):
            
                MinLrInd=AblesungLr.index(MinLr)                                    #Index Minimale LrAblesung
                Korrektur = (MinLr-MinAblesung-0.1)-((MinLr-MinAblesung-0.1)%-.1)   #Berechnet Korrekturwert(Vorzeichen geändert)   
                Ablesung[Lr[MinLrInd]]=Ablesung[Lr[MinLrInd]]-Korrektur             #Korrigiert minimalen Lr Wert
                
                MaxLr=max(AblesungLr)                                               
                MaxLrInd=AblesungLr.index(MaxLr)
                Ablesung[Lr[MaxLrInd]]=Ablesung[Lr[MaxLrInd]]+Korrektur             #Niedrigste LrAblesung erhält Korrektur
                
                
                for i in range(len(Lr)):                                                                                 
                    AblesungLr[i]=Ablesung[Lr[i]]                                   #Neuberechnung Schleifenvariable        
                MinLr=min(AblesungLr)
                
                
            for i in range(len(Lr)):                                               #Setzt Schleifenvariable der äußeren Schleife neu                                  
                AblesungLr[i]=Ablesung[Lr[i]]                                                  
            MaxLr=max(AblesungLr)
        
        
        
        """
        Korrektur AblesungLv
        """
        
            
        AblesungLv=[None] * len(Lv)    
        
        for i in range(len(Lv)):                                                                                 
            AblesungLv[i]=Ablesung[Lv[i]]                                              #Alle Lv Ablesungen         
        MaxLv=max(AblesungLv)
        
        
        
        while(MaxLv>MaxAblesung):
        
            MaxLvInd=AblesungLv.index(MaxLv)                                    #Index Maximale LvAblesung
            Korrektur = (MaxLv-MaxAblesung+0.1)-((MaxLv-MaxAblesung+0.1)%0.1)   #Berechnet Korrekturwert   
            Ablesung[Lv[MaxLvInd]]=Ablesung[Lv[MaxLvInd]]-Korrektur             #Korrigiert maximalen Lv Wert
            
            MinLv=min(AblesungLv)
            MinLvInd=AblesungLv.index(MinLv)
            Ablesung[Lv[MinLvInd]]=Ablesung[Lv[MinLvInd]]+Korrektur             #Niedrigste LvAblesung erhält Korrektur
            
            
            for i in range(len(Lv)):                                                                                 
                AblesungLv[i]=Ablesung[Lv[i]]                                   #Neuberechnung Schleifenvariable        
            MaxLv=max(AblesungLv)
            
        
        
        MinLv=min(AblesungLv) 
           
        while(MinLv<MinAblesung):
        
            MinLvInd=AblesungLv.index(MinLv)                                    #Index Minimale LvAblesung
            Korrektur = (MinLv-MinAblesung-0.1)-((MinLv-MinAblesung-0.1)%-0.1)   #Berechnet Korrekturwert(Vorzeichen geändert)   
            Ablesung[Lv[MinLvInd]]=Ablesung[Lv[MinLvInd]]-Korrektur             #Korrigiert minimalen Lv Wert
            
            MaxLv=max(AblesungLv)
            MaxLvInd=AblesungLv.index(MaxLv)
            Ablesung[Lv[MaxLvInd]]=Ablesung[Lv[MaxLvInd]]+Korrektur             #Niedrigste LvAblesung erhält Korrektur
            
            
            for i in range(len(Lv)):                                                                                 
                AblesungLv[i]=Ablesung[Lv[i]]                                   #Neuberechnung Schleifenvariable        
            MinLv=min(AblesungLv)
            
            
            
        """
        Korrektur AblesungLr
        """
        AblesungLr=[None] * len(Lr)    
        
        for i in range(len(Lr)):                                                                                 
            AblesungLr[i]=Ablesung[Lr[i]]                                              #Alle Lr Ablesungen         
        MaxLr=max(AblesungLr)	
    	
    	
        while(MaxLr>MaxAblesung):
        
            MaxLrInd=AblesungLr.index(MaxLr)                                    #Index Maximale LrAblesung
            Korrektur = (MaxLr-MaxAblesung+0.1)-((MaxLr-MaxAblesung+0.1)%0.1)   #Berechnet Korrekturwert   
            Ablesung[Lr[MaxLrInd]]=Ablesung[Lr[MaxLrInd]]-Korrektur             #Korrigiert maximalen Lr Wert
            
            MinLr=min(AblesungLr)
            MinLrInd=AblesungLr.index(MinLr)
            Ablesung[Lr[MinLrInd]]=Ablesung[Lr[MinLrInd]]+Korrektur             #Niedrigste LrAblesung erhält Korrektur
            
            
            for i in range(len(Lr)):                                                                                 
                AblesungLr[i]=Ablesung[Lr[i]]                                   #Neuberechnung Schleifenvariable        
            MaxLr=max(AblesungLr)
            
        
        
        MinLr=min(AblesungLr) 
           
        while(MinLr<MinAblesung):
        
            MinLrInd=AblesungLr.index(MinLr)                                    #Index Minimale LrAblesung
            Korrektur = (MinLr-MinAblesung-0.1)-((MinLr-MinAblesung-0.1)%-0.1)   #Berechnet Korrekturwert(Vorzeichen geändert)   
            Ablesung[Lr[MinLrInd]]=Ablesung[Lr[MinLrInd]]-Korrektur             #Korrigiert minimalen Lr Wert
            
            MaxLr=max(AblesungLr)
            MaxLrInd=AblesungLr.index(MaxLr)
            Ablesung[Lr[MaxLrInd]]=Ablesung[Lr[MaxLrInd]]+Korrektur             #Niedrigste LrAblesung erhält Korrektur
                    
            for i in range(len(Lr)):                                                                                 
                AblesungLr[i]=Ablesung[Lr[i]]                                   #Neuberechnung Schleifenvariable        
            MinLr=min(AblesungLr)
        
        
        
        
        
        """
        Geänderte Werte wieder in NivZuege integrieren ink. Runden und Format
        """
            
        Niv.Distanz=ReFehlstellenStr(Distanz,StartDistanz,Niv.Fehlstellen,Startfehlstellen,3) #Fügt Fehlstellen inkl. ihrer Werte wieder ein
        Niv.Ablesung=ReFehlstellenStr(Ablesung,StartAblesung,Niv.Fehlstellen,Startfehlstellen,5)
        Niv.Art=ReFehlstellen(Art,StartArt,Niv.Fehlstellen,Startfehlstellen)
              
        
#        if(Niv.Distanz!=StartDistanz):
#            print("Die Zielweiten in Zug Nr."+ Niv.ZugNr +" wurden korrigiert")
#        else:
#            print("Die Zielweiten in Zug Nr."+ Niv.ZugNr +" wurden belassen")
#            
#        if(Niv.Ablesung!=StartAblesung):
#            print("Die Ablesungen in Zug Nr."+ Niv.ZugNr +" wurden korrigiert")
#        else:
#            print("Die Ablesungen in Zug Nr."+ Niv.ZugNr +" wurden belassen")
            
    
    
    """
    Ende der NivZuegeschleife  /  Wieder Zusammensetzen der Datei
    """
    
    Auslesen(NivZuege,Dateiname,DateinameK)

    

