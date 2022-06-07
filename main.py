"""
Main part of the process
"""
from tkinter import Tk
from process_controller import BackgroundTask
from gui_controller import GUILabel, GUIButton, GUIWindow

class tkThreadingTest():

    class UnitTestGUI:
        env_choices = ['ruindows', 'unix']
        def __init__( self, master ):
            self.window = GUIWindow(master, "CarManGUI", 420, 320)
            self.env = self.env_choices[0]
            ##file related
            self.saveFile = False # variável que vai indicar se tem que gravar o arquivo ou não quando executar a thread da serial
            self.logFile = None 

            self.serialButton = GUIButton(master, 'Conect Serial', self.onSerialClicked, 10, 84)
            self.arduinoButton = GUIButton(master, 'Conect Arduino', self.onConectedClicked, 90, 84)
            self.recButton = GUIButton(master, 'Rec', self.onRecClicked, 185, 84)
            self.cancelButton = GUIButton(master, 'Stop', self.onStopClicked, 240, 84)
            
            self.infoLabel = GUILabel(master, 'Waiting connection...', 20, 20)

            self.bgTaskSerial = BackgroundTask( self.serialStartConection )
            self.bgTaskArduino = BackgroundTask( self.serialConectionRead )
            self.bgTaskRecArduino = BackgroundTask( self.serialArduinoRec )
            
        def close( self ) :
            print ("close")
            try: self.bgTaskSerial.stop()
            except: pass
            try: self.bgTaskArduino.stop()
            except: pass
            try: self.bgTaskRecArduino.stop()
            except: pass            
            self.master.quit()

        def onSerialClicked( self ):
            print ("onSerialClicked")
            try: 
                if self.ser == None : # or self.ser : #TO DO : não esquecer de checar problemas com a serial também além do None
                    self.bgTaskSerial.start()
            except: pass

        def onConectedClicked( self ):
            print ("onConectedClicked")
            try: self.bgTaskArduino.start()
            except: pass
            
        def onRecClicked( self ):
            print ("onRecClicked")
            try: self.bgTaskRecArduino.start()
            except: pass        

        def onStopClicked( self ) :
            print ("onStopClicked")
            try: self.bgTaskSerial.stop()
            except: pass
            try: self.bgTaskArduino.stop()
            except: pass
            try: self.bgTaskRecArduino.stop()
            except: pass 

        def serialStartConection ( self, isRunningFunc = None ) : #using the long process as the serial thread handler
            self.onSerialThreadUpdate ( "Starting Serial connection..." )
            try :
                if self.env == self.env_choices[0]:    
                    self.ser = serial.Serial('COM4', 9600) 
                if self.env == self.env_choices[1]:
                    self.ser = serial.Serial('/dev/ttyACM0', 9600)
                    
                if(self.ser.isOpen() == False):
                    self.ser.open()
                    self.onSerialThreadUpdate ( "Conected to Arduino..." )     
            except :
                self.onSerialThreadUpdate ( "Error serial conection" )     

        def serialConectionRead ( self, isRunningFunc = None  ) :
            self.keepGoing = 1
            self.ser.write(str.encode("1#"))

            while self.keepGoing == 1 :
                try:
                    if isRunningFunc() :
                        self.lineRead = (self.ser.readline()).decode() #precisa do decode se não ele retorna b'{valores}'
                        self.onSerialThreadUpdate(self.lineRead)
                        self.onThreadUpdateCheckFileWrite(self.lineRead)
                    else :
                        self.onSerialThreadUpdate ( "Serial connection stopped..." )
                        self.ser.write(str.encode("0#"))
                        self.keepGoing = 0
                except :
                    self.keepGoing = 0 
                
            self.onSerialThreadUpdate( "Serial connection stopped" ) 

        def serialArduinoRec ( self, isRunningFunc = None ) :
            try: 
                if isRunningFunc() :
                    self.onSerialThreadUpdate ( "Sending request to start/stops rec..." )
                    self.ser.write(str.encode("2#"))  
            except : pass        

        def onSerialThreadUpdate( self, status ) :
            print( str(status) )
            self.infoLabel.update_text(str(status))
            
        def onThreadUpdateCheckFileWrite( self, status ) :
            print( "Checking if write file" )
            self.firstElement = 0
            self.lastElement = -1
            self.amountOfArduinoData = 29
            self.conectionElements = str(status).split('_')
            self.lastConectElement = []
            print( 'Nro elementos: ' + str(len(self.conectionElements)) + ' antes de verificar primeiro caracter e se grava ou não.')
            if not str(self.conectionElements[self.firstElement]) : #Se ele conseguir fazer o split e o primeiro elemento for vazio, quer dizer que está recebendo certo a mensagem do arduino pela serial
                self.lastConectElement = self.conectionElements[self.lastElement]
                del self.conectionElements[:]
                self.conectionElements = str(self.lastConectElement).split(':')
                if str(self.conectionElements[self.firstElement]) == '0' : #Lê o primeiro elemento que dita se grava o log ou não
                    self.saveFile = False
                else :
                    self.saveFile = True
                print(str(self.conectionElements[self.lastElement]))  

            if self.saveFile == True :
                self.logFile = open('/home/pi/Desktop/logJanPy.txt','a+') #'.\longJanPy.txt'
                self.logFile.write( str(status) + '\r' )
                if not len(self.conectionElements) == self.amountOfArduinoData :
                    self.logFile.write(' quantidade de informações ' + str(len(self.conectionElements)) + ' difere da quantidade esperada. \n\r')
                self.logFile.close()

if __name__ == "__main__": 
    root = Tk()
    window = tkThreadingTest(root)
    root.protocol("WM_DELETE_WINDOW", window.close)
    root.mainloop()
