#Raspberry Pi TB6612FNG Library
import RPi.GPIO as GPIO

#See https://raspberrypi.stackexchange.com/a/12967 for more info
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

class Motor:
	in1 = ""
	in2 = ""
	pwm = ""
	standbyPin = ""

	#Defaults
	hertz = 1000
	reverse = False #Reverse flips the direction of the motor

	#Constructor
	def __init__(self, in1, in2, pwm, standbyPin, reverse):
		self.in1 = in1
		self.in2 = in2
		self.pwm = pwm
		self.standbyPin = standbyPin
		self.reverse = reverse

		GPIO.setup(in1,GPIO.OUT)
		GPIO.setup(in2,GPIO.OUT)
		GPIO.setup(pwm,GPIO.OUT)
		GPIO.setup(standbyPin,GPIO.OUT)
		GPIO.output(standbyPin,GPIO.HIGH)
		self.p = GPIO.PWM(pwm, self.hertz)
		self.p.start(0)

	#Speed from -100 to 100
	def drive(self, speed):
		#Negative speed for reverse, positive for forward
		#If necessary use reverse parameter in constructor
		dutyCycle = speed
		if(speed < 0):
			dutyCycle = dutyCycle * -1

		if(self.reverse):
			speed = speed * -1

		if(speed > 0):
			GPIO.output(self.in1,GPIO.HIGH)
			GPIO.output(self.in2,GPIO.LOW)
		else:
			GPIO.output(self.in1,GPIO.LOW)
			GPIO.output(self.in2,GPIO.HIGH)
		self.p.ChangeDutyCycle(dutyCycle)

	def brake(self):
		self.p.ChangeDutyCycle(0)
		GPIO.output(self.in1,GPIO.HIGH)
		GPIO.output(self.in2,GPIO.HIGH)

	def standby(self, value):
		self.p.ChangeDutyCycle(0)
		GPIO.output(self.standbyPin,value)

	def __del__(self):
		GPIO.cleanup()
