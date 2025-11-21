# core/mqtt.py
import os
import ssl
import json
import threading
import paho.mqtt.client as mqtt_client

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "766a9e1259c64fa481f16df3d055bf25.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USER = os.getenv("MQTT_USER", "mqt12345")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "Wasd12345")

# Topics
WEIGHT_TOPIC = "iot/machine/weight"
GRADE_TOPIC = "iot/machine/grade"

# Global state
mqttGrade = None
mqttWeight = None

# Use a distinct name to avoid conflict with imported `mqtt` in main.py
client = mqtt_client.Client(client_id="fastapi-backend", protocol=mqtt_client.MQTTv311)


def on_message(_client, userdata, msg):
    global mqttWeight
    try:
        payload = msg.payload.decode().strip()
        print(f"📥 MQTT Received on {msg.topic}: {payload}")

        if msg.topic == WEIGHT_TOPIC:
            try:
                bobot = float(payload)
            except ValueError:
                data = json.loads(payload)
                if isinstance(data, dict):
                    bobot = float(data.get("bobot", 0))
                else:
                    bobot = float(data)
            mqttWeight = bobot
            print(f"💾 Stored weight: {mqttWeight}")
    except Exception as e:
        print(f"⚠️ Error handling MQTT message: {e}")


def on_connect(_client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Cloud")
        _client.subscribe(WEIGHT_TOPIC)
        print(f"📚 Subscribed to: {WEIGHT_TOPIC}")
    else:
        print(f"❌ MQTT connection failed (code {rc})")


def publish_grade(grade: str):
    global mqttGrade
    mqttGrade = grade
    client.publish(GRADE_TOPIC, json.dumps({"grade": grade}), qos=1, retain=True)
    print(f"📤 Published grade '{grade}' to {GRADE_TOPIC}")


def init_mqtt():
    """Initialize and start MQTT client in background thread."""
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.on_connect = on_connect
    client.on_message = on_message

    def run():
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_forever()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print("🧵 MQTT thread started")


# Optional: for introspection or debugging
__all__ = [
    "init_mqtt",
    "publish_grade",
    "mqttGrade",
    "mqttWeight",
    "GRADE_TOPIC",
    "WEIGHT_TOPIC"
]