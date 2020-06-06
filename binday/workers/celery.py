import os

from celery import Celery
from celery.schedules import crontab

from binday.workers.tasks import (
    add_bin_reading_task,
    send_push_notif_task,
    turn_on_led_task,
)

worker = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)


@worker.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # TODO Add proper timing.
    sender.add_periodic_task(
        crontab(minute="*/30"), add_bin_reading, name="Add bin reading task"
    )
    sender.add_periodic_task(
        crontab(minute="*/30"), turn_on_led, name="Turn on LED task"
    )
    sender.add_periodic_task(
        crontab(minute="0", hour="6,18"),
        send_push_notif,
        name="Send push notification task",
    )


@worker.task
def add_bin_reading():
    add_bin_reading_task()


@worker.task
def turn_on_led():
    turn_on_led_task()


@worker.task
def send_push_notif():
    send_push_notif_task()
