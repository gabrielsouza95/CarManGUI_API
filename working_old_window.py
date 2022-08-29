def tkThreadingTest():
    from tkinter import Tk, Label, Button, StringVar # changed the * to 'Tk, Label, Button, StringVar' because it may limit memory usage
    import tkinter.font
    import sys
    import requests
    from time import sleep
    from arduinoserial import SerialPort as serial
    from working_old_baground_task_controller import BackgroundTask

    class UnitTestGUI:
        
        def __init__(self, master):
            self.master=master
            self.master.title('CarManGUI')
            self.master.geometry('820x320')
            
            ##button position related
            self.buttonYLine=85

            ##serial releated
            self.runComunication=0
            #variable related to serial port
            self.ser=None #=serial.Serial('COM4', 9600)#('/dev/ttyACM0', 9600) segundo valor é a iniciação da comunicação serial no raspberry        

            ##file related
            self.saveFile=False # variável que vai indicar se tem que gravar o arquivo ou não quando executar a thread da serial
            self.logFile=None 
            self.initial_offset=10
            self.positional_offset=self.initial_offset

            self.serialButton=Button(
                self.master, text='Conect Serial', command=self.onSerialClicked 
            )
            self.serialButton.place(
                x=self.positional_offset, 
                y=self.buttonYLine
            )
            self.master.update()
            self.serial_button_width = self.serialButton.winfo_width()
            self.positional_offset += self.serial_button_width

            self.arduinoButton=Button(
                self.master, text='Conect Arduino', command=self.onConectedClicked 
            )
            self.arduinoButton.place(
                x=self.positional_offset, 
                y=self.buttonYLine
            )
            self.master.update()
            self.arduino_button_width = self.arduinoButton.winfo_width()
            self.positional_offset += self.arduino_button_width

            self.recButton=Button(
                self.master, text='Rec', command=self.onRecClicked 
            )
            self.recButton.place(
                x=self.positional_offset, 
                y=self.buttonYLine
            )
            self.master.update()
            self.rec_button_width = self.recButton.winfo_width()
            self.positional_offset += self.rec_button_width

            self.cancelButton=Button(
                self.master, text='Stop', command=self.onStopClicked 
            )
            self.cancelButton.place(
                x=self.positional_offset, 
                y=self.buttonYLine
            )

            self.receviedInfo=StringVar()
            self.infoLabel=Label(master, textvariable=self.receviedInfo) 
            self.receviedInfo.set('Waiting connection...')
            self.infoLabel.place(
                x=20, 
                y=20
            )

            self.bgTaskSerial=BackgroundTask(self.serialStartConection) #BackgroundTask(self.myLongProcess)
            self.bgTaskArduino=BackgroundTask(self.serialConectionRead)
            self.bgTaskRecArduino=BackgroundTask(self.serialArduinoRec)
            
        def close(self):
            print ('close')
            try: self.bgTaskSerial.stop()
            except: pass
            try: self.bgTaskArduino.stop()
            except: pass
            try: self.bgTaskRecArduino.stop()
            except: pass            
            self.master.quit()

        def onSerialClicked(self):
            print ('onSerialClicked')
            try: 
                if self.ser == None: # or self.ser: #TO DO: não esquecer de checar problemas com a serial também além do None
                    self.bgTaskSerial.start()
            except: pass

        def onConectedClicked(self):
            print ('onConectedClicked')
            try: self.bgTaskArduino.start()
            except: pass
            
        def onRecClicked(self):
            print ('onRecClicked')
            try: self.bgTaskRecArduino.start()
            except: pass        

        def onStopClicked(self):
            print ('onStopClicked')
            try: self.bgTaskSerial.stop()
            except: pass
            try: self.bgTaskArduino.stop()
            except: pass
            try: self.bgTaskRecArduino.stop()
            except: pass 

        def serialStartConection (self, isRunningFunc=None): #myLongProcess(self, isRunningFunc=None): using the long process as the serial thread handler
            self.onSerialThreadUpdate ('Starting Serial connection...')
            try:
                self.ser=serial.Serial('/dev/ttyACM0', 9600) #('COM4', 9600)('/dev/ttyACM0', 9600) 
                if(self.ser.isOpen() == False):
                    self.ser.open()
                    self.onSerialThreadUpdate ('Conected to Arduino...')     
            except:
                self.onSerialThreadUpdate ('Error serial conection')     

        def serialConectionRead (self, isRunningFunc=None):
            self.keepGoing=1
            self.ser.write(str.encode('1#'))

            while self.keepGoing == 1:
                try:
                    if isRunningFunc():
                        self.lineRead=(self.ser.readline()).decode() #precisa do decode se não ele retorna b'{valores}'
                        self.onSerialThreadUpdate(self.lineRead)
                        self.onThreadUpdateCheckFileWrite(self.lineRead)
                    else:
                        self.onSerialThreadUpdate ('Serial connection stopped...')
                        self.ser.write(str.encode('0#'))
                        self.keepGoing=0
                except:
                    self.keepGoing=0 
                
            self.onSerialThreadUpdate('Serial connection stopped') 

        def serialArduinoRec (self, isRunningFunc=None):
            try: 
                if isRunningFunc():
                    self.onSerialThreadUpdate ('Sending request to start/stops rec...')
                    self.ser.write(str.encode('2#'))  
            except: pass        

        def onSerialThreadUpdate(self, status): #onMyLongProcessUpdate(self, status):
            print(str(status)) #print ('Process Update: %s' % (status))
            self.receviedInfo.set(str(status)) #self.statusLabelVar.set(str.encode(status))
            self.infoLabel.place(x=20, y=20)

        def onThreadUpdateCheckFileWrite(self, status):
            print('Checking if write file')
            self.firstElement=0
            self.lastElement=-1
            self.amountOfArduinoData=29
            self.conectionElements=str(status).split('_')
            self.lastConectElement=[]
            print('Nro elementos: ' + str(len(self.conectionElements)) + ' antes de verificar primeiro caracter e se grava ou não.')
            if not str(self.conectionElements[self.firstElement]): #Se ele conseguir fazer o split e o primeiro elemento for vazio, quer dizer que está recebendo certo a mensagem do arduino pela serial
                self.lastConectElement=self.conectionElements[self.lastElement]
                del self.conectionElements[:]
                self.conectionElements=str(self.lastConectElement).split(':')
                if str(self.conectionElements[self.firstElement]) == '0': #Lê o primeiro elemento que dita se grava o log ou não
                    self.saveFile=False
                else:
                    self.saveFile=True
                print(str(self.conectionElements[self.lastElement]))  

            if self.saveFile == True:
                self.logFile=open('/home/pi/Desktop/logJanPy.txt','a+') #'.\longJanPy.txt'
                self.logFile.write(str(status) + '\r')
                if not len(self.conectionElements) == self.amountOfArduinoData:
                    self.logFile.write(' quantidade de informações ' + str(len(self.conectionElements)) + ' difere da quantidade esperada. \n\r')
                self.logFile.close()

    root=Tk()    
    gui=UnitTestGUI(root)
    root.protocol('WM_DELETE_WINDOW', gui.close)
    root.mainloop()

if __name__ == '__main__': 
    tkThreadingTest()