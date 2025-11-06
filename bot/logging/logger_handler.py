import logging
from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Any, Callable, Dict, Coroutine


class LoggingMiddleware(BaseMiddleware):
    """Logs incoming aiogram updates."""

    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.logger = logger

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Coroutine[Any, Any, Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        self.logger.info(
            f"{data['event_router']} started process",
        )
        return await handler(event, data)