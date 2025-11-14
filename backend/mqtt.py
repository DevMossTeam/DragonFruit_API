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
WEIGHT_TOPIC = "iot/machine/weight"
GRADE_TOPIC = "iot/machine/grade"

# Global MQTT client
client = mqtt.Client(client_id="fastapi-backend", protocol=mqtt.MQTTv311)

# Store latest data in memory
mqttGrade = None
mqttWeight = None

def on_message(client, userdata, msg):
    global mqttWeight
    try:
        payload = msg.payload.decode().strip()
        print(f"📥 MQTT Received on {msg.topic}: {payload}")

        if msg.topic == WEIGHT_TOPIC:
            # Try raw float first
            try:
                bobot = float(payload)
            except ValueError:
                # Try JSON format
                data = json.loads(payload)
                if isinstance(data, dict):
                    bobot = float(data["bobot"])
                else:
                    bobot = float(data)  # in case it's a JSON number

            mqttWeight = bobot
            print(f"💾 Stored weight: {mqttWeight}")
            # ⚠️ TIDAK ADA PERHITUNGAN GRADE → TIDAK ADA PUBLISH OTOMATIS
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

# Helper: publish grade manually (used by /test-send-grade)
def publish_grade(grade: str):
    global mqttGrade
    mqttGrade = grade
    client.publish(GRADE_TOPIC, json.dumps({"grade": grade}), qos=1, retain=True)
    print(f"📤 Published grade '{grade}' to {GRADE_TOPIC} (retained)")

# Exports
__all__ = [
    "init_mqtt",
    "client",
    "GRADE_TOPIC",
    "WEIGHT_TOPIC",
    "mqttGrade",
    "mqttWeight",
    "publish_grade"
]