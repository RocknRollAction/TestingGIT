# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:23:34 2020

@author: wycital
"""
#from Klassen import *
#from Einlesen import *
#from Auslesen import *


def KorrDstAbl(Dateiname, DateinameK, VarMaxDelta1,VarMaxDelta2,StreckenGrenze,MaxDistanz,MaxLrLvDelta,MinAblesung,MaxAblesung, Loeschmich):

    
    from Einlesen import Einlesen
#    from Klasse import *
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
        
        """
        Korrektur Ablesungen und Zielweiten
        """
    
        
        
        Niv=SummeRVfehler(Niv,Lr,Lv,VarMaxDelta1,VarMaxDelta2,Streckengrenze)      #Korrektur SummenFehler
        
        Niv=ZielweitenLrLv(Niv,Lr, Lv, MaxDistanz, MaxLrLvDelta)                   #Korrektur ZielweitenDifferenz
    
        Niv=AblesungLrLv(Niv,Lr,Lv, MaxAblesung, MinAblesung)   
        
        
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
        
        