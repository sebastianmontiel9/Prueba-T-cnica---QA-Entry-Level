import json
import os
from abc import ABC, abstractmethod
from typing import List, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- 1. CONFIGURACIÓN DE LA "BASE DE DATOS" JSON ---
DB_FILE = "database.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

def save_to_db(notification_data: dict):
    with open(DB_FILE, "r+") as f:
        data = json.load(f)
        data.append(notification_data)
        f.seek(0)
        json.dump(data, f, indent=4)

def get_all_from_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

# --- 2. PATRÓN STRATEGY PARA PROVEEDORES ---

class NotificationProvider(ABC):
    """Interfaz base para las estrategias de envío"""
    @abstractmethod
    def send(self, user_id: str, message: str):
        pass

class EmailProvider(NotificationProvider):
    def send(self, user_id: str, message: str):
        # Aquí iría la integración real con SendGrid, Mailchimp, etc.
        print(f"📧 Enviando Email a {user_id}: {message}")
        return True

class SMSProvider(NotificationProvider):
    def send(self, user_id: str, message: str):
        # Aquí iría la integración real con Twilio, AWS SNS, etc.
        print(f"📱 Enviando SMS a {user_id}: {message}")
        return True

class NotificationFactory:
    """Clase para seleccionar el proveedor según el canal"""
    _providers = {
        "email": EmailProvider(),
        "sms": SMSProvider()
    }

    @staticmethod
    def get_provider(channel: str) -> NotificationProvider:
        return NotificationFactory._providers.get(channel)

# --- 3. MODELOS DE DATOS (PYDANTIC) ---

class NotificationRequest(BaseModel):
    userId: str
    message: str
    channel: Literal["email", "sms"]

class NotificationListResponse(BaseModel):
    data: List[NotificationRequest]

# --- 4. APLICACIÓN FASTAPI ---

app = FastAPI(title="Notification Service API")

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/notifications", status_code=201)
async def create_notification(request: NotificationRequest):
    # 1. Seleccionar el proveedor usando el Patrón Strategy
    provider = NotificationFactory.get_provider(request.channel)
    
    if not provider:
        raise HTTPException(status_code=400, detail="Channel not supported")

    # 2. Ejecutar el "envío"
    success = provider.send(request.userId, request.message)
    
    if success:
        # 3. Persistir en el historial (JSON)
        notification_data = request.dict()
        save_to_db(notification_data)
        return {"status": "sent", "channel": request.channel}
    
    raise HTTPException(status_code=500, detail="Failed to send notification")

@app.get("/notifications", response_model=NotificationListResponse)
async def get_notifications():
    # Recuperar historial del archivo JSON
    history = get_all_from_db()
    return {"data": history}