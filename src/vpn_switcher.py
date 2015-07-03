#! /usr/bin/python
import time
import json
import requests
import subprocess
import urllib2
import logging
from pprint import pprint

try:
	import RPi.GPIO as GPIO
except ImportError:
	logging.info("No Module GPIO present")


wait_channel = None
vpn_configs = []
current_config_id = None
current_out_channel = None
current_country = None
switching = False
error = False


def setup():
	logging.basicConfig(filename='/var/log/vpn_switcher.log',level=logging.DEBUG)
	global wait_channel
	global vpn_configs

	json_config=open('/etc/vpn_switcher/vpn_switcher.config')
	config = json.load(json_config)
	json_config.close()

	wait_channel = config["wait_channel"]
	vpn_configs = config["vpn_configs"]

	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(wait_channel, GPIO.OUT )
	for vpn_config in vpn_configs:
		in_channel = vpn_config["in_channel"]
		out_channel = vpn_config["out_channel"]
		country = vpn_config["country"]
		config_id = vpn_config["config_id"]
		logging.info("Setup channels for config %s in:%s out:%s" % (config_id, in_channel, out_channel))
		if in_channel:
			GPIO.setup(in_channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
			GPIO.add_event_detect(in_channel, GPIO.RISING, callback=switch_called, bouncetime=300)
			pass
		if out_channel:
			GPIO.setup(out_channel, GPIO.OUT )
			GPIO.output(out_channel, GPIO.LOW)
		if not config_id:
			switch_config(config_id, country, out_channel)
			

def switch_config(config_id, country, out_channel):
	global current_config_id
	global current_out_channel
	global current_country
	global switching
	global error

	logging.info("Switching to config: %s for country: %s" % (config_id, country))
	error = False
	switching = True

	if current_out_channel:
		GPIO.output(current_out_channel, GPIO.LOW)
	subprocess.call("service openvpn stop" , shell=True)
	if config_id:
		subprocess.call("service openvpn start %s" % (config_id) , shell=True)
		time.sleep(10)

	# Check the correct country
	current_checks = 0
	max_checks = 5 
	result = False
	
	if not country:
		# no country to check
		result = True

	while not result and current_checks < max_checks :
		current_checks = current_checks + 1
		result = check_country(country)
		if not result:
			time.sleep(5)
	
	# Switching the out LED
	if result:
		if out_channel:
			current_config_id = config_id
			current_country = country
			current_out_channel = out_channel
			GPIO.output(current_out_channel, GPIO.HIGH)
	else:
		logging.error("Could not verify country: %s" % (country))
		error = True
	
	switching = False

def check_country(country):
	r = requests.get("http://www.trackip.net/ip?json")
	json_result = r.json()
	result_country = json_result["country"]
	logging.info("Checking country: %s found country: %s " % (country, result_country))
	success = result_country and result_country.lower() == country.lower()
	if not success:
		r = requests.get("http://ipinfo.io/json")
		json_result = r.json()
		result_country = json_result["country"]
		logging.info("Checking country: %s found country: %s " % (country, result_country))
		success = result_country and result_country.lower() == country.lower()
	return success 

def switch_called(channel):
	logging.info('Edge detected on channel %s'%channel)
	if not switching:		
		for config in vpn_configs:
			in_channel = config["in_channel"]
			out_channel = config["out_channel"]
			country = config["country"]
			config_id = config["config_id"]
			if in_channel == channel:
				switch_config(config_id, country, out_channel)
				
def main_loop():
	while True:
		time.sleep(0.1)
		if error:
			if GPIO.input(wait_channel) == GPIO.LOW:
				GPIO.output(wait_channel, GPIO.HIGH)
		else:
			# Blink if switching
			if switching or not current_out_channel:
				GPIO.output(wait_channel, not GPIO.input(wait_channel))
			else:
				GPIO.output(wait_channel, GPIO.LOW)
	
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	main_loop()
