from core.game_objects.items.item import Item, ItemRegistry, BaseItemIds

class Weapon(Item):
    """Base class for all weapon items."""
    _item_id = 0  # To be defined in subclasses
    _group_id = BaseItemIds.WEAPON
    item_id = _group_id + _item_id

@ItemRegistry.register_item
class DummySword(Weapon):
    """A basic sword item."""
    _item_id: int = 1   

    def __init__(self):
        super().__init__()
        self.name = "Dummy Sword"
        self.damage = 10
        self.description = "A simple sword for training purposes."
