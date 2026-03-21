import asyncio
import logging
from typing import Optional

# ✅ Logging Configuration (IMPORTANT)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

log = logging.getLogger("ai_hr.cron")

# 14 minutes in seconds
CRON_INTERVAL_SECONDS = 14 * 60


def run_scheduled_job() -> None:
    """
    Work that runs on each 14-minute tick while the server is up.
    """
    log.info("========== CRON JOB STARTED ==========")

    try:
        log.info("Running periodic tasks...")

        # 👉 Add your actual logic here
        # Example:
        # cleanup_old_data()
        # send_notifications()

        log.info("Tasks executed successfully ✅")

    except Exception:
        log.exception("Error while executing scheduled job ❌")

    log.info("========== CRON JOB FINISHED ==========\n")


async def _fourteen_minute_loop(stop: asyncio.Event) -> None:
    log.info(
        "cron scheduler started | interval=%ss (14 minutes)",
        CRON_INTERVAL_SECONDS,
    )

    while not stop.is_set():
        try:
            log.info("Waiting for next run...")
            await asyncio.wait_for(stop.wait(), timeout=CRON_INTERVAL_SECONDS)
            break

        except asyncio.TimeoutError:
            if stop.is_set():
                break

            log.info("Triggering scheduled job now 🚀")

            try:
                run_scheduled_job()
            except Exception:
                log.exception("scheduled job raised an error")

    log.info("cron scheduler stopped")


def start_cron_scheduler() -> tuple[asyncio.Event, asyncio.Task]:
    log.info("Starting cron scheduler...")

    stop = asyncio.Event()
    task = asyncio.create_task(_fourteen_minute_loop(stop))

    return stop, task


async def stop_cron_scheduler(
    stop: asyncio.Event, task: Optional[asyncio.Task]
) -> None:
    log.info("Stopping cron scheduler...")

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

    log.info("Cron scheduler stopped successfully ✅")