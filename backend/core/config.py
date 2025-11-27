import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "DragonEye Backend"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost/dragonFruit")
    MQTT_BROKER: str = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))
    MQTT_TOPIC: str = "dragonFruit/device"

settings = Settings()
