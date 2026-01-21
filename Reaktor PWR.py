# -*- coding: utf-8 -*-
"""
s203991
"""
import tkinter as tk
import math

TemperaturaZC=13
TemperaturaReaktor=13
TemperaturaBoilerReaktor=13
TemperaturaBoilerPara=0
TemperaturaTurbina=0
TemperaturaInputKondenser=0
TemperaturaRadiator=0
TemperaturaRadiatorOutput=0
TemperaturaAmbient = 13


class Symulator:
    def __init__(self, root):
        self.Pompa = False
        self.Dump = False
        self.Komin = False
        self.CRLift=0
        
        self.root = root
        self.root.title("[s203991] Reaktor PWR - Pressurized Water Reactor")
        c = tk.Canvas(root, width=1500, height=750, bg="#021e36")
        c.pack()
        self.canvas = c
        self.draw()
    
    def draw(self):
        c=self.canvas###################################################
        c.create_rectangle(0,600,1500,750, fill="gray", outline="gray")
        self.jezioro= Jezioro(c)
        self.zbiornik = Zbiornik(c,self,self.jezioro)
        self.boiler =Boiler(c,self.zbiornik)
        self.reactor = Reactor(c,self)
        self.turbina = Turbina(c)
        self.komin = Komin(c,self.zbiornik)
        self.kondenser = Kondenser(c)
        self.radiator = Radiator(c, self.zbiornik)
        self.UI()
        
    def UI(self): #User int
        c=self.canvas


          
        c.create_text(10,630, text="Stan Pompy", font=("Arial", 12), fill="white", anchor="w")
        self.PompaPrzyc = tk.Button(c, text="OFF", command=self.PompaPrzycisk)
        self.PompaPrzyc.place(x=110, y=630-12)
        
        c.create_text(10,630+30, text="Odpływ", font=("Arial", 12), fill="white", anchor="w")
        self.DumpPrzyc = tk.Button(c, text="PUSH")
        self.DumpPrzyc.bind("<ButtonPress>", self.zbiornik.start_dump)
        self.DumpPrzyc.bind("<ButtonRelease>", self.zbiornik.stop_dump)
        self.DumpPrzyc.place(x=110, y=630+30-12)
        
        c.create_text(10,630+60, text="Stan Komina", font=("Arial", 12), fill="white", anchor="w")
        self.KominPrzyc = tk.Button(c, text="OFF", command=self.KominPrzycisk)
        self.KominPrzyc.place(x=110, y=630+60-12)
        
        
        self.suwak = tk.Scale(root, from_=0, to=100, orient='vertical', command=self.updateCR)
        self.suwak.set(100)
        self.suwak.place(x=1440, y=640)

    def SetSuwak(self, val):
        self.suwak.set(val)
    def updateCR(self,value):
        self.reactor.CRinsertion=int(value)
        self.reactor.RenderCR()
        
    def PompaPrzycisk(self):
        self.Pompa = not self.Pompa
        if self.PompaPrzyc["text"] == "ON":
            self.PompaPrzyc.config(text="OFF")
        else:
            self.PompaPrzyc.config(text="ON")
            self.zbiornik.CheckPump()
    
    def KominPrzycisk(self):
        self.Komin = not self.Komin
        if self.KominPrzyc["text"] == "ON":
            self.KominPrzyc.config(text="OFF")
            self.komin.KominON=False
        else:
            self.KominPrzyc.config(text="ON")
            self.komin.KominON=True
class Zbiornik:
    def __init__(self,canvas,Symulator, jezioro):
        global TemperaturaZC
        self.canvas = canvas
        self.Symulator=Symulator
        self.jezioro=jezioro
        c = canvas
        self.Fill=0
        self.Dumping=False
        self.Temperature=TemperaturaZC
        #main
        c.create_text( (580+710)/2, (360+530-200)/2, text="ZBIORNIK", font=("Arial", 20), fill="white")
        
        c.create_rectangle(580,360,710,530,fill="grey", outline="")
        #pompa
        c.create_rectangle(410,500,580,500+20,fill="grey", outline="")
        c.create_rectangle(410,500,410+20,560,fill="grey", outline="")
        c.create_oval((410+580)/2 -25, (500+500+20)/2+25, (410+580)/2+25, (500+500+20)/2-25, fill="gray", outline="")
        c.create_text( ((410+580)/2 -25+(410+580)/2+25)/2, ((500+500+20)/2+25+(500+500+20)/2-25)/2+35, text="POMPA", font=("Arial", 12), fill="white")
        #dump
        c.create_rectangle(670,530,670+20,560,fill="grey", outline="")
        
        #ToBoiler
        c.create_rectangle(710,450,930,450+20,fill="grey", outline="")
        c.create_rectangle(930-20,470,930,380,fill="grey", outline="")
        
        
        self.ciecz=c.create_rectangle(580+1,530-1,710-1,530+1-170*(self.Fill/1000),fill="blue", outline="")
        
        self.P1=c.create_rectangle(410+1,500+1,580,500+20-1,fill="grey", outline="")
        self.P2=c.create_rectangle(410+1,500+1,410+20-1,560,fill="grey", outline="")
        self.P3=c.create_oval((410+580)/2 -24, (500+500+20)/2+24, (410+580)/2+24, (500+500+20)/2-24, fill="grey", outline="")
        self.D=c.create_rectangle(670+1,530,670+20-1,560,fill="grey", outline="")
        
        self.B1 = c.create_rectangle(710,450+1,930-1,450+20-1,fill="grey", outline="")
        self.B2 = c.create_rectangle(930-20+1,470-1,930-1,380+1,fill="grey", outline="")
        
        c.create_text(370, 620, text="ZBIORNIK CHŁODZENIA", font=("Arial", 12), fill="white")
        self.tciecz=c.create_text( 300, 640, text=f"Zawartość: {self.Fill} L", font=("Arial", 12), fill="white", anchor="w")
        self.ttemp=c.create_text( 300, 640+5+12, text=f"Temperatura: {self.Temperature} °C", font=("Arial", 12), fill="white", anchor="w")
        
        
        c.create_rectangle(500-1,600+10,500+1,750-10,fill="white", outline="")   
        
        
        self.ProcessSelf()
        self.RenderLiquid()
        
    def Evaporate(self,val):
        if(self.Fill>=val):
            self.Fill=self.Fill-val
    def FillCheck(self):
        if self.Fill>1000: self.Fill=1000
        if self.Fill<0: self.Fill=0
        
    def RenderLiquid(self):
        self.FillCheck()
        c=self.canvas
        c.coords(self.ciecz, 580+1, 530-1, 710-1, 530-2-166*(self.Fill/1000))
        if self.Fill==0:
            c.itemconfig(self.ciecz, fill="grey")
        else:
            c.itemconfig(self.ciecz, fill="blue")
            
    def PourIn(self,val):
        
        global TemperaturaZC, TemperaturaAmbient
        if self.Fill==0:
            TemperaturaZC=TemperaturaAmbient
            self.RenderLiquid()
        if self.Fill<1000:
            self.Fill=self.Fill+val
            self.RenderLiquid()
            return True
        
    def CheckPump(self):
        c=self.canvas
        if self.Symulator.Pompa==True : 
            if self.PourIn(10): self.jezioro.PumpFrom(10)
            c.itemconfig(self.P1, fill="blue")
            c.itemconfig(self.P2, fill="blue")
            c.itemconfig(self.P3, fill="blue")
            self.canvas.after(100, self.CheckPump)
        else:
            c.itemconfig(self.P1, fill="grey")
            c.itemconfig(self.P2, fill="grey")
            c.itemconfig(self.P3, fill="grey")
    def DumpOut(self,val):
        if self.Fill>val:
            self.Fill=self.Fill-val
        else:
            self.Fill=0
        self.RenderLiquid()
    def CheckDump(self):
        c=self.canvas
        if self.Dumping :
            if self.Fill>0: 
                c.itemconfig(self.D, fill="blue")
                self.jezioro.PumpInto(20)
                self.DumpOut(20)
            else:  
                c.itemconfig(self.D, fill="grey")
            self.canvas.after(100, self.CheckDump)
        else:
            c.itemconfig(self.D, fill="grey")

    def start_dump(self,event):
        self.Dumping=True
        self.CheckDump()
        
    def stop_dump(self,event):
        self.Dumping=False
        
    def RenderPipe(self):
        c=self.canvas
        if self.Fill>0:
            c.itemconfig(self.B1, fill="blue")
            c.itemconfig(self.B2, fill="blue")
        else:
            c.itemconfig(self.B1, fill="grey")
            c.itemconfig(self.B2, fill="grey")
        
        
    def ProcessSelf(self):
        
        self.RenderPipe()
        self.ShiftTemp()
        self.RenderInfo()
        self.canvas.after(100, self.ProcessSelf)
    
    def ShiftTemp(self):
        global TemperaturaZC, TemperaturaRadiatorOutput, TemperaturaAmbient
        
        Vinner=self.Fill
        if TemperaturaRadiatorOutput>0:
            Vrad=5
        else:
            Vrad=0
        if self.Symulator.Pompa:
            Vp=10
        else:
            Vp=0
        if (Vinner+Vrad+Vp)>0:
            TemperaturaZC=(TemperaturaZC*Vinner+TemperaturaRadiatorOutput*Vrad+TemperaturaAmbient*Vp)/(Vinner+Vrad+Vp)
        else:
            TemperaturaZC=0
            
        
        self.Temperature=TemperaturaZC
        
    def RenderInfo(self):
        c=self.canvas
        Fill=round(self.Fill,2)
        Temp=round(self.Temperature,2)
        c.itemconfig(self.tciecz, text=f"Zawartość: {Fill} L")
        c.itemconfig(self.ttemp, text=f"Temperatura: {Temp} °C")  
class Boiler:
    def __init__(self, canvas,zbiornik):
        self.canvas = canvas
        self.ZB=zbiornik
        c=canvas
        #main
        c.create_rectangle(850,120,1050,380, fill="grey", outline="")
        c.create_text( (1050+850)/2, (120+380)/2, text="BOILER", font=("Arial", 20), fill="white")
        
        #ToReaktor
        c.create_rectangle(980,120,980+20,70, fill="grey", outline="")
        c.create_rectangle(980,70,1400,70+20, fill="grey", outline="")
        c.create_rectangle(1400,70,1400-20,470, fill="grey", outline="")
        c.create_rectangle(1340,470-20,1400,470, fill="grey", outline="")
        
        c.create_rectangle(980+1,120-1,980+20-1,70+1, fill="#8a0ac9", outline="")#
        c.create_rectangle(980+1,70+1,1400-1,70+20-1, fill="#8a0ac9", outline="")#
        c.create_rectangle(1400-1,70+1,1400-20+1,470-1, fill="#8a0ac9", outline="")#
        c.create_rectangle(1340+1,470-20+1,1400-1,470-1, fill="#8a0ac9", outline="")#
        
        #ToTurbine
        c.create_rectangle(930,120,930-20,70, fill="grey", outline="")
        c.create_rectangle(770,70,930,70+20, fill="grey", outline="")
        
        self.TP1=c.create_rectangle(930-1,120-1,930-20+1,70+1, fill="grey", outline="")
        self.TP2=c.create_rectangle(815,70+1,930-1,70+20-1, fill="grey", outline="")
        
        c.create_text(1210, 620, text="BOILER", font=("Arial", 12), fill="white")

        self.RCI=c.create_text( 1113, 640, text="RCoolIn: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        self.RCO=c.create_text( 1113, 640+5+12, text="RCoolOut: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        
        self.SO=c.create_text( 1113, 640+5+12+5+12+5+12, text="Steam: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        self.CI=c.create_text( 1113, 640+5+12+5+12+5+12+5+12, text="Coolant: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        
        c.create_rectangle(1110-1,600+10,1110+1,750-10,fill="white", outline="") 
        
        
        self.ProcessSelf(self.ZB)
    def ProcessSelf(self,zbiornik):
        global TemperaturaZC, TemperaturaReaktor, TemperaturaBoilerPara, TemperaturaBoilerReaktor
        
        Treaktor=TemperaturaReaktor

        n=0.6 #spr wymian
        
        
        if zbiornik.Fill>0 : 
            Tcool=TemperaturaZC
        else:
            Tcool=0
        
        if Tcool==0:
            TemperaturaBoilerReaktor=TemperaturaReaktor
            TemperaturaBoilerPara=0
        else:
            Para=Tcool+(Treaktor-Tcool)*n
            if Para>float(100) :
                TemperaturaBoilerPara=Para
                TemperaturaBoilerReaktor=Treaktor-(Treaktor-Tcool)*n
                zbiornik.PourIn(-5)
            else:
                TemperaturaBoilerReaktor=TemperaturaReaktor
                TemperaturaBoilerPara=0
        self.RenderSteam()
        self.RenderInfo()
        self.canvas.after(100,lambda: self.ProcessSelf(zbiornik))
    def RenderSteam(self):
        global TemperaturaBoilerPara
        c = self.canvas
        
        if TemperaturaBoilerPara>0:
            c.itemconfig(self.TP1, fill="white")
            c.itemconfig(self.TP2, fill="white")
        else:
            c.itemconfig(self.TP1, fill="grey")
            c.itemconfig(self.TP2, fill="grey")
    def RenderInfo(self):
        c=self.canvas
        global TemperaturaZC, TemperaturaReaktor, TemperaturaBoilerPara, TemperaturaBoilerReaktor
        RCoolIn = round(TemperaturaReaktor,2)
        RCoolOut = round(TemperaturaBoilerReaktor,2)
        Steam = round(TemperaturaBoilerPara,2)
        Coolant = round(TemperaturaZC,2)
        c.itemconfig(self.RCI, text=f"RCoolIn: {RCoolIn} °C")
        c.itemconfig(self.RCO, text=f"RCoolOut: {RCoolOut} °C")
        c.itemconfig(self.SO, text=f"Steam: {Steam} °C")
        c.itemconfig(self.CI, text=f"Coolant: {Coolant} °C")  
class Reactor:
    def __init__(self,canvas,sym):
        self.canvas = canvas
        self.CRinsertion=100
        self.sym = sym
        self.Flag= False
        c=canvas
        #main
        c.create_rectangle(1340,530,1240,150, fill="grey", outline="")
        c.create_text( (1340+1240)/2, (530+150)/2-210, text="REAKTOR", font=("Arial", 20), fill="white")
        c.create_rectangle(1340-1,150+1,1240+1,340, fill="black", outline="")
        c.create_rectangle(1340-1,340,1240+1,530-1, fill="#8a0ac9", outline="")
        
        c.create_rectangle(1340-1-30,350,1340-1-10,530-1, fill="#f2cb05", outline="")
        c.create_rectangle(1240+1+30,350,1240+1+10,530-1, fill="#f2cb05", outline="")
        
        #To boiler
        c.create_rectangle(1240,470-20,980,470, fill="grey", outline="")
        c.create_rectangle(980,380,980+20,470, fill="grey", outline="")
        
        c.create_rectangle(1240-1,470-20+1,980+1,470-1, fill="#8a0ac9", outline="")#
        c.create_rectangle(980+1,380+1,980+20-1,470-1, fill="#8a0ac9", outline="")#
        
        c.create_rectangle(1280,151,1300,340, fill="black", outline="")
        c.create_rectangle(1280,340,1300,530-1, fill="#8a0ac9", outline="")
        self.CR=c.create_rectangle(1280,151+178*(self.CRinsertion/100),1300,151+200+178*(self.CRinsertion/100), fill="#ffffff", outline="")
        
        c.create_text(1320, 620, text="REAKTOR", font=("Arial", 12), fill="white", anchor="w")
        c.create_text(1500-10,630, text="Control Rods", font=("Arial", 12), fill="white", anchor="e")
        
        self.ttemp=c.create_text( 1322, 640+5+12, text="Temp: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        
        c.create_rectangle(1310-1,600+10,1310+1,750-10,fill="white", outline="")
        self.CRIT=c.create_text( (1340+1240)/2, 550, text="", font=("Arial", 20), fill="red")
        self.RenderCR()
        self.ProcessSelf()
        
    def RenderCR(self):
        c=self.canvas
        c.coords(self.CR,1280,151+178*(self.CRinsertion/100),1300,151+200+178*(self.CRinsertion/100))
    def ProcessSelf(self):
        global TemperaturaReaktor, TemperaturaBoilerReaktor
        P_max=3000
        P=P_max*(1-self.CRinsertion/100)**1.6
        deltaTemp=P*0.2
        self.TempReakt = TemperaturaBoilerReaktor+deltaTemp
        if self.Flag:
            TemperaturaReaktor = 0
        else:
            TemperaturaReaktor = TemperaturaBoilerReaktor+deltaTemp
        self.CheckSCRAM()
        self.RenderInfo()
        self.canvas.after(100,self.ProcessSelf)
    def CheckSCRAM (self):
        if self.TempReakt >5000:
            self.canvas.itemconfig(self.CRIT, text="CRIT. TEMP")
            if not(self.CRinsertion==100):
                if(self.CRinsertion>100): 
                    self.CRinsertion=100
                else:
                    self.CRinsertion=self.CRinsertion+10
                    self.canvas.itemconfig(self.CRIT, text="SCRAM")
                    
            self.sym.SetSuwak(self.CRinsertion)
            self.RenderCR()
        else:
            self.canvas.itemconfig(self.CRIT, text="")
            
        if self.TempReakt>9000: self.Flag=True
    def RenderInfo(self):
        c=self.canvas
        global TemperaturaReaktor
        temp=round(TemperaturaReaktor,2)
        if self.Flag:
            c.itemconfig(self.ttemp, text="MELTDOWN", fill="red")
        else:
            c.itemconfig(self.ttemp, text=f"Temp: {temp} °C")
        
        
class Turbina:
    def __init__(self,canvas):
        self.canvas = canvas
        self.rotation = 0
        self.rotationTGT=0
        self.RPS=0
        c = canvas
        #main
        c.create_oval(700,20,820,140, fill="grey", outline="")
        c.create_text( (700+820)/2, (20+140+150)/2, text="TURBINA", font=("Arial", 12), fill="white")
        
        #rozdroża 600
        c.create_rectangle(600,70,710,70+20, fill="grey", outline="")
        
        r=self.rotation%360
        x=760
        y=80
        length=50
        
        self.p1=c.create_arc(700, 20, 820, 140, start=0, extent=180, fill="grey", outline="")
        self.p2=c.create_rectangle(600-1,70+1,710,70+20-1, fill="grey", outline="")
        self.p3=c.create_rectangle(900,70+1,810,70+20-1, fill="grey", outline="")
        c.create_oval(760-30, 80-30, 760+30, 80+30, fill="grey", outline="")
        
        self.f1=c.create_line(x, y, x + length*math.cos(math.radians(0+r)),   y - length*math.sin(math.radians(0+r)), fill="orange", width=5)
        self.f2=c.create_line(x, y, x + length*math.cos(math.radians(120+r)), y - length*math.sin(math.radians(120+r)), fill="orange", width=5)
        self.f3=c.create_line(x, y, x + length*math.cos(math.radians(240+r)), y - length*math.sin(math.radians(240+r)), fill="orange", width=5)
        
        c.create_text(1010, 620, text="TURBINA", font=("Arial", 12), fill="white")

        self.tsteamI=c.create_text( 923, 640, text="Steam In: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        self.tsteamO=c.create_text( 923, 640+5+12, text="Steam Out: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        self.trps=c.create_text( 923, 640+5+12+5+12, text="RPS: 0", font=("Arial", 12), fill="white", anchor="w")
        self.tpwr=c.create_text( 923, 640+5+12+5+12+5+12, text="POWER: 0 W", font=("Arial", 12), fill="white", anchor="w")
        c.create_rectangle(910-1,600+10,910+1,750-10,fill="white", outline="")       
        
        
        
        self.ProcessSelf()
    def ProcessSelf(self):
        c=self.canvas
        self.CheckRotation()
        self.RenderInfo()
        r=self.rotation%360
        x=760
        y=80
        length=50
        
        c.coords(self.f1,x, y, x + length*math.cos(math.radians(0+r)), y - length*math.sin(math.radians(0+r)))
        c.coords(self.f2,x, y, x + length*math.cos(math.radians(120+r)), y - length*math.sin(math.radians(120+r)))
        c.coords(self.f3,x, y, x + length*math.cos(math.radians(240+r)), y - length*math.sin(math.radians(240+r)))
        c.tag_raise(self.f1)
        c.tag_raise(self.f2)
        c.tag_raise(self.f3)
        c.after(100,self.ProcessSelf)
    def CheckRotation(self):
        global TemperaturaBoilerPara, TemperaturaTurbina
        c=self.canvas
        
        if TemperaturaBoilerPara>0:
            if TemperaturaBoilerPara>100:
                self.RPS=max(0,5*(TemperaturaBoilerPara-100)*0.02)
            TemperaturaTurbina = TemperaturaBoilerPara*0.6
            c.itemconfig(self.p1,fill="white")
            c.itemconfig(self.p2,fill="white")
            c.itemconfig(self.p3,fill="white")
        else:
            TemperaturaTurbina = 0
            c.itemconfig(self.p1,fill="grey")
            c.itemconfig(self.p2,fill="grey")
            c.itemconfig(self.p3,fill="grey")
            
            if self.RPS>0:
                self.RPS=self.RPS-0.05*self.RPS
                if self.RPS<0.01: self.RPS=0
            else:
                self.RPS=0
        
        
        self.SimulateInertia()
        
        
    def SimulateInertia(self):
        delta_rotation = self.RPS * 360 * 0.1
        self.rotation =self.rotation+ delta_rotation
        
                
    def RenderInfo(self):
        c=self.canvas
        global TemperaturaBoilerPara, TemperaturaTurbina
        SteamIn = round(TemperaturaBoilerPara,2)
        SteamOut = round(TemperaturaTurbina,2)
        RPM = round(self.RPS*60,2)
        PWR=1.5 * 5 * (TemperaturaBoilerPara - 100)*self.RPS
        Power = max(0,round(PWR,2))
        c.itemconfig(self.tsteamI, text=f"Steam In: {SteamIn} °C")
        c.itemconfig(self.tsteamO, text=f"Steam Out: {SteamOut} °C")
        c.itemconfig(self.trps, text=f"RPM: {RPM}")
        if Power <10000:
            c.itemconfig(self.tpwr,text=f"POWER: {Power} W")
        else:
            Power=round(Power/1000,2)
            c.itemconfig(self.tpwr,text=f"POWER: {Power} kW")
class Komin:
    def __init__(self,canvas,zbiornik):
        self.canvas=canvas
        self.KominON=False
        self.zbiornik=zbiornik
        c=canvas
        
        #rozdroże
        c.create_rectangle(590,80+20,630,80-20,fill="grey",outline="")
        #wybor
        self.pathKomin=c.create_rectangle(610+3,120,610-3,270,fill="red",outline="") #Komin
        self.pathKondenser=c.create_rectangle(480,80+3,570,80-3,fill="green",outline="") #kondenser
        
        
        #dym
        x1=528
        y1=192
        x2=543
        y2=163
        r1=20
        r2=30
        self.smoke1=c.create_oval(x1-r1,y1-r1,x1+r1,y1+r1,fill="#021e36", outline="")
        self.smoke2=c.create_oval(x2-r2,y2-r2,x2+r2,y2+r2,fill="#021e36", outline="")
        
        #komin
        c.create_rectangle(610,300+6,490,300-6,fill="grey",outline="") #komin rura
        c.create_polygon(
            500,200,
            560,200,
            550,220,
            550,240,
            570,290,
            490,290,
            510,240,
            510,220,
            fill="grey") #komin komin
        c.create_text( (570+490)/2, (290+290-40)/2, text="KOMIN", font=("Arial", 12), fill="white")
        
        
        
        #to kondenser
        c.create_rectangle(460,70,400,70+20,fill="grey",outline="")
        
        self.Pkondenser=c.create_rectangle(460,70+1,400,70+20-1,fill="grey",outline="")
        self.Pkomin=c.create_rectangle(610-1,300+6-1,490+1,300-6+1,fill="grey",outline="")
        
        self.ProcessSelf()
    def RenderSteamKondenser(self):
        global TemperaturaTurbina, TemperaturaInputKondenser
        c=self.canvas
        c.itemconfig(self.pathKondenser, fill="green")
        c.itemconfig(self.pathKomin, fill="red")
        if TemperaturaTurbina>0:
            c.itemconfig(self.Pkondenser, fill="white")
            TemperaturaInputKondenser = TemperaturaTurbina
        else:
            c.itemconfig(self.Pkondenser, fill="grey")
            TemperaturaInputKondenser = 0
        
        
    def RenderSteamKomin(self):
        global TemperaturaTurbina, TemperaturaInputKondenser
        TemperaturaInputKondenser = 0
        c=self.canvas
        c.itemconfig(self.pathKondenser, fill="red")
        c.itemconfig(self.pathKomin, fill="green")
        if TemperaturaTurbina>0:
            c.itemconfig(self.Pkomin, fill="white")
            c.itemconfig(self.smoke1, fill="white")
            c.itemconfig(self.smoke2, fill="white")
            self.zbiornik.Evaporate(5)
        else:
            c.itemconfig(self.Pkomin, fill="grey")
            c.itemconfig(self.smoke1, fill="#021e36")
            c.itemconfig(self.smoke2, fill="#021e36")
        
    def ProcessSelf(self):
        c=self.canvas
        if self.KominON:
            self.RenderSteamKomin()
            c.itemconfig(self.Pkondenser,fill="grey")
        else:
            self.RenderSteamKondenser()
            c.itemconfig(self.Pkomin, fill="grey")
            c.itemconfig(self.smoke1, fill="#021e36")
            c.itemconfig(self.smoke2, fill="#021e36")
        
        self.canvas.after(100,self.ProcessSelf)
class Kondenser:
    def __init__(self,canvas):
        c=canvas
        self.canvas=c
        #main
        c.create_rectangle(200,50,400,110,fill="grey",outline="")
        c.create_text( (200+400)/2, (160)/2, text="KONDENSER", font=("Arial", 20), fill="white")
        #to radiator
        c.create_rectangle(200,70,90,70+20,fill="grey",outline="")
        c.create_rectangle(90,70,90+20,120,fill="grey",outline="")
        
        self.PO1=c.create_rectangle(200-1,70+1,90+1,70+20-1,fill="grey",outline="")
        self.PO2=c.create_rectangle(90+1,70+1,90+20-1,120-1,fill="grey",outline="")
        
        c.create_text(800, 620, text="KONDENSER", font=("Arial", 12), fill="white")
        self.tpara=c.create_text( 723, 640, text="Para: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        self.twoda=c.create_text( 723, 640+5+12, text="Woda: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        c.create_rectangle(700-1,600+10,700+1,750-10,fill="white", outline="") 
        
        self.ProcessSelf()
    
    def ProcessSelf(self):
        self.Temperature()
        self.RenderInfo()
        self.canvas.after(100,self.ProcessSelf)
    
    def Temperature(self):
        c=self.canvas
        global TemperaturaInputKondenser, TemperaturaRadiator
        
        if TemperaturaInputKondenser>0:
            TemperaturaRadiator=max(25,TemperaturaInputKondenser*0.4)
            c.itemconfig(self.PO1, fill="blue")
            c.itemconfig(self.PO2, fill="blue")
        else:
            TemperaturaRadiator=0
            c.itemconfig(self.PO1, fill="grey")
            c.itemconfig(self.PO2, fill="grey")
    
    def RenderInfo(self):
        global TemperaturaRadiator, TemperaturaInputKondenser
        c=self.canvas
        Para=round(TemperaturaInputKondenser,2)
        Woda = round(TemperaturaRadiator,2)
        c.itemconfig(self.tpara, text=f"Para: {Para} °C")
        c.itemconfig(self.twoda, text=f"Woda: {Woda} °C")        
class Radiator:
    def __init__(self,canvas,zbiornik):
        self.canvas = canvas
        c= self.canvas
        self.zb=zbiornik
        
        #main
        c.create_rectangle(80,120,400,380,fill="grey",outline="")
        c.create_text( (80+400)/2, (120+380)/2, text="RADIATOR", font=("Arial", 20), fill="white")
        #to zbiornika
        c.create_rectangle(90,380,90+20,470,fill="grey",outline="")
        c.create_rectangle(90,470-20,580,470,fill="grey",outline="")
        
        self.PO1=c.create_rectangle(90+1,380+1,90+20-1,470-1,fill="grey",outline="")
        self.PO2=c.create_rectangle(90+1,470-20+1,580-1,470-1,fill="grey",outline="")
        
        c.create_text(600, 620, text="RADIATORY", font=("Arial", 12), fill="white")
        self.tInput=c.create_text( 523, 640, text="Input: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        self.tOutput=c.create_text( 523, 640+5+12, text="Output: 0 °C", font=("Arial", 12), fill="white", anchor="w")
        c.create_rectangle(500-1,600+10,500+1,750-10,fill="white", outline="")  
        
        self.ProcessSelf()
    def ProcessSelf(self):
        self.RenderInfo()
        self.Cooldown()
        self.canvas.after(100,self.ProcessSelf)
        
    def Cooldown(self):
        global TemperaturaRadiator, TemperaturaRadiatorOutput, TemperaturaZC, TemperaturaAmbient
        c=self.canvas
        if TemperaturaRadiator>0:
            TemperaturaRadiatorOutput = TemperaturaRadiator-(TemperaturaRadiator-TemperaturaAmbient)*0.3
            c.itemconfig(self.PO1, fill="blue")
            c.itemconfig(self.PO2, fill="blue")
            self.zb.PourIn(5)
            
        else:
            TemperaturaRadiatorOutput = 0
            c.itemconfig(self.PO1, fill="grey")
            c.itemconfig(self.PO2, fill="grey")
    
    def RenderInfo(self):
        c=self.canvas
        global TemperaturaRadiator, TemperaturaRadiatorOutput
        Input=round(TemperaturaRadiator,2)
        Output = round(TemperaturaRadiatorOutput,2)
        c.itemconfig(self.tInput, text=f"Input: {Input} °C")
        c.itemconfig(self.tOutput, text=f"Output: {Output} °C")

class Jezioro:
    def __init__(self, canvas):
        global TemperaturaAmbient
        self.canvas = canvas
        self.Fill=100000
        self.Temp=TemperaturaAmbient
        c=canvas
        c.create_rectangle(190,560,810,595,fill="#473500",outline="")
        self.tafla=c.create_rectangle(190,560,810,595,fill="blue",outline="")
        c.create_polygon(
            190,560,
            220,570,
            340,580,
            500,590,
            660,580,
            780,570,
            810,560,
            810,595,
            190,595,
            fill="#948337")
        
        self.level=c.create_text(190-2,(560+595)/2-10, text=f"{self.Fill} L", font=("Arial",10), fill="white", anchor="e")
        c.create_text(190-2,(560+595)/2+10, text=f"{self.Temp} °C", font=("Arial",10), fill="white", anchor="e")
        
        self.ProcessSelf()
    def ProcessSelf(self):
        self.RenderInfo()
        self.CheckLogic()
        self.RenderLake()
        self.canvas.after(100,self.ProcessSelf)
    
    def CheckLogic(self):
        if self.Fill<0: self.Fill=0
        if self.Fill>100000: self.Fill=100000
    def PumpFrom(self,val):
        self.Fill=self.Fill-val
        self.CheckLogic()
    
    def PumpInto(self,val):
        self.Fill=self.Fill+val
        self.CheckLogic()
    def RenderLake(self):
        self.canvas.coords(self.tafla,190,591,810,591-32*(self.Fill/100000))
    def RenderInfo(self):
        c=self.canvas
        c.itemconfig(self.level, text=f"{self.Fill} L")
        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    Program = Symulator(root)
    root.mainloop()