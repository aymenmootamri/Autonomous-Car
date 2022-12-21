import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA,GPIO.OUT)
        GPIO.setup(self.In1A,GPIO.OUT)
        GPIO.setup(self.In2A,GPIO.OUT)
        GPIO.setup(self.EnaB,GPIO.OUT)
        GPIO.setup(self.In1B,GPIO.OUT)
        GPIO.setup(self.In2B,GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100);
        self.pwmA.start(0);
        self.pwmB = GPIO.PWM(self.EnaB, 100);
        self.pwmB.start(0);
    def moveF(self,speed=50,t=0):
            self.pwmA.ChangeDutyCycle(speed);
            GPIO.output(self.In1A.GPIO.LOW)
            GPIO.output(self.In2A.GPIO.HIGH)
            sleep(t)

            self.pwmB.ChangeDutyCycle(speed);
            GPIO.output(self.In1B.GPIO.LOW)
            GPIO.output(self.In2B.GPIO.HIGH)
            sleep(t)
            
    def moveB(self,speed=50,t=0):
            self.pwmA.ChangeDutyCycle(speed);
            GPIO.output(self.In1A.GPIO.HIGH)
            GPIO.output(self.In2A.GPIO.LOW)
            sleep(t)

            self.pwmB.ChangeDutyCycle(speed);
            GPIO.output(self.In1B.GPIO.HIGH)
            GPIO.output(self.In2B.GPIO.LOW)
            sleep(t)    
            
        def stop(self,t=0):
            self.pwmA.ChangeDutyCycle(0);
            self.pwmB.ChangeDutyCycle(0);
            
def main():
    motor.moveF(50,2)
    motor.stop(2)
    motor.moveB(50,2)
    motor.stop(2)

if __name__ == '__main__':
    motor= Motor(2,3,4,17,22,27)
    main()
