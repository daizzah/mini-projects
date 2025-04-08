# This is the script we run from the RPi
import RPi.GPIO as GPIO
import PCF8591 as ADC
import time
import paho.mqtt.client as mqtt
import json

BtnPin = 11
Gpin   = 12
Rpin   = 13
light_flash = 0
sensor_on = False


# Dictionary to easily iterate through each of them
parking_pins = {
    "P1": 35,
    "P2": 37,
    "P3": 36,
    "P4": 38,
    "P5": 40
}

# To setup all components
def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Gpin, GPIO.OUT)
	GPIO.setup(Rpin, GPIO.OUT)
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# Sets up each pins for the parking space
	for pin in parking_pins.values():
		GPIO.setup(pin, GPIO.IN)

	ADC.setup(0x48)

	# Starts the LED as OFF
	GPIO.output(Gpin, GPIO.LOW)
	GPIO.output(Rpin, GPIO.LOW)

def read_space_availabilities(): 
	# This creates a dictionary to check the availability of each parking space
	# Should look like this {'P1': 1, 'P2': 1, 'P3': 0, 'P4': 0, 'P5': 0}
    space_availabilities = {}
    for space, pin in parking_pins.items():
        availability = GPIO.input(pin)
        space_availabilities[space] = availability
    return space_availabilities


# This is ran when the ON/OFF button on the GUI is clicked
# It sets light_flash to 1 and flashes the LED
def light_on_message(client, userdata, message):
	global light_flash
	light_data = message.payload.decode("utf-8")
	print("Light data from client: ", light_data)

	if (light_data == "ON"):
		light_flash = 1
	else:
		light_flash = 0

# This is ran when the SEND button on the GUI is clicked
def display_on_message(client, userdata, message):
	display_data = message.payload.decode("utf-8")
	print("Display board: ", display_data)

def check_button_press():
	global sensor_on
	if GPIO.input(BtnPin) == 0:
		sensor_on = True
	if GPIO.input(BtnPin) == 1:
		sensor_on = False

def flash_green():
	# Flashes LED when light_flash is 1
	if light_flash == 1:
		GPIO.output(Gpin, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(Gpin, GPIO.LOW)
		time.sleep(0.2)
		GPIO.output(Gpin, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(Gpin, GPIO.LOW)


def read_sound_sensor():
	sensor_data = ""
	if sensor_on:
		sensor_data += "Sound sensor is on!\n"
		voice_value = ADC.read(0)
		if voice_value:
			sensor_data += "Value: " + str(voice_value) + " "
			if voice_value < 70:
				sensor_data += "Voice In!! "
	else:
		sensor_data += "Sound sensor is off! Hold button to turn sensor on. "

	return sensor_data

def publish():
	client.publish("sensor_dcb772", read_sound_sensor())

	json_data = json.dumps(read_space_availabilities())
	client.publish("parking_dcb772", json_data)

# Loop to run for the button/sensor and publishing
def loop():
	while True:
		check_button_press()
		flash_green()
		publish()

		time.sleep(0.5)

# Turns off LEDs at the end
def destroy():
	GPIO.output(Gpin, GPIO.LOW)
	GPIO.output(Rpin, GPIO.LOW)
	GPIO.cleanup()


if __name__ == '__main__':
	mqttBroker = "broker.hivemq.com"

	client = mqtt.Client("pi_client")  
	client.connect(mqttBroker)

	light_client = mqtt.Client("light_client")  
	light_client.connect(mqttBroker)

	light_client.on_message = light_on_message
	light_client.subscribe("light_dcb772")
	light_client.loop_start()

	display_client = mqtt.Client("display_client")  
	display_client.connect(mqttBroker)

	display_client.on_message = display_on_message
	display_client.subscribe("display_dcb772")
	display_client.loop_start()

	try:
		setup()
		loop()
	except KeyboardInterrupt: 
		destroy()