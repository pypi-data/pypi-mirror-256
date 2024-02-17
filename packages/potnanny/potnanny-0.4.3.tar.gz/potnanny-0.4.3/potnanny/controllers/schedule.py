import asyncio
import logging
import datetime
from potnanny.utils import utcnow
from potnanny.models.schedule import Schedule


logger = logging.getLogger(__name__)


async def run_schedules(
    now:datetime.datetime = datetime.datetime.now().replace(second=0, microsecond=0)):
    """
    Run scheduled actions
    """

    tasks = []
    schedules = await Schedule.select()
    logger.debug(schedules)
    if not schedules:
        return

    for s in schedules:
        asyncio.create_task(s.run(now))
