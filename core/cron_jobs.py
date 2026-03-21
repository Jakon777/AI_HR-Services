import asyncio
import logging
from typing import Optional

log = logging.getLogger("ai_hr.cron")

# 14 minutes in seconds
CRON_INTERVAL_SECONDS = 14 * 60


def run_scheduled_job() -> None:
    """
    Work that runs on each 14-minute tick while the server is up.
    Extend this (e.g. cleanup, reminders, cache refresh) as needed.
    """
    log.info("scheduled job: executing periodic tasks (placeholder)")


async def _fourteen_minute_loop(stop: asyncio.Event) -> None:
    log.info(
        "cron scheduler started | interval=%ss (14 minutes)",
        CRON_INTERVAL_SECONDS,
    )
    while not stop.is_set():
        try:
            await asyncio.wait_for(stop.wait(), timeout=CRON_INTERVAL_SECONDS)
            break
        except asyncio.TimeoutError:
            if stop.is_set():
                break
            try:
                run_scheduled_job()
            except Exception:
                log.exception("scheduled job raised an error")
    log.info("cron scheduler stopped")


def start_cron_scheduler() -> tuple[asyncio.Event, asyncio.Task]:
    stop = asyncio.Event()
    task = asyncio.create_task(_fourteen_minute_loop(stop))
    return stop, task


async def stop_cron_scheduler(
    stop: asyncio.Event, task: Optional[asyncio.Task]
) -> None:
    stop.set()
    if task is not None:
        try:
            await asyncio.wait_for(task, timeout=5.0)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
