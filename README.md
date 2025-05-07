# ATSAVE MQTT + Flask Ingest Backend

本專案為智慧能效管理系統後端接收架構，提供：

- MQTT 訂閱功能（接收智器平台傳入之設備 KPI 數據）
- `/ingest` API 將資料寫入 Supabase 資料庫
- 適用於 Railway 雲端部署或本地執行測試

## 📦 專案結構

```
.
├── app.py              # Flask API /ingest 路由
├── mqtt_listener.py    # MQTT 訂閱 + POST 傳送到 /ingest
├── .env.template       # Supabase 連線設定模板
├── requirements.txt    # 依賴套件
└── Procfile            # Railway 部署設定（web + worker）
```

## 🌐 MQTT Broker 設定（由智器提供）

- Host: `save-mqtt.artifactdev.tw`
- Port: `1883`
- Username: `james`
- Password: `TSN7d74ksHgswEHB`
- Topic: `/atsave/+/kpi`

## 🧪 測試 JSON Payload 格式

```json
{
  "device_id": "device01",
  "product_model": "ST-500",
  "availability": 88.5,
  "quality": 97.1,
  "performance": 93.3,
  "power": 118,
  "emission": 56,
  "cost": 3.71,
  "eco_triggered": false,
  "timestamp": "2024-05-06T14:20:00"
}
```

## 🛠️ Railway 部署方式

1. 將本專案上傳至 GitHub
2. Railway → New Project → Deploy from GitHub
3. 設定環境變數：

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

4. Railway 自動讀取 `Procfile` 啟動：
   - `web: python app.py`
   - `worker: python mqtt_listener.py`

---

📬 如需前端顯示、ESG 報表、AI 建議模組，請搭配 ATSAVE 儀表板模組部署