import paho.mqtt.client as mqtt
import requests
import json

# MQTT Broker 設定（由智器提供）
MQTT_BROKER = "save-mqtt.artifactdev.tw"
MQTT_PORT = 1883
MQTT_USERNAME = "james"
MQTT_PASSWORD = "TSN7d74ksHgswEHB"

# Flask 後端 ingest API
INGEST_API = "http://localhost:8000/ingest"

# MQTT 訂閱主題
MQTT_TOPIC = "/atsave/+/kpi"

def on_connect(client, userdata, flags, rc):
    print("✅ Connected to MQTT Broker:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"📥 Received from {msg.topic}: {payload}")
        res = requests.post(INGEST_API, json=payload)
        print("↪️ Forwarded to /ingest:", res.status_code)
    except Exception as e:
        print("❌ Error:", e)

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()