import paho.mqtt.client as mqtt
import requests
import json

# MQTT Broker 設定（智器平台）
MQTT_BROKER = "save-mqtt.artifactdev.tw"
MQTT_PORT = 1883
MQTT_USERNAME = "james"
MQTT_PASSWORD = "TSN7d74ksHgswEHB"

# 後端 ingest API
INGEST_API = "atsave-mqtt-backend-production.up.railway.app:8000/ingest"

# MQTT 主題
MQTT_TOPIC = "/atsave/+/kpi"

def on_connect(client, userdata, flags, rc):
    print("✅ MQTT Connected with result code:", rc)
    client.subscribe(MQTT_TOPIC)
    print(f"🔄 Subscribed to topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        print(f"📥 Message received from topic: {msg.topic}")
        payload = json.loads(msg.payload.decode())
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")

        res = requests.post(INGEST_API, json=payload)
        print(f"↪️ POST to /ingest status: {res.status_code}")
    except Exception as e:
        print("❌ Error in message processing:", e)

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

print("🚀 Starting MQTT Listener...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
