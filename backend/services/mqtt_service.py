# services/mqtt_service.py

import json
import paho.mqtt.client as mqtt

# ============================
# Konfigurasi Mosquitto Broker
# ============================
MQTT_BROKER = "localhost"   # atau IP Raspberry Pi
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# Client global untuk FastAPI
mqtt_client = mqtt.Client(client_id="fastapi_backend")

# ============================
# Koneksi ke broker Mosquitto
# ============================
def mqtt_connect():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        mqtt_client.loop_start()  # penting: membuat client berjalan di background
        print(f"[MQTT] Connected to Mosquitto at {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print("[MQTT] Connection failed:", e)


# ============================
# Publish JSON
# ============================
def mqtt_publish(topic: str, payload: dict):
    """
    payload: dict → otomatis di-convert JSON
    """
    try:
        mqtt_client.publish(topic, json.dumps(payload))
        print(f"[MQTT] Published to {topic}")
    except Exception as e:
        print("MQTT publish error:", e)
