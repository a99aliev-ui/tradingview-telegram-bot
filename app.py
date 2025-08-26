import os
import json
from datetime import datetime, timezone
from typing import Any, Dict

import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Telegram bot sozlamalari (token va chat_id .env faylidan olinadi)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")
WEBHOOK_SECRET     = os.getenv("WEBHOOK_SECRET")  # ixtiyoriy, lekin xavfsizlik uchun yaxshi

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise RuntimeError("Env sozlamalari yetarli emas: TELEGRAM_BOT_TOKEN va TELEGRAM_CHAT_ID kerak")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

app = FastAPI(title="TradingView ➜ Telegram Signals")

class SignalPayload(BaseModel):
    secret: str | None = None
    pair: str | None = None
    symbol: str | None = None
    signal: str | None = None
    price: str | float | None = None
    exchange: str | None = None
    timeframe: str | None = None
    strategy: str | None = None
    tp: str | float | None = None
    sl: str | float | None = None

    class Config:
        extra = "allow"  # qo‘shimcha maydonlarga ham ruxsat

def send_telegram(text: str) -> Dict[str, Any]:
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    r = requests.post(TELEGRAM_API_URL, json=payload, timeout=15)
    try:
