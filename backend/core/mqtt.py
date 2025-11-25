import os
import json
import threading
import time
import uuid
from typing import Optional

import paho.mqtt.client as mqtt

# import your grading entry point (should accept weight and return grade string)
# make sure services.grading_service.process_grading exists and is importable
from services.grading_service import process_grading

# --------------------------
# Configuration (from env)
# --------------------------
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER") or None
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD") or None
MQTT_TLS = os.getenv("MQTT_TLS", "0") == "1"  # set "1" to enable TLS
MQTT_KEEPALIVE = int(os.getenv("MQTT_CLIENT_KEEPALIVE", "60"))

WEIGHT_MIN = float(os.getenv("MQTT_WEIGHT_MIN", "0.0"))
WEIGHT_MAX = float(os.getenv("MQTT_WEIGHT_MAX", "2000.0"))

# Topics
WEIGHT_TOPIC = os.getenv("MQTT_TOPIC_WEIGHT", "iot/machine/weight")
GRADE_TOPIC = os.getenv("MQTT_TOPIC_GRADE", "iot/machine/grade")

# --------------------------
# MQTT client (unique id)
# --------------------------
_client_id = f"fastapi-backend-{os.getpid()}-{uuid.uuid4().hex[:6]}"
client = mqtt.Client(client_id=_client_id, protocol=mqtt.MQTTv311)

# State (exportable)
mqttWeight: Optional[float] = None
mqttGrade: Optional[str] = None

# Internal flag
_started = False


# --------------------------
# Helpers
# --------------------------
def _safe_parse_weight(payload: str) -> Optional[float]:
    """
    Try parse payload as float or JSON with key 'bobot'/'weight'.
    Returns None if cannot parse.
    """
    payload = payload.strip()
    # try plain float
    try:
        return float(payload)
    except Exception:
        pass

    # try JSON
    try:
        data = json.loads(payload)
        if isinstance(data, dict):
            for k in ("bobot", "weight", "w"):
                if k in data:
                    return float(data[k])
        # if it's a json number
        if isinstance(data, (int, float)):
            return float(data)
    except Exception:
        pass

    return None


def _is_valid_weight(w: float) -> bool:
    return (w is not None) and (WEIGHT_MIN <= w <= WEIGHT_MAX)


# --------------------------
# MQTT Callbacks
# --------------------------
def on_connect(client_, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connected to broker {MQTT_BROKER}:{MQTT_PORT} (client_id={_client_id})")
        # Subscribe to topics we care about
        client_.subscribe(WEIGHT_TOPIC)
        print(f"[MQTT] Subscribed to {WEIGHT_TOPIC}")

        # Optionally clear retained grade (uncomment if desired)
        # client_.publish(GRADE_TOPIC, payload=None, retain=True)

    else:
        print(f"[MQTT] Connect failed with rc={rc}")


def on_disconnect(client_, userdata, rc):
    print(f"[MQTT] Disconnected (rc={rc}). Will attempt reconnect automatically.")


def on_subscribe(client_, userdata, mid, granted_qos):
    print(f"[MQTT] Subscribed (mid={mid}, qos={granted_qos})")


def on_message(client_, userdata, msg):
    global mqttWeight, mqttGrade
    try:
        payload = msg.payload.decode(errors="ignore")
        print(f"[MQTT] Received on {msg.topic}: {payload}")

        if msg.topic == WEIGHT_TOPIC:
            w = _safe_parse_weight(payload)
            if w is None:
                print("[MQTT] Warning: cannot parse weight payload, ignoring.")
                return

            if not _is_valid_weight(w):
                print(f"[MQTT] Warning: weight {w} outside valid range [{WEIGHT_MIN}, {WEIGHT_MAX}], ignoring.")
                return

            mqttWeight = w
            print(f"[MQTT] Stored weight: {mqttWeight}")

            # Run grading in try/except to prevent callback crash
            try:
                print("[MQTT] Running automatic grading...")
                grade = process_grading(mqttWeight)
                mqttGrade = grade if isinstance(grade, str) else str(grade)
            except Exception as e:
                print(f"[MQTT] Error during grading: {e}")
                return  # don't publish if grading failed

            # Publish result (with QoS and retained)
            payload_out = json.dumps({
                "grade": mqttGrade,
                "weight": mqttWeight,
                "timestamp": int(time.time())
            })

            result = client.publish(GRADE_TOPIC, payload_out, qos=1, retain=True)
            # result is MQTTMessageInfo
            if getattr(result, "rc", None) == mqtt.MQTT_ERR_SUCCESS:
                print(f"[MQTT] Published grade '{mqttGrade}' to {GRADE_TOPIC}")
            else:
                print(f"[MQTT] Publish returned rc={getattr(result, 'rc', None)}")

    except Exception as exc:
        print(f"[MQTT] Handler error: {exc}")


# --------------------------
# Init / Start function
# --------------------------
def init_mqtt():
    """
    Initialize and start MQTT client loop in background thread.
    Safe to call multiple times (will no-op after first start).
    """
    global _started

    if _started:
        return client

    # configure user/pass if provided
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    # TLS if requested
    if MQTT_TLS:
        try:
            client.tls_set()  # use default certs; for custom CA call with arguments
            print("[MQTT] TLS enabled for broker connection")
        except Exception as e:
            print(f"[MQTT] TLS setup failed: {e}")

    # handlers
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    # auto-reconnect backoff
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    # start loop in background thread
    def _run():
        backoff = 1
        while True:
            try:
                client.connect(MQTT_BROKER, MQTT_PORT, keepalive=MQTT_KEEPALIVE)
                client.loop_forever()
            except Exception as e:
                print(f"[MQTT] Connection error: {e}. Reconnecting in {backoff}s...")
                time.sleep(backoff)
                backoff = min(30, backoff * 2)

    thread = threading.Thread(target=_run, daemon=True, name="mqtt-loop")
    thread.start()

    _started = True
    return client


# --------------------------
# Utility publish function
# --------------------------
def publish_grade(grade: str, extra: Optional[dict] = None):
    """
    Publish a grade message programmatically.
    extra: additional key/value pairs to include in payload.
    """
    global mqttGrade
    mqttGrade = grade
    payload = {"grade": grade, "timestamp": int(time.time())}
    if extra and isinstance(extra, dict):
        payload.update(extra)

    try:
        res = client.publish(GRADE_TOPIC, json.dumps(payload), qos=1, retain=True)
        if getattr(res, "rc", None) == mqtt.MQTT_ERR_SUCCESS:
            print(f"[MQTT] Manually published grade '{grade}' to {GRADE_TOPIC}")
        else:
            print(f"[MQTT] Manual publish returned rc={getattr(res, 'rc', None)}")
    except Exception as e:
        print(f"[MQTT] Manual publish error: {e}")


# expose useful names
__all__ = [
    "init_mqtt",
    "client",
    "publish_grade",
    "WEIGHT_TOPIC",
    "GRADE_TOPIC",
    "mqttWeight",
    "mqttGrade",
]