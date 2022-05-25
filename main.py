from process_controller import BackgroundTask

class tkThreadingTest():

    class UnitTestGUI:
        
        def __init__( self, master ):
            
            ##button position related
            self.buttonYLine = 85

            ##file related
            self.saveFile = False # variável que vai indicar se tem que gravar o arquivo ou não quando executar a thread da serial
            self.logFile = None 

            self.serialButton = Button( 
                self.master, text="Conect Serial", command=self.onSerialClicked )
            self.serialButton.place(x = 10, y = self.buttonYLine)

            self.arduinoButton = Button( 
                self.master, text="Conect Arduino", command=self.onConectedClicked )
            self.arduinoButton.place(x = 90, y = self.buttonYLine)

            self.recButton = Button( 
                self.master, text="Rec", command=self.onRecClicked )
            self.recButton.place(x = 185, y = self.buttonYLine)

            self.cancelButton = Button( 
                self.master, text="Stop", command=self.onStopClicked )
            self.cancelButton.place(x = 240, y = self.buttonYLine)

            self.receviedInfo = StringVar()
            self.infoLabel = Label( master, textvariable=self.receviedInfo) 
            self.receviedInfo.set("Waiting connection...")
            self.infoLabel.place( x = 20, y = 20)

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

        def serialStartConection ( self, isRunningFunc = None ) : #myLongProcess( self, isRunningFunc=None ) : using the long process as the serial thread handler
            self.onSerialThreadUpdate ( "Starting Serial connection..." )
            try :
                self.ser = serial.Serial('/dev/ttyACM0', 9600) #('COM4', 9600)('/dev/ttyACM0', 9600) 
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

        def onSerialThreadUpdate( self, status ) : #onMyLongProcessUpdate( self, status ) :
            print( str(status) ) #print ("Process Update: %s" % (status))
            self.receviedInfo.set( str(status) ) #self.statusLabelVar.set( str.encode(status) )
            self.infoLabel.place( x = 20, y = 20)

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

    root = Tk()    
    gui = UnitTestGUI( root )
    root.protocol( "WM_DELETE_WINDOW", gui.close )
    root.mainloop()

if __name__ == "__main__": 
    window = tkThreadingTest()
