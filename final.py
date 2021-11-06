from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import numpy as np
import tkinter as tk
import tkinter as ttk
import tkinter.ttk as ttk
import pandas as pd
from scipy import signal
import pyvisa as visa
import time
import csv
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('fivethirtyeight')
from matplotlib import cm
plt.rcParams["font.sans-serif"] = "Raleway"
filesave="MesuresFiltre.csv"
rm = visa.ResourceManager()
instruments = rm.list_resources()
global freqv
global decv
global pointv

class MainApp(Tk): #Tk
    def __init__(self):
        super().__init__()
        self.title("Plotting")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.configure(bg = "white")
        data = pd.read_csv("MesuresFiltre.csv") 
        results=data
        gain = 20*np.log10(data.iloc[:, 2] / data.iloc[:, 1])
        ## COnfigurartion graphs
        fig = Figure(figsize = (8, 6), 
                 dpi = 100) 
        #y = [i**2 for i in range(101)] 
        #plot1 = fig.add_subplot(111) 
        # Change tittle fig 
        b, a = signal.butter(1, 1.0/(2.7e6*42e-9), 'low', analog=True)
        w, h = signal.freqs(b, a)
        f_th = w/2*np.pi
        g_th = 20 * np.log10(abs(h))-12.4

        plot1 = fig.add_subplot(2, 1, 1)
        plot1.semilogx(f_th, g_th, '-')
        plot1.semilogx(data.iloc[:, 3], gain, '-o') #### Plotthin measured  gain
        plot1.grid(True, 'minor')
        plot1.grid(True, 'major')
        #plot1.ylabel('Gain (dB)')
        #plot1.xlabel('Frequency (Hz)')
        plot1.set_title('Gain vs Frequency')
        plot1.set_facecolor('#ffffff')
        
        plot1.plot() 

        ### Plot the phase#########
        plot2 = fig.add_subplot(2, 1, 2)
        
        f_me =data.iloc[:, 3]

        ph_th = np.angle(h)
        periods = 1.0/data.iloc[:, 3]
        ph_me = 2.0*np.pi*(data.iloc[:, 0]/periods)

       # x = np.array([0, 1, 2, 3])
        #y = np.array([10, 20, 30, 40])
        plot2.semilogx(f_th, ph_th, '-') ##################plotting therical  phase
        plot2.semilogx(f_me, ph_me, '-o') ##################plotting measured phase
        plot2.grid(True, 'minor')
        plot2.grid(True, 'major')
        #plot1.ylabel('Phase [rad]')
        #plot1.xlabel(u'Fréquence [Hz]')
        #plot1.title("Diagramme de Bode du filtre RC")
        plot2.legend(("Theirical","Practical"))
        plot2.margins(0.1, 0.1)


        plot2.set_title('Amplitude')
        
        plot2.set_title('Phase')
        # change background color 
        plot2.set_facecolor('#ffffff')
        plot2.plot()
        
        #Labelframe1
        self.labelFrame1 = LabelFrame(self, text = "Plotting", font = ("arial", 11, "bold"), bg = "white", fg = "black", width = 300, height = 750) #red
        self.labelFrame1.grid(row = 0, column = 0, padx=5, pady=10)

        #Labelframe2
        self.labelFrame2 = LabelFrame(self, text = "Bode Plot", font = ("arial", 15, "bold"), bg = "white", fg = "black", width = 800, height = 750)
        self.labelFrame2.grid(row = 0, column = 1, padx=5, pady=10)
        #################Controllerrs##################33
        ## add combobox
        ##Add label
        self.label1 = Label(self.labelFrame1, text = "Frequency base", font = ("arial", 10, "italic"), bg = "white", fg = "black")
        self.label1.place(x = 50, y = 40)
        self.combofreq = ttk.Combobox(self, text="Select Frequency", state="readonly")
        self.combofreq['values'] = ("10Hz", "100Hz", "50Hz", "1000Hz", "2000Hz")
        self.combofreq.current(1)
        #CHange size combobox
        self.combofreq.config(width = 10)
        self.combofreq.place(x = 180, y = 70) ### ITS IS CHANGING 30 PIXELES
        # get value combofrq
        
        ####Values obtained
        global freqv
        self.freqv=self.combofreq.get()
        freqv=self.combofreq.get()
        
        

        ##Add label
        self.label2 = Label(self.labelFrame1, text = "Decades", font = ("arial", 10, "italic"), bg = "white", fg = "black")
        self.label2.place(x = 50, y = 80)
        ##Add combobox
        self.combodec = ttk.Combobox(self, text="Select Decades", state="readonly")
        self.combodec['values'] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.combodec.current(0)
        

        #CHange size combobox
        self.combodec.config(width = 10)
        self.combodec.place(x = 180, y = 110) ### ITS IS CHANGING 30 PIXELES

        # get value combodec
        global decv
        decv=self.combodec.get()
        print(decv)

        ##Add label
        self.label3 = Label(self.labelFrame1, text = "Nropoints/decade", font = ("arial", 10, "italic"), bg = "white", fg = "black")
        self.label3.place(x = 50, y = 120)
        ##Add combobox
        self.combopoints = ttk.Combobox(self, text="Select Nropoints/decade", state="readonly")
        self.combopoints['values'] = ("10", "20", "30", "40", "50", "60", "70", "80", "90", "100")
        self.combopoints.current(0)
        #CHange size combobox
        self.combopoints.config(width = 10)
        self.combopoints.place(x = 180, y = 150) ### ITS IS CHANGING 30 PIXELES
        #get value combopoints
        
        global pointv
        self.pointv=self.combopoints.get()
        
        

        ## BUTTTON 1-----------------EXTRACT INFORMATION---------------------------------
        #self.button1 = Button(self.labelFrame1, text = "Demand", font = ("arial", 10, "bold"), bg = "white", fg = "black", command=group1)
        self.button1 = Button(self.labelFrame1, text = "Extract information", font = ("arial", 10, "bold"), bg = "white", fg = "black", command=self.vars1)
        self.button1.place(x = 160, y = 170)
        ## get value button1
        #################################button value###################

        ## Add label
        self.label4 = Label(self.labelFrame1, text = "Theoretical resistance kOhm", font = ("arial", 8, "italic"), bg = "white", fg = "black")
        self.label4.place(x = 30, y = 250)
        #Add spinbox
        self.freq1 = Spinbox(self.labelFrame1, from_ = 0, to = 100, width = 10)
        self.freq1.place(x = 180, y = 250)
        #get value freq1
        freq1v=self.freq1.get()
        print(freq1v)


        ## Add label 2
        self.label5 = Label(self.labelFrame1, text = "Theoretical Capacitance nF", font = ("arial", 8, "italic"), bg = "white", fg = "black")
        self.label5.place(x = 30, y = 280)
        #Add spinbox
        
        self.freq2 = Spinbox(self.labelFrame1, from_ = 0, to = 100, width = 10)
        # Spinbox default value

        self.freq2.place(x = 180, y = 280)
        


        ## add label nro points
        self.label6 = Label(self.labelFrame1, text = "Nropoints", font = ("arial", 10, "italic"), bg = "white", fg = "black")
        self.label6.place(x = 50, y = 310)
        #Add combobox
        self.combopoints2 = ttk.Combobox(self, text="Select Nropoints", state="readonly")
        self.combopoints2['values'] = ("10", "20", "30", "40", "50", "60", "70", "80", "90", "100")
        self.combopoints2.current(0)
        #CHange size combobox
        self.combopoints2.config(width = 10)
        self.combopoints2.place(x = 180, y = 340) ### ITS IS CHANGING 30 PIXELES
        # get value combopoints2
        #get value freq2
        freq1v=self.freq1.get()
        print(freq1v)
        freq2v=self.freq2.get()
        print(freq2v)
        point2v=self.combopoints2.get()
        print(point2v)



        ## BUTTON2------------------ MOST IMPORTANT------------------------------
        self.button2 = Button(self.labelFrame1, text = "Calculate theoretical function", font = ("arial", 10, "bold"), bg = "white", fg = "black", command=self.vars2)
        self.button2.place(x = 80, y = 370)
        #############COnnection section################
        ##Add label
        self.label7 = Label(self.labelFrame1, text = "Ossciloscope", font = ("arial", 10, "italic"), bg = "white", fg = "black")
        self.label7.place(x = 50, y = 450)
        ##Add combobox
        self.combogen = ttk.Combobox(self, text="Select Osciloscope", state="readonly")
        self.combogen['values'] = ("test Osciloscope")
        self.combogen.current(0)
        #get value combogen
        genv=self.combogen.get()
        print(genv)

        #CHange size combobox
        self.combogen.config(width = 10)
        self.combogen.place(x = 180, y = 480) ### ITS IS CHANGING 30 PIXELES

        ##Add label Generator
        self.label8 = Label(self.labelFrame1, text = "Generator", font = ("arial", 10, "italic"), bg = "white", fg = "black")
        self.label8.place(x = 50, y = 480)
        ##Add combobox
        self.combogen2 = ttk.Combobox(self, text="Select Generator", state="readonly")
        self.combogen2['values'] = ("test Generator")
        self.combogen2.current(0)
        #CHange size combobox
        self.combogen2.config(width = 10)
        self.combogen2.place(x = 180, y = 510) ### ITS IS CHANGING 30 PIXELES
        ## BUTTTON3 ------------------Instrument-----------Testing----------------
        self.button3 = Button(self.labelFrame1, text = "Instrument testing", font = ("arial", 10, "bold"), bg = "white", fg = "black", command=self.vars3)
        self.button3.place(x = 160, y = 540)
        ## Add label status
        self.label9 = Label(self.labelFrame1, text = "Status", font = ("arial", 12, "italic"), bg = "white", fg = "black")
        self.label9.place(x = 50, y = 600)
        
        ## Adding figures
        
        
        
        canvas = FigureCanvasTkAgg(fig, 
                               master = self.labelFrame2)   
        canvas.draw() 
    
        
        canvas.get_tk_widget().place(x = 0, 
                                     y = 0)
    
        
        toolbar = NavigationToolbar2Tk(canvas, 
                                    self.labelFrame2) 
        toolbar.update() 
    
        #canvas.get_tk_widget().place(x = 100, 
        #                            y = 200)
        canvas.get_tk_widget().pack(side = TOP, 
                                    fill = BOTH, 
                                    expand = True)
        
        ##### Add reset button
        
        
        #self.button4.place(x = 50, y = 700)
        #canvas.get_tk_widget().pack() 
  
        #window = Tk() 
        
        #window.title('Plotting in Tkinter') 
        
        #window.geometry("500x500")


        #self.plot()
    #########To test the instruments########################
    def vars3(self):
        rm = visa.ResourceManager()
        instruments = rm.list_resources()
        oscilloscope = rm.open_resource('USB0::0x1AB1::0x04CE::DS1ZA192712238::INSTR')
        generator= rm.open_resource('USB0::0x0400::0x09C4::DG1D184350683::INSTR')
        try:
            print(instruments)
            print(oscilloscope.query('*IDN?'))
            print(generator.query('*IDN?'))
            print("Instruments are working")
            oscilloscope.write(":RST")
            oscilloscope.write(":AUT")
        except:
            print("Instruments are not working")
        
#create function vars1
    def vars1(self):
        
        num_freqx=self.combofreq.get()
        num_decx=  self.combodec.get()
        num_pointsx=self.combopoints.get()
        print(num_freqx)
        print(num_decx)
        print(num_pointsx)
# create function vars2
    def vars2(self):
     
        freq1v=self.freq1.get()
        
        freq2v=self.freq2.get()
        
        point2v=self.combopoints2.get()
        print(freq1v)
        print(freq2v)
        print(point2v)
        #Call function concatenation
        var1='APPL'
        var2='SIN'
        var3='5000' ## Frecuency
        var4='3.0' ## Voltaje
        var5='0.0'
        fvar=concatenation(var1,var2,var3,var4,var5)
        print(fvar)
        ##################VISA PROCESS############################
        oscilloscope = rm.open_resource('USB0::0x1AB1::0x04CE::DS1ZA192712238::INSTR')
        generator= rm.open_resource('USB0::0x0400::0x09C4::DG1D184350683::INSTR')
        cont=1
        NB=20
        #NB=float(point2v)
        results = np.zeros((NB, 6))
        FREQ_MIN=1.1
        FREQ_MIN=float(freq1v)
        FREQ_MAX=3
        FREQ_MAX=float(freq2v)
        generator.write("APPL:SIN %f,3.3.0,0.0" % (FREQ_MAX/2,))
        time.sleep(2)
        oscilloscope.write(":AUT")
        time.sleep(5)
        filesave="MesuresFiltre.csv"
        cont=0
        for idx, f in enumerate(np.logspace(FREQ_MIN, FREQ_MAX, NB)):
            #generator.write("APPL:SIN 3000,3.0,-2.5")
            generator.write("APPL:SIN %f,3.3.0,0.0" % (f,))
            #generator.query("APPL:SIN %f,1.0,0.0" % (f,))
            time.sleep(2)
            if f>2000 and cont<1:
                oscilloscope.write(":AUT")
                time.sleep(3)
                cont=cont+1
            if f>50000 and cont<2:
                oscilloscope.write(":AUT")
                time.sleep(3)
                cont=cont+1
              
            #time.sleep(5) # Necesario para que se lleve a cabo el autoajuste
            #time.sleep(0.2)
            results[idx, 5] = float(oscilloscope.query(":MEASure:ITEM? FPHase,CHANnel2,CHANnel1", 0.8)) #:MEASure:FREQuency
            #time.sleep(0.2)
            results[idx, 0] = float(oscilloscope.query(":MEASure:ITEM? FDELay,CHANnel2,CHANnel1", 0.8)) #:MEASure:FREQuency
            #time.sleep(0.2)
            results[idx, 1] = float(oscilloscope.query(":MEASure:ITEM? VPP,CHANnel1",0.8)) ## :WAV:DATA?
            #time.sleep(0.5)
            results[idx, 2] = float(oscilloscope.query(":MEASure:ITEM? VPP,CHANnel2",0.8)) ##:MEASure:VRMS?
            #time.sleep(0.5)
            results[idx, 3] = float(oscilloscope.query(":MEASure:ITEM? FREQuency,CHANnel2",0.8)) ##:MEASure:VRMS?
            results[idx,4]=f
            time_base = oscilloscope.query(":TIM:SCAL?")
            #oscilloscope.write(":TIM:SCAL %f"%(float(time_base)/4.0))
            # Change to mode AC...
            #oscilloscope.write(":RST")
            #oscilloscope.write(":AUT")
            #oscilloscope.write(":CHAN1:COUP AC")
            
            #oscilloscope.write(":TIM:SCAL %f"%(float(time_base)/4.0))
            # Change to mode AC...
            oscilloscope.write(":CHAN2:COUP AC")
            cont=cont+1
            print(cont)
            print("APPL:SIN %f,1.0,0.0" % (f,))
            print(results[idx, 4])
            print(results[idx, 0])
            print(results[idx, 1])
            print(results[idx, 2])
            print('frequency=')
            print(results[idx, 3])
            print('therory f')
            print(f)
            #oscilloscope.write(":AUT")
            
            filesave="MesuresFiltre.csv"
        with open(filesave, "w") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["#FdDelay", "In (Vrms)", "Out (Vrms)", 'Frequency_real','Frequency_theory','Fphase'])
            writer.writerows(results)



def concatenation(var1,var2,var3,var4,var5):
    finalvar=var1+':'+var2+' '+var3+','+var4+','+var5
    return finalvar



if __name__ == "__main__":
    while (1):

        app = MainApp()
        button4 = Button(app, text = "Reset", font = ("arial", 10, "bold"), bg = "white", fg = "black", command = app.destroy)
        button4.place(x = 160, y = 640)
        app.update()
        app.mainloop()
        print(app.freqv) 
