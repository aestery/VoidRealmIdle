import logging
from bot.handlers.base_handler import BaseHandler
from core.game_objects.player import Player


class VoidHandler(BaseHandler):
    def __init__(self, pool):
        super().__init__()
        self.player: Player = Player()
        self.logger = logging.getLogger(__name__)