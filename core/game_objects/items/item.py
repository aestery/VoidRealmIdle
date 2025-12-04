import logging
from abc import ABC
from typing import Callable, Dict


class BaseItemIds:
    """Holds constant item IDs for reference."""
    WEAPON: int = 1000
    SHIELDS: int = 2000

class Item(ABC):
    """Base class for all items in the game."""
    _item_id: int  # ID within its group
    _group_id: int  # Base ID for the item group
    item_id: int  # Unique identifier for the item

class ErrorItem(Item):
    """A placeholder item for unregistered IDs."""
    _item_id: int = 0
    _group_id: int = 0
    item_id: int = _group_id + _item_id

class ItemRegistry:
    """Registry for all item classes, mapping item IDs to their classes."""
    logger = logging.getLogger(__name__)
    _items: Dict[int, Item] = {}

    @classmethod
    def register_item(cls, item_class: Callable[..., Item]) -> Callable[..., Item]:
        """Registers an item class in the item registry for databse id map."""
        cls._items[item_class.item_id] = item_class()
        return item_class
    
    @classmethod
    def get_item_class(cls, item_id: int) -> Item | ErrorItem:
        """Retrieve an item class by its ID."""
        if item_id not in cls._items:
            ItemRegistry.logger.error("Item ID %i not found in registry, returning ErrorItem", item_id)
            return ErrorItem()
        if isinstance(cls._items.get(item_id), Item) is False:
            ItemRegistry.logger.error("Item ID %i is not an Item instance, returning ErrorItem", item_id)
            return ErrorItem()
        return cls._items.get(item_id, ErrorItem())
    
    @classmethod
    def get_all_items(cls) -> Dict[int, Item]:
        """Return all registered items."""
        return cls._items