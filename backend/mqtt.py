import paho.mqtt.client as mqtt
import ssl
import json
import threading
import os

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "4ed49e33a627487fae5850963dd4042d.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USER = os.getenv("MQTT_USER", "MQTTDG")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "Wasd12345")

# MQTT Topics
GRADE_TOPIC = "iot/machine/grade"
WEIGHT_TOPIC = "iot/machine/weight"

# Global MQTT client
client = mqtt.Client(client_id="fastapi-backend", protocol=mqtt.MQTTv311)

# Store latest grade in memory
dragonFruitGrade = None
dragonFruitWeight = None

# def determine_grade(weight: float) -> str:
#     if weight < 10:
#         return "C"
#     elif weight < 50:
#         return "B"
#     else:
#         return "A"

def on_message(client, userdata, msg):
    global dragonFruitGrade, dragonFruitWeight  
    try:
        payload = msg.payload.decode().strip()
        print(f"📥 MQTT Received on {msg.topic}: {payload}")

        if msg.topic == WEIGHT_TOPIC:
            # Try to parse as raw float first
            try:
                bobot = float(payload)
            except ValueError:
                # If it's not a raw number, try JSON
                data = json.loads(payload)
                if isinstance(data, dict):
                    bobot = float(data["bobot"])
                else:
                    raise ValueError("Unexpected payload format")

            dragonFruitWeight = bobot
            grade = determine_grade(bobot)
            dragonFruitGrade = grade

            client.publish(GRADE_TOPIC, json.dumps({"grade": grade}))
            print(f"📤 Published grade '{grade}' to {GRADE_TOPIC}")
    except Exception as e:
        print(f"⚠️ Error in MQTT message handler: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Cloud")
        client.subscribe(WEIGHT_TOPIC)
        print(f"📚 Subscribed to topic: {WEIGHT_TOPIC}")
    else:
        print(f"❌ MQTT Connection failed with code {rc}")

def init_mqtt():
    """Start MQTT client in background thread."""
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.on_connect = on_connect
    client.on_message = on_message

    def run():
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_forever()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return client

# Debugging exports
__all__ = [
    "init_mqtt", 
    "client", 
    "GRADE_TOPIC", 
    "WEIGHT_TOPIC",
    "dragonFruitGrade", 
    "dragonFruitWeight" 
]