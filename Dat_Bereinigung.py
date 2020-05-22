# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 15:18:52 2020

@author: DrX
"""

from Klassen import *
from Einlesen import *
from Auslesen import *
from Hauptfunktionen import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from CSV import EinlesenCSV
from Header import *
 

#from tkFileDialog   import askopenfilename

class App(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.grid()                                          #Variablendeklaration
        config=ReadConfig("config.ini")                     #liest die config Date ein
        self.DateinameU=StringVar(value=".dat")
        self.DateinameK=StringVar(value="_K.dat")
        self.DateinameU.trace("w", self.DateinameAnpassen)
        self.MaxDeltaStreckenSumme1=DoubleVar(value=config[0])
        self.MaxDeltaStreckenSumme2=DoubleVar(value=config[1])
        self.Streckengrenze=DoubleVar(value=config[2])
        self.MaxLrLvStreckenDelta=DoubleVar(value=config[3])
        self.MinAblesung=DoubleVar(value=config[4])
        self.MaxAblesung=DoubleVar(value=config[5])
        self.MaxDistanz=DoubleVar(value=config[6])
        self.GrenzwertC=DoubleVar(value=config[7])
        self.NameCSV=StringVar(value=config[8])
        self.MaxDistWarn=DoubleVar(value=config[9])
        self.SollwertC=DoubleVar(value=config[10])
        self.Headerdatei=StringVar(value=config[11])
        
        self.NivZuege=[]
        self.Header=[]
        self.Justierung=[]
               
        
        Label(self, text="Dateiname Ursprungsdatei").grid(row=0,column=0, padx=0)      #Eingabefenster
        Entry(self, textvariable=self.DateinameU).grid(row=0,column=1, padx=0) 
                
        Label(self, text="Dateiname korrigiert").grid(row=1,column=0, padx=0)
        Entry(self, textvariable=self.DateinameK).grid(row=1,column=1, padx=0)      
        
        Label(self, text="MaxDeltaZielweitenSumme1").grid(row=2,column=0, padx=10)
        Entry(self, textvariable=self.MaxDeltaStreckenSumme1).grid(row=2,column=1, padx=0)
        
        Label(self, text="MaxDeltaZielweitenSumme2").grid(row=3,column=0, padx=10)
        Entry(self, textvariable=self.MaxDeltaStreckenSumme2).grid(row=3,column=1, padx=0)
        
        Label(self, text="Streckengrenze").grid(row=4,column=0, padx=10)
        Entry(self, textvariable=self.Streckengrenze).grid(row=4,column=1, padx=0)
               
        Label(self, text="MaxZielweitenDeltaLrLv").grid(row=5,column=0, padx=10)
        Entry(self, textvariable=self.MaxLrLvStreckenDelta).grid(row=5,column=1, padx=0)
        
        Label(self, text="MaxZielweite").grid(row=6,column=0, padx=0)
        Entry(self, textvariable=self.MaxDistanz).grid(row=6,column=1, padx=0) 
        
        Label(self, text="Warnwert Zielweite").grid(row=7,column=0, padx=10)
        Entry(self, textvariable=self.MaxDistWarn).grid(row=7,column=1, padx=0)
        
        Label(self, text="MinAblesung").grid(row=8,column=0, padx=10)
        Entry(self, textvariable=self.MinAblesung).grid(row=8,column=1, padx=0)
        
        Label(self, text="MaxAblesung").grid(row=9,column=0, padx=10)
        Entry(self, textvariable=self.MaxAblesung).grid(row=9,column=1, padx=0)
        
        Label(self, text="Justierung \n GrenzwertC ").grid(row=10,column=0, padx=10)
        Entry(self, textvariable=self.GrenzwertC).grid(row=10,column=1, padx=0)
        
        Label(self, text="Name Punktdatei").grid(row=11,column=0, padx=10)
        Entry(self, textvariable=self.NameCSV).grid(row=11,column=1, padx=0)
        
        Label(self, text="Sollwert Justierung").grid(row=12,column=0, padx=10)
        Entry(self, textvariable=self.SollwertC).grid(row=12,column=1, padx=0)
        
        Label(self, text="Header-Datei").grid(row=17,column=0, padx=10)
        Entry(self, textvariable=self.Headerdatei).grid(row=17,column=1, padx=0)  
        
        
        Button(self, text="Einlesen", command=self.EinlesenDat).grid(row=13, column=1, pady=10)
        Button(self, text="Auslesen", command=self.AuslesenDat).grid(row=14, column=1, pady=10)
                
        Button(self, text="Korrigieren Ablesung und Zielweiten", command=self.Korr).grid(row=15, column=1, pady=10)
        Button(self, text="Beenden", command=root.destroy).grid(row=13)        
        
#        Button(self, text="Eingegebene Punkthöhen prüfen", command=self.Starthoehen).grid(row=14, column=1, pady=10)
#        Button(self, text="Header Daten prüfen", command=self.Header).grid(row=15, column=1, pady=10)
        Button(self, text="Justierung prüfen", command=self.Just).grid(row=20,column=1, pady=10 )
        
        Button(self, text="Datei suchen", command=self.FileOpen).grid(row=0, column=2)
#        Button(self, text="Speicherort wählen", command=self.FileSave).grid(row=1, column=2)
        
    def EinlesenDat(self):
        Daten=Einlesen(self.DateinameU.get())
        self.NivZuege=Daten[0]
        self.Header=Daten[1]
        self.Justierung=Daten[2]
        print("Einlesen")
        print(self.Justierung)
        
    def AuslesenDat(self):

#        self.Header.get()        
#        self.Justierung.get() 
        print(self.Justierung)
        Auslesen(self.NivZuege,self.Justierung,self.DateinameU.get(), self.DateinameK.get())
        

    def Korr(self):                                 #Korrekturfunktion für Ablesung und Distanzen
        print("Ablesungen und Zielweiten werden korrigiert.")
        
        VarMaxDelta1=self.MaxDeltaStreckenSumme1.get()
        VarMaxDelta2=self.MaxDeltaStreckenSumme2.get()
        StreckenLimit=self.Streckengrenze.get()
        DateinameIN=self.DateinameU.get()
        DateinameOUT=self.DateinameK.get()        
        MaxLrLvDelta=self.MaxLrLvStreckenDelta.get()
        MinAbl=self.MinAblesung.get()
        MaxAbl=self.MaxAblesung.get()
        MaxDist=self.MaxDistanz.get() 
        MaxDistWarn=self.MaxDistWarn.get()
#        
        Ausgabe=KorrDstAbl(self.NivZuege,VarMaxDelta1,VarMaxDelta2,StreckenLimit,MaxDist,MaxLrLvDelta,MinAbl,MaxAbl,MaxDistWarn)   
        self.NivZuege=Ausgabe[0]
        Message=Ausgabe[1]
        
        messagebox.showinfo(title="Dateiausgabe", message= Message + "\n")
        
    def DateinameAnpassen(self,*a):                                 # Passt Ausgabedateinamen an
        self.DateinameK.set(self.DateinameU.get()[:-4] + "_K.dat")
        
    def Starthoehen(self):                                 # Prüft eingegebene Punkthöhen
        print("Eingegebene Punkthöhen werden geprüft.")
        
        AusgabePunkthoehen=Punkthoehen(self.NameCSV.get(), self.DateinameU.get())
        AusgabePunkthoehen.append( "\n \n Sollen die Ergebnisse gespeichert werden?" )
        
#        messagebox.showinfo(title="Punkthoehen Prüfung", message= AusgabePunkthoehen)
        
        MsgBox=messagebox.askquestion ("Punkthoehen Prüfung",AusgabePunkthoehen)
        if MsgBox=="yes":
            StrListSpeichern(AusgabePunkthoehen,"Punkthöhen_"+self.DateinameU.get()[0:-4]+".txt")
            print("Datei Punkthöhen_"+self.DateinameU.get()[0:-4]+".txt ausgegeben." )
        else:
            print("Keine Datei ausgegeben.")
            
    def Header(self):
        Message=HeaderKorr(self.Headerdatei.get(),self.DateinameU.get())
        messagebox.showinfo(title="Dateiausgabe", message=Message)
         
    def Just(self):

        #Exception für keine Justierung vorhanden
        if float(self.Justierung[4])>= self.GrenzwertC.get():           #Wenn C größer als der Grenzwert ist, kommt eine Abfrage
            
            MsgBox=messagebox.askquestion ("Justierung", "Die Justierung ist zu schlecht! Der Justierwert C beträgt " + str(self.Justierung[4]) +" DMS und übersteigt somit den Grenzwert von " + str(self.GrenzwertC.get()) +" DMS um " + str(round(self.Justierung[4]-self.GrenzwertC.get(),1)) + "! \n Soll der Wert auf "+ str(self.SollwertC.get()) +" angepasst und ausgegeben werden?")
            if MsgBox=="yes":
                Ausgabe=Justierung_Korr(self.Justierung, self.SollwertC.get())
                self.Justierung=Ausgabe[0]
                print(Ausgabe[1])

                
            else:
                print("Der Justierwert wurde beibehalten! Es wurde keine neue Datei ausgegeben.")
        else:
            messagebox.showinfo(title="Justierung",message="Die Justierung ist korrekt! Der Justierwert C beträgt " + str(self.Justierung[4]) +" DMS und liegt somit "+ str(round(self.GrenzwertC.get()-(self.Justierung[4]),1)) +" unter dem Grenzwert von " + str(self.GrenzwertC.get()) +" DMS! Jesus liebt dich!")
    def FileOpen(self):
        name=askopenfilename(filetypes = (("Dat-Dateien","*.dat"),("all files","*.*")))
        print(name)
        self.DateinameU.set(name)
#    def FileSave(self):
#        name=askopenfilename()
#        
#        self.DateinameK.set(name)
        

#-- Hauptprogramm: ----------------------------------------

root = Tk()
#root.geometry("600x500")
root.title("Skynet.exe")
app = App(root)
app.mainloop()




#MaxAblesung=3    