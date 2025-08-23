import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import TRAFFIC_MONITOR_ENABLED
from .traffic_alert import check_traffic_alerts


logger = logging.getLogger(__name__)


class SimpleScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """Start the scheduler and add the job"""

        if TRAFFIC_MONITOR_ENABLED:
            self.scheduler.add_job(
                self._wrap_coroutine(check_traffic_alerts),
                trigger=CronTrigger(minute=0),
                id="traffic_usage_check",
                replace_existing=True,
                max_instances=1,
                coalesce=True,
            )
        self.scheduler.start()

    async def stop(self):
        """Stop the scheduler"""
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()

    def _wrap_coroutine(self, coro):
        """Wrapper async"""

        async def wrapper():
            try:
                await coro()
            except Exception as e:
                logger.error({e})

        return wrapper


TaskManager = SimpleScheduler()
