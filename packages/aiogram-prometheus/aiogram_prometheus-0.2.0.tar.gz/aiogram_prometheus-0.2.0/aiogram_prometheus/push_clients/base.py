import abc
import asyncio
import logging
import time
from asyncio import AbstractEventLoop
from typing import Dict, Optional

from prometheus_client import REGISTRY, CollectorRegistry

from aiogram_prometheus.collectors import PushClientsCollector

logger = logging.getLogger('aiogram_prometheus')


class BasePushClient(abc.ABC):
    base_address: str
    job: str
    registry: CollectorRegistry
    grouping_key: Dict[str, str]

    _schedule_task: asyncio.Task

    def __init__(
        self,
        base_address: str,
        job: str,
        grouping_key: Optional[Dict[str, str]] = None,
        registry: CollectorRegistry = REGISTRY,
    ) -> None:
        self.base_address = base_address
        self.job = job
        self.grouping_key = grouping_key if grouping_key is not None else {}
        self.registry = registry

        self.collector = PushClientsCollector()
        registry.register(self.collector)

    @abc.abstractmethod
    async def push(self):
        pass

    async def __schedule_push(self, on_time: int = 15):
        _on_time_original = on_time

        while True:
            await asyncio.sleep(on_time)

            _start_time = time.time()

            await self.push()

            # try:

            # except BaseException as ex:
            #     logger.exception(ex)

            #     if isinstance(ex, asyncio.CancelledError):
            #         break

            #     on_time += _on_time_original

            #     raise ex

            # else:
            #     on_time = _on_time_original

            # self.collector.was_push(200, time.time() - _start_time)

    def schedule_push(self, on_time: int = 15, loop: Optional[AbstractEventLoop] = None):
        """Отправка метрик раз в on_time секунд

        Args:
            on_time (int, optional): Seconds

        """

        if loop is None:
            loop = asyncio.get_event_loop()

        self._schedule_task = loop.create_task(self.__schedule_push(on_time))
