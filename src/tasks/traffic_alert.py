import logging
from typing import List

from hcloud import Client as HCloudClient

from src.db import GetDB, Client
from src.config import TELEGRAM_ADMINS_ID, BOT, TRAFFIC_MONITOR_ALERT_PERCENT
from src.lang import Dialogs

logger = logging.getLogger(__name__)


async def _fetch_usage(hclient: HCloudClient) -> List[dict]:
    servers = hclient.servers.get_all()
    usage: List[dict] = []
    for srv in servers:
        outgoing_gb = round(((srv.outgoing_traffic or 0) / 1024**3), 3)
        included_gb = round(((getattr(srv, "included_traffic", 0) or 0) / 1024**3), 3)
        used_percent = round((outgoing_gb / included_gb * 100), 1) if included_gb else None
        billable = round(max(outgoing_gb - included_gb, 0), 3) if included_gb else 0
        usage.append(
            {
                "id": srv.id,
                "name": srv.name,
                "out": outgoing_gb,
                "included": included_gb,
                "percent": used_percent,
                "billable": billable,
            }
        )
    return usage


async def check_traffic_alerts():
    async with GetDB() as db:
        clients = await Client.get_all(db)
    if not clients:
        return

    for client in clients:
        try:
            hclient = HCloudClient(token=client.secret)
            usage = await _fetch_usage(hclient)
            for item in usage:
                percent = item["percent"]
                if percent is not None and percent >= TRAFFIC_MONITOR_ALERT_PERCENT:
                    text = Dialogs.TRAFFIC_ALERT.format(
                        client=client.kb_remark,
                        server_name=item["name"],
                        server_id=item["id"],
                        out=item["out"],
                        included=item["included"],
                        percent=percent,
                        billable=item["billable"],
                    )
                    for admin_id in TELEGRAM_ADMINS_ID:
                        try:
                            await BOT.send_message(chat_id=admin_id, text=text)
                        except Exception:
                            pass
        except Exception as e:
            logger.error("TrafficCheck error for client %s: %s", client.id, e)
