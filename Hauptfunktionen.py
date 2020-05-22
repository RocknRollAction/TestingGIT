from Klassen import *
from Einlesen import *
from Auslesen import *


def KorrDstAbl(NivZuege,VarMaxDelta1,VarMaxDelta2,StreckenGrenze,MaxDistanz,MaxLrLvDelta,MinAblesung,MaxAblesung,MaxDistWarn):


    if NivZuege==[]:
        Message=("Keine Datei eingelesen! Bitte zunächst Datei auswählen und auf Einlesen klicken.") 
        return [],Message
        raise Exception("Keine Datei eingelesen! Bitte zunächst Datei auswählen und auf Einlesen klicken.")      
    
#    NivZuege=Einlesen(Dateiname)     #List Datei ein und gibt NivZuege aus
#    NivZuege=NivZuege[0]
    Message=[]
    
    for i in range(len(NivZuege)):
        
        """
        Bereinigen
        """
        Niv=NivZuege[i]
        
        StartDistanz=(list(Niv.Distanz))                                           #Ursprungswerte werden gespeichert/ Als String mit.5 um späteren Nullfehler zu vermeiden
       
          
        StartAblesung=list(Niv.Ablesung)                                             #Ursprungswerte werden gespeichert/ Als String mit.5 um späteren Nullfehler zu vermeiden
        
        Startfehlstellen=Niv.Art.index("Lr")    
        StartArt=list(Niv.Art)
        
        
        Niv.Distanz=delFehlstellen(Niv.Distanz,Niv.Fehlstellen,Startfehlstellen)                #Löscht Wiederholungen/Zwischenblick, Startfehlstellen              
        Niv.Ablesung=delFehlstellen(Niv.Ablesung,Niv.Fehlstellen,Startfehlstellen)
        Art=delFehlstellen(Niv.Art,Niv.Fehlstellen,Startfehlstellen)
        
        
        
        Lr=getIndexPositions(Art,"Lr")
        Lv=getIndexPositions(Art,"Lv")
        
        
        LvDist = [ Niv.Distanz[i] for i in Lv]
        LrDist = [ Niv.Distanz[i] for i in Lr]
        
        maxLv=max(LvDist)
        maxLr=max(LrDist)
        
        MaxDist=max([maxLv, maxLr])                                            #Prüfung Warnwert überschritten        
        if MaxDist > MaxDistWarn:
            Message.append("In Zug Nr."+ Niv.ZugNr+" gab es Zielweiten mit einer länge von "+ str(MaxDist) +". Sie wurden korrigiert.")
#        else:
#            Message.append()
            
        
        
        
        
        """
        Korrektur Ablesungen und Zielweiten
        """
        
        if(Niv.Art[-1] =="Sr"):                                                 # Summenfehler soll nur bei vollständigen Zügen korrigiert werden      
            Niv=SummeRVfehler(Niv,Lr,Lv,VarMaxDelta1,VarMaxDelta2,StreckenGrenze)      #Korrektur SummenFehler
        
        Niv=ZielweitenLrLv(Niv,Lr, Lv, MaxDistanz, MaxLrLvDelta)                   #Korrektur ZielweitenDifferenz
    
        Niv=AblesungLrLv(Niv,Lr,Lv, MaxAblesung, MinAblesung)   
                
        """
        Geänderte Werte wieder in NivZuege integrieren ink. Runden und Format
        """
            
        Niv.Distanz=ReFehlstellen(Niv.Distanz,StartDistanz,Niv.Fehlstellen,Startfehlstellen) #Fügt Fehlstellen inkl. ihrer Werte wieder ein
        Niv.Ablesung=ReFehlstellen(Niv.Ablesung,StartAblesung,Niv.Fehlstellen,Startfehlstellen)
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
    Message=("Ablesungen und Zielweiten wurden bereinigt.")
#    Auslesen(NivZuege,Dateiname,DateinameK)
    return NivZuege,Message


def SummeRVfehler(Niv,Lr,Lv,VarMaxDelta1,VarMaxDelta2,StreckenGrenze):
    
    Ablesung=Niv.Ablesung
    Distanz=Niv.Distanz   
    

    MaxDelta=VarMaxDelta2
    DeltaSummeRV=Niv.SummeR-Niv.SummeV
    if StreckenGrenze==0:
        MaxDelta=VarMaxDelta1
    elif (Niv.SummeR+Niv.SummeV) < StreckenGrenze:             #Bestimmt welche maximale Streckendiff angewendet werden mus
        MaxDelta=VarMaxDelta1      
       
    # Hier evtl noch Random einbaue, sodass manchmal 0.25 m verwendet und manchmal 0.5m werden   
    SummenKorrektur=(DeltaSummeRV-MaxDelta+0.5) - ((DeltaSummeRV-MaxDelta+0.5)%0.5)      #Zu korrigierendes Delta mit Überhang auf 0.25M Werte normalisiert
       
       
       
    if DeltaSummeRV>MaxDelta:                                  #Summe Rückblicke ist größer und überschreitet Grenzwert
        
        LvDist = [ Distanz[i] for i in Lv]                         #nimmt nur Distanzen der Beobachtungsart LV
        MinLv=min(LvDist)                                            #findet min Distanz von LV
        
        MinDistInd=Distanz.index(MinLv)                    #Findet Ind des Min Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
#        MinDistInd=list(set(MinDistInd)-(set(MinDistInd)-set(Lv)))                  #Verschneidet DistanzenInd mit LVInd> Ergebnis minimale(r) LvWertInd        
#        MinDistInd=MinDistInd[0]                                       #Falls mehrere gleiche minimale Lv vorhanden
        
        Distanz[MinDistInd]=Distanz[MinDistInd]+SummenKorrektur
        Niv.SummeV=sum([ Distanz[i] for i in Lv]) 
        Distanz[-1]=Niv.SummeV
        print("Bei Zug Nr." + Niv.ZugNr + " DeltaSummeRV angepasst: Rückblicke um "+ str(SummenKorrektur) +"m vergrößert")
        
        
    elif (-1)*DeltaSummeRV>MaxDelta:                                    #SummeR<SummeL
        SummenKorrektur=-1*SummenKorrektur
        
        LrDist = [ Distanz[i] for i in Lr]                         #nimmt nur Distanzen der Beobachtungsart Lr
        MinLr=min(LrDist)                                            #findet min Distanz von Lr
        
        MinDistInd=Distanz.index(MinLr)                    #Findet Ind des Min Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
#        MinDistInd=list(set(MinDistInd)-(set(MinDistInd)-set(Lr)))                  #Verschneidet DistanzenInd mit LrInd> Ergebnis minimale(r) LrWertInd        
#        MinDistInd=MinDistInd[0]                                       #Falls mehrere gleiche minimale Lr vorhanden
        
        Distanz[MinDistInd]=Distanz[MinDistInd]+SummenKorrektur
        Niv.SummeR=sum([ Distanz[i] for i in Lr]) 
        Ablesung[-1]=Niv.SummeR
        
        print("Bei Zug Nr." + Niv.ZugNr + " DeltaSummeLr angepasst: Vorblicke um "+ str(SummenKorrektur) +"m  vergrößert")
    #    Distanz(MinDistIndex)=Distanz(MinDistIndex)
    else:
       
        print("Bei Zug Nr." + Niv.ZugNr + " keinen Summenfehler festgestellt")
            
    return Niv


def ZielweitenLrLv(Niv,Lr, Lv, MaxDistanz, MaxLrLvDelta):

    Ablesung=Niv.Ablesung
    Distanz=Niv.Distanz


    """
    Korrektur MaxDistanz Lr
    """   
    LrDist = [ Distanz[i] for i in Lr]
    MaxLr=max(LrDist)
    
    if sum(LrDist)/len(LrDist) > MaxDistanz:                                   #Prüfung ob Verteilbar
        raise Exception("Maximale Zielweiten Lr in Zug.Nr:" + Niv.ZugNr + " können nicht auf unter "+str(MaxDistanz)+"m verteilt werden. Abbruch!")  
    
    FehlerDistanz=True
    
    while(FehlerDistanz==True):                                                    #Schleife über MaxDistanzLrLv und RVDelta, Bei der Summe reicht ein Durchlauf
    
#        LrDist = [ Distanz[i] for i in Lr]                                         #Berechnet MaxLr
        
        while(MaxLr>MaxDistanz):
            if MaxLr> MaxDistanz :
                
                DistKorrektur=(MaxLr-MaxDistanz+0.25) - ((MaxLr-MaxDistanz+0.25)%0.25)     #Der Wert um den korrigiert wird in 0.25er Schritten
                
                MaxDistInd=Distanz.index(MaxLr)                        #Findet Ind des Max Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
#                MaxDistInd=list(set(MaxDistInd)-(set(MaxDistInd)-set(Lr)))         #Verschneidet DistanzenInd mit LrInd> Ergebnis Maximale(r) LrWertInd        
#                MaxDistInd=MaxDistInd[0]  
                
                
                LrDist = [ Distanz[i] for i in Lr]                                 #nimmt nur Distanzen der Beobachtungsart Lr
                MinLr=min(LrDist)                                                  #findet min Distanz von Lr
                
                MinDistInd=Distanz.index(MinLr)                         #Findet Ind des Min Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
#                MinDistInd=list(set(MinDistInd)-(set(MinDistInd)-set(Lr)))         #Verschneidet DistanzenInd mit LrInd> Ergebnis minimale(r) LrWertInd        
#                MinDistInd=MinDistInd[0] 
                
                Distanz[MinDistInd]=Distanz[MinDistInd]+DistKorrektur              #Kleiner Wert erhält Aufschlag
                
                Distanz[MaxDistInd]=Distanz[MaxDistInd]-DistKorrektur              #Großer Wert erhält Abschlag
                
#                    print("Bei Zug Nr." + str(Niv.ZugNr) + "ist die Lr Distanz in Zugzeile "+ MaxDistInd + "zu groß. Sie wird um "+ str(DistKorrektur) +"m  verkleinert")
#                    print("Als Ausgleich wurde in Zugzeile "+ str(MinDistInd) +"um "+ str(DistKorrektur)+ "verringert ")
                                    
                LrDist = [ Distanz[i] for i in Lr]                                 #Aktuallisierung der Liste und Schleifenvariable
                MaxLr=max(LrDist)
        
        """
        Korrektur MaxDistanz Lv
        """ 
        LvDist = [ Distanz[i] for i in Lv]
        MaxLv=max(LvDist)
        
        if sum(LvDist)/len(LvDist) > MaxDistanz:                                   #Prüfung ob Verteilbar
            raise Exception("Maximale Zielweiten Lv in Zug.Nr:" + Niv.ZugNr + " können nicht verteilt werden. Abbruch!")
        
        while(MaxLv>MaxDistanz):
            if MaxLv> MaxDistanz :
                
                DistKorrektur=(MaxLv-MaxDistanz+0.25) - ((MaxLv-MaxDistanz+0.25)%0.25)   #Der Wert um den korrigiert wird in 0.25er Schritten
                
                MaxDistInd=Distanz.index(MaxLv)                        #Findet Ind des Max Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
#                MaxDistInd=list(set(MaxDistInd)-(set(MaxDistInd)-set(Lv)))        #Verschneidet DistanzenInd mit LvInd> Ergebnis Maximale(r) LvWertInd        
#                MaxDistInd=MaxDistInd[0]  
                
                
#                LvDist = [ Distanz[i] for i in Lv]                                #????? nimmt nur Distanzen der Beobachtungsart Lv
                MinLv=min(LvDist)                                                 #findet min Distanz von Lv
                
                MinDistInd=Distanz.index(MinLv)                      #Findet Ind des Min Wertes in ALLEN Distanzen(falls Distanzen Mehrfach vorhanden)
#                MinDistInd=list(set(MinDistInd)-(set(MinDistInd)-set(Lv)))        #Verschneidet DistanzenInd mit LvInd> Ergebnis minimale(r) LvWertInd        
#                MinDistInd=MinDistInd[0] 
                
                Distanz[MinDistInd]=Distanz[MinDistInd]+DistKorrektur             #Kleiner Wert erhält Aufschlag
                
                Distanz[MaxDistInd]=Distanz[MaxDistInd]-DistKorrektur             #Großer Wert erhält Abschlag
                
#                    print("Bei Zug Nr." + str(Niv.ZugNr) + "ist die Lv Distanz in Zugzeile "+ str(MaxDistInd) + "zu groß. Sie wird um "+ str(DistKorrektur) +"m  verkleinert")
#                    print("Als Ausgleich wurde in Zugzeile "+ str(MinDistInd) + "um "+ str(DistKorrektur)+ "verringert ")
                
                LvDist = [ Distanz[i] for i in Lv]                                #Änderung der SChleifenvariable
                MaxLv=max(LvDist)

        
        
        
        """
        Korrektur RVDelta
        """
           
        
        LaengeLvLr=len(min([Lr,Lv], key=len))                                  # Falls Zug unvollständig ist, wird hier der kürzere LrLv verwendet. Sonst könnte ein IndexError entstehen
        DeltaLrLv=[None] * LaengeLvLr
        
        for i in range(LaengeLvLr):                                                   #Berechnen der LrLv Deltas                                   
            DeltaLrLv[i]=Distanz[Lr[i]]-Distanz[Lv[i]] 
        
            
        if(abs(sum(DeltaLrLv))>=len(DeltaLrLv)*MaxLrLvDelta):                     #Wenn Summe der Deltas größer ist als Anzahl Deltas* MaxDelta
            print("Achtung! Zielweitendifferenzen sind wahrscheinlich nicht verteilbar!")
       
        DeltaLrLvMax=max(DeltaLrLv, key=abs)                                   #Berechnen absolutes DeltaMax


        
        while(abs(DeltaLrLvMax)>=MaxLrLvDelta):
                                            
            DeltaLrLvMaxInd=DeltaLrLv.index(DeltaLrLvMax)        #Bestimmung Ind

            if(DeltaLrLvMax>=0):                                                   #DeltaMax >0  => Lr zu groß
                
                Korrektur = (DeltaLrLvMax-MaxLrLvDelta+0.1)-((DeltaLrLvMax-MaxLrLvDelta+0.1)%0.1)
                DeltaLrLvGegenInd=DeltaLrLv.index(min(DeltaLrLv))   #Gegenwert von DeltaLrLvMax auf den die Korrektur kompensiert wird. Hier das Paar wo Lr viel kleiner ist als Lv
                
                Distanz[Lr[DeltaLrLvMaxInd]] -= Korrektur           #Zieht vom Zu Hohen Lr die Korrektur ab
                Distanz[Lr[DeltaLrLvGegenInd]] += Korrektur         #Und gibt sie einem zu niedrigen LR
        
            elif(DeltaLrLvMax<0):                                                   #DeltaMAx <0  =>Lv zu groß
                
                Korrektur = (-DeltaLrLvMax-MaxLrLvDelta+0.1)-((-DeltaLrLvMax-MaxLrLvDelta+0.1)%0.1)
                DeltaLrLvGegenInd=DeltaLrLv.index(max(DeltaLrLv))  #Gegenwert von DeltaLrLvMax auf den die Korrektur kompensiert wird. Hier das Paar wo Lr viel größer ist als Lv
                
                Distanz[Lv[DeltaLrLvMaxInd]] -= Korrektur
                Distanz[Lr[DeltaLrLvGegenInd]] += Korrektur      


             
            for i in range(LaengeLvLr):                                                   #Berechnen der LrLv Deltas                                   
                DeltaLrLv[i]=Distanz[Lr[i]]-Distanz[Lv[i]] 
            DeltaLrLvMax=max(DeltaLrLv, key=abs) 
        """
        Prüfungen
        """
        
        LrDist = [ Distanz[i] for i in Lr]                                                    
        MaxLr=max(LrDist)
        LvDist = [ Distanz[i] for i in Lv]                               
        MaxLv=max(LvDist)
        
        if(MaxLr <= MaxDistanz and MaxLv <= MaxDistanz):            #Anpassung Schleifenvariable/ Falls durch die DeltaLrLv Anpassung MaxDistanz überschritten wurde
            FehlerDistanz=False
            
    return Niv
    """
     Die obige Prüfvariable enthält nur MaxDistanz, da Korrektur RVDelta solange durchgeführt wird bis es korrekt ist. 
     """
#def DeltaLrLv(Niv,Lr, Lv, MaxLrLvDelta):
#    
#    
#    
#    LaengeLvLr=len(min([Lr,Lv], key=len))                                  # Falls Zug unvollständig ist, wird hier der kürzere LrLv verwendet. Sonst könnte ein IndexError entstehen
#    DeltaLrLv=[None] * LaengeLvLr
#
#    
#    while(abs(DeltaLrLvMax)>=MaxLrLvDelta):
#    
#        for i in range(LaengeLvLr):                                                   #Berechnen der LrLv Deltas                                   
#            DeltaLrLv[i]=Distanz[Lr[i]]-Distanz[Lv[i]]  
#            
#        if(abs(sum(DeltaLrLv))>len(DeltaLrLv)*MaxLrLvDelta):                     #Wenn Summe der Deltas größer ist als Anzahl Deltas* MaxDelta
#            print("Achtung! Zielweitendifferenzen sind wahrscheinlich nicht verteilbar!")
#                
#        DeltaLrLvMax=max(DeltaLrLv, key=abs)                                   #Berechnen absolutes DeltaMax
#        DeltaMaxLrLvMaxInd=DeltaLrLv.index(DeltaLrLvMax)                       #Bestimmung Ind
#                
#    
#        if(DeltaLrLvMax>=0):                                                   #DeltaMax >0  => Lr zu groß
#            
#            Korrektur = (DeltaLrLvMax-MaxLrLvDelta+0.1)-((DeltaLrLvMax-MaxLrLvDelta+0.1)%0.1)
#            DeltaLrLvGegenInd=DeltaLrLv.index(min(DeltaLrLv))   #Gegenwert von DeltaLrLvMax auf den die Korrektur kompensiert wird. Hier das Paar wo Lr viel kleiner ist als Lv
#            
#            Distanz[Lr[DeltaLrLvMaxInd]] -= Korrektur           #Zieht vom Zu Hohen Lr die Korrektur ab
#            Distanz[Lr[DeltaLrLvGegenInd]] += Korrektur         #Und gibt sie einem zu niedrigen LR
#
#        elif(DeltaLrLvMax<0):                                                   #DeltaMAx <0  =>Lv zu groß
#            
#            Korrektur = (-DeltaLrLvMax-MaxLrLvDelta+0.1)-((-DeltaLrLvMax-MaxLrLvDelta+0.1)%0.1)
#            DeltaLrLvGegenInd=DeltaLrLv.index(max(DeltaLrLv))  #Gegenwert von DeltaLrLvMax auf den die Korrektur kompensiert wird. Hier das Paar wo Lr viel größer ist als Lv
#            
#            Distanz[Lv[DeltaLrLvMaxInd]] -= Korrektur
#            Distanz[Lr[DeltaLrLvGegenInd]] += Korrektur     
     
def AblesungLrLv(Niv,Lr,Lv, MaxAblesung, MinAblesung):   
    
    Ablesung=Niv.Ablesung
    Distanz=Niv.Distanz

    """
    Korrektur AblesungLr
    """
    #MaxLr    
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
        
        
        
        #MinLr
        
        
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
    
    #MaxLv
    
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
        
    #MinLv
    
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
             
    return Niv