import RPi.GPIO as GPIO
import time

# This test is made for a quick check of the gpios

# List of the in channels to test. When pressed they output a message.
in_chanels = []

# A list of output channels to test. These whill be switched on and off in a pattern.
out_chanels = []

def switch_called(channel):
	print 'Edge detected on channel %s'%channel
	
for in_channel in in_chanels:
    GPIO.setup(in_channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
    GPIO.add_event_detect(in_channel, GPIO.RISING, callback=switch_called, bouncetime=300)
    
for out_channel in out_chanels:
    GPIO.setup(out_channel, GPIO.OUT)
    GPIO.output(out_channel, GPIO.LOW)
	
print 'Start output test'
while True:
    for out_channel in out_chanels:
    	time.sleep(1)
    	GPIO.output(out_channel, not GPIO.input(out_channel))
    
    