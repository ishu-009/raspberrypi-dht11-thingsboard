import json
import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

at = "eG5A6gAMmPaww1Dv48LI"

client = mqtt.Client()
client.username_pw_set(at)
client.connect("eu.thingsboard.cloud", 1883, 60)

dht = adafruit_dht.DHT11(board.D4)

TEMP_LIMIT = 30

try:
    while True:
        try:
            temp = dht.temperature
            hum = dht.humidity

            if temp > TEMP_LIMIT:
                GPIO.output(LED_PIN, GPIO.HIGH)
                alert = True
            else:
                GPIO.output(LED_PIN, GPIO.LOW)
                alert = False

            payload = {
                "temperature": temp,
                "humidity": hum,
                "alert": alert
            }

            client.publish(
                "v1/devices/me/telemetry",
                json.dumps(payload)
            )

            print(payload)

        except Exception as e:
            print(e)

        time.sleep(10)

except KeyboardInterrupt:
    print("Program stopped.")

finally:
    GPIO.output(LED_PIN, GPIO.LOW)  
    GPIO.cleanup()                   