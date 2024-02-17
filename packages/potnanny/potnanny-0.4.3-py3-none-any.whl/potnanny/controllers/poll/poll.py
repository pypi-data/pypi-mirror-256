import asyncio
import logging
from potnanny.models.device import Device
from potnanny.controllers.pipeline import Pipeline
from potnanny.utils import utcnow
from .ble import BLEInterface
from .gpio import GPIOInterface
from .parse import Parser


logger = logging.getLogger(__name__)


class Poller:

    def __init__(self, *args, **kwargs):
        self.convert_c = False
        self.leaf_offset = -2
        self.devices = []
        self.now = utcnow()
        self._kwargs = kwargs

        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)


    async def poll(self):
        measurements = []

        if not self.devices:
            await self._load_devices()

        tasks = [
            BLEInterface().poll_devices(self.devices),
            GPIOInterface().poll_devices(self.devices)
        ]

        # collect measurements
        results = await asyncio.gather(*tasks)

        # parse and normalize measurement data
        if results:
            measurements = Parser(**self._kwargs).parse(results)
            logger.debug("MEASUREMENTS: %s" % measurements)

        # send measurement data into the pipeline
        p = Pipeline()
        t = asyncio.create_task(p.input(measurements))
        self.devices = []

        return measurements


    async def poll_id(self, pk:int):
        """
        Poll measurements only for a named device id
        """

        device = await Device.get_by_id(pk)
        logger.debug(f"Loaded individual device: {device.as_dict()}")
        if device is not None:
            self.devices = [device]
            await self.poll()
            self.devices = []


    async def _load_devices(self):
        results = await Device.select().where(Device.room_id != None)
        for d in results:
            self.devices.append(d)
