from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.core.scheduler import scheduler

from .tasks.smm_services import update_service_data


def start_scheduler():
    scheduler.add_job(
        update_service_data,
        IntervalTrigger(hours=1),
        id="update_smm_services",
        replace_existing=True,
    )

    scheduler.start()