import json
import paho.mqtt.client as mqtt

# ============================
# Konfigurasi Mosquitto Broker
# ============================
MQTT_BROKER = "localhost"     #
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# Single MQTT Client (direkomendasikan untuk FastAPI)
mqtt_client = mqtt.Client(client_id="fastapi_backend")


# ============================
# Koneksi ke Broker Mosquitto
# ============================
def mqtt_connect():
    """Menghubungkan FastAPI ke broker MQTT."""
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        mqtt_client.loop_start()  # Menjalankan MQTT secara background-thread
        print(f"[MQTT] Connected to {MQTT_BROKER}:{MQTT_PORT}")
        return True

    except Exception as e:
        print(f"[MQTT] Connection failed: {e}")
        return False


# ============================
# Publish dalam Format JSON
# ============================
def mqtt_publish(topic: str, payload: dict):
    """Mengirim payload JSON ke topik MQTT."""
    if not isinstance(payload, dict):
        raise ValueError("Payload harus berupa dict agar bisa di-JSON")

    try:
        mqtt_client.publish(topic, json.dumps(payload))
        print(f"[MQTT] Published → {topic}: {payload}")
        return True

    except Exception as e:
        print(f"[MQTT] Publish error: {e}")
        return False
