# core/mqtt.py

import os
import json
import threading
import paho.mqtt.client as mqtt_client

# Load config from .env
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "").strip()
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "").strip()
MQTT_TLS = os.getenv("MQTT_TLS", "0") == "1"

WEIGHT_TOPIC = "iot/machine/weight"
GRADE_TOPIC = "iot/machine/grade"

# Global state
mqttGrade = None
mqttWeight = None

def get_mqtt_weight():
    return mqttWeight

def set_mqtt_weight(value):
    global mqttWeight
    mqttWeight = value

def get_mqtt_grade():
    return mqttGrade

def set_mqtt_grade(value):
    global mqttGrade
    mqttGrade = value

# Create client
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
                try:
                    data = json.loads(payload)
                    if isinstance(data, dict):
                        bobot = float(data.get("bobot", 0))
                    else:
                        bobot = float(data)
                except (json.JSONDecodeError, TypeError, ValueError):
                    print(f"⚠️ Unrecognized weight payload format: {payload}")
                    return
            mqttWeight = bobot
            print(f"💾 Stored weight: {mqttWeight}")
    except Exception as e:
        print(f"⚠️ Error handling MQTT message: {e}")

def on_connect(_client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to Mosquitto MQTT Broker")
        _client.subscribe(WEIGHT_TOPIC)
        print(f"📚 Subscribed to: {WEIGHT_TOPIC}")
    else:
        print(f"❌ MQTT connection failed with code {rc}")

def publish_grade(grade: str):
    global mqttGrade
    mqttGrade = grade
    client.publish(GRADE_TOPIC, json.dumps({"grade": grade}), qos=1, retain=True)
    print(f"📤 Published grade '{grade}' to {GRADE_TOPIC}")

def init_mqtt():
    """Initialize and start MQTT client in background."""
    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    if MQTT_TLS:
        import ssl
        client.tls_set(tls_version=ssl.PROTOCOL_TLS)

    client.on_connect = on_connect
    client.on_message = on_message

    def run():
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_forever()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print(f"🧵 MQTT background thread started → {MQTT_BROKER}:{MQTT_PORT}")

# # Optional: for introspection or debugging
# __all__ = [
#     "init_mqtt",
#     "publish_grade",
#     "mqttGrade",
#     "mqttWeight",
#     "GRADE_TOPIC",
#     "WEIGHT_TOPIC"
# ]
