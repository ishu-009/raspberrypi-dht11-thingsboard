import board
import adafruit_dht
import paho.mqtt.client as mqtt
at="eG5A6gAMmPaww1Dv48LI"
client=mqtt.Client()
client.username_pw_set(at)
client.connect("eu.thingsboard.cloud",1883,60)
dht=adafruit_dht.DHT11(board.D4)
while True:
    try:
        temp=dht.temperature
        hum=dht.humidity
        payload={
            "temperature": temp,
            "humidity": hum
            }
        client.publish(
            "v1/devices/me/telemetry",
            json.dumps(payload)
            )
        print(payload)
    except Exception as e:
        print(e)
        time.sleep(10)