import serial 

class Move:
    @staticmethod
    def avancer():
        ser = serial.Serial('COM4', 115200)
        data = b'\x61'
        ser.write(data)
        ser.close()

    @staticmethod
    def avance_rapide():
        ser = serial.Serial('COM4', 115200)
        data = b'\x76'
        ser.write(data)
        ser.close()

    @staticmethod
    def reculer():
        ser = serial.Serial('COM4', 115200)
        data = b'\x79'
        ser.write(data)
        ser.close()

    @staticmethod
    def recule_rapide():
        ser = serial.Serial('COM4', 115200)
        data = b'\x68'
        ser.write(data)
        ser.close()

    @staticmethod
    def stop():
        ser = serial.Serial('COM4', 115200)
        data = b'\x73'
        ser.write(data)
        ser.close()

    @staticmethod
    def avant_gauche():
        ser = serial.Serial('COM4', 115200)
        data = b'\x71'
        ser.write(data)
        ser.close()

    @staticmethod
    def avant_droite():
        ser = serial.Serial('COM4', 115200)
        data = b'\x65'
        ser.write(data)
        ser.close()

    @staticmethod
    def arriere_gauche():
        ser = serial.Serial('COM4', 115200)
        data = b'\x67'
        ser.write(data)
        ser.close()

    @staticmethod
    def arriere_droite():
        ser = serial.Serial('COM4', 115200)
        data = b'\x6A'
        ser.write(data)
        ser.close()

    @staticmethod
    def augmenter():
        ser = serial.Serial('COM4', 115200)
        data = b'\x78'
        ser.write(data)
        ser.close()
    
    @staticmethod
    def diminuer():
        ser = serial.Serial('COM4', 115200)
        data = b'\x77'
        ser.write(data)
        ser.close()
        
    
      
