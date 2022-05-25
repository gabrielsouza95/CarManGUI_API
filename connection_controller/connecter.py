import serial

class SerialConnecter():
    def __init__( self, master ):
        ##serial releated
        self.runComunication = 0
        #variable related to serial port
        self.ser = None # = serial.Serial('COM4', 9600)#('/dev/ttyACM0', 9600) segundo valor é a iniciação da comunicação serial no raspberry        
