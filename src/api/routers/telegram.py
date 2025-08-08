from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from eiogram.types import Update
from src.config import BOT, DP, TELEGRAM_WEBHOOK_SECRET_KEY


router = APIRouter(
    prefix="/api/telegram",
    tags=["Telegram"],
    include_in_schema=False,
)


@router.post("/webhook")
async def telegram_webhook(request: Request, bg: BackgroundTasks):
    if TELEGRAM_WEBHOOK_SECRET_KEY:
        secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret_token != TELEGRAM_WEBHOOK_SECRET_KEY:
            raise HTTPException(status_code=403, detail="Invalid secret key")
    data = await request.json()
    data["bot"] = BOT
    update = Update(**data)
    bg.add_task(DP.process, update)
    return {"result": "success"}
