# aiogram Prometheus Exporter

Module for exporting monitoring values for Prometheus

[![PyPI](https://img.shields.io/pypi/v/aiogram-prometheus)](https://pypi.org/project/aiogram-prometheus/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram-prometheus)](https://pypi.org/project/aiogram-prometheus/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/aiogram-prometheus)](https://gitlab.com/rocshers/python/aiogram-prometheus)
[![Docs](https://img.shields.io/badge/docs-exist-blue)](https://rocshers.gitlab.io/python/aiogram-prometheus/)

[![Test coverage](https://codecov.io/gitlab/rocshers:python/aiogram-prometheus/graph/badge.svg?token=3C6SLDPHUC)](https://codecov.io/gitlab/rocshers:python/aiogram-prometheus)
[![Downloads](https://static.pepy.tech/badge/aiogram-prometheus)](https://pepy.tech/project/aiogram-prometheus)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/aiogram-prometheus)](https://gitlab.com/rocshers/python/aiogram-prometheus)

## Installation

`pip install aiogram-prometheus`

## Quick start

```python
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from decouple import config

from aiogram_prometheus import (
    DispatcherAiogramCollector,
    PrometheusMetricMessageMiddleware,
    PrometheusMetricStorageMixin,
    PrometheusPrometheusMetricRequestMiddleware,
    PushGatewayClient,
    StorageAiogramCollector,
)

logging.basicConfig(level='DEBUG')

logger = logging.getLogger(__name__)

bot = Bot('TOKEN')


# Metric requests
# which are made by the target bot
bot.session.middleware(PrometheusPrometheusMetricRequestMiddleware())

# Metric storage
# Change "MemoryStorage" to your storage
class _Storage(PrometheusMetricStorageMixin, MemoryStorage):
    pass

storage_collector = StorageAiogramCollector()
storage = _Storage(storage_collector)

dp = Dispatcher(storage=storage)

# Metric message
# which are processed by the dispatcher
dp.message.middleware(PrometheusMetricMessageMiddleware())


# Metric base info
DispatcherAiogramCollector(dp)


@dp.startup()
async def on_startup(bot: Bot):
    # Make connect to your `PUSHGATEWAY` server
    # For More: https://prometheus.io/docs/practices/pushing/
    client = PushGatewayClient('http://localhost:9091/', 'job-name')
    client.schedule_push()

@dp.message()
async def handle(message: Message) -> None:
    await message.reply('Ok')

asyncio.run(dp.start_polling(bot))

```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/aiogram-prometheus/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/aiogram-prometheus>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
