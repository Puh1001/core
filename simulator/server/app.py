#server/app.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from collections import defaultdict

app = FastAPI()

# Cho phép CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorServer:
    def __init__(self):
        self.clients = set()
        self.sensor_data = defaultdict(dict)
        self.gateway_data = defaultdict(dict)
        
    async def register(self, websocket: WebSocket):
        await websocket.accept()
        self.clients.add(websocket)
        
    def unregister(self, websocket: WebSocket):
        self.clients.remove(websocket)
        
    async def broadcast(self, data: dict):
        """Gửi dữ liệu đến tất cả clients"""
        for client in self.clients:
            try:
                await client.send_json(data)
            except:
                await self.unregister(client)

sensor_server = SensorServer()

@app.post("/api/sensor-data")
async def receive_sensor_data(data: dict):
    """Nhận dữ liệu từ gateway"""
    gateway_id = data["gateway_id"]
    readings = data["readings"]
    
    # Lưu dữ liệu
    sensor_server.gateway_data[gateway_id] = readings
    
    # Broadcast dữ liệu mới đến tất cả clients
    await sensor_server.broadcast({
        "gateway_id": gateway_id,
        "readings": readings
    })
    
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Xử lý kết nối WebSocket từ clients"""
    await sensor_server.register(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        sensor_server.unregister(websocket)