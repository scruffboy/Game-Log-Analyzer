from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple, Dict, Optional, Any


class Player:
    """Class for saving status of player"""

    def __init__(self, player_id: str):
        self.player_id = player_id
        self.money = 0
        self.inventory: Dict[int, int] = {}
        self.first_seen: datetime | None = None
        self.last_seen: datetime | None = None

    def add_money(self, amount: int):
        self.money += amount

    def remove_money(self, amount: int):
        self.money -= amount

    def add_item(self, item_id: int, amount: int):
        current = self.inventory.get(item_id, 0)
        self.inventory[item_id] = current + amount

    def remove_item(self, item_id: int, amount: int):
        current = self.inventory.get(item_id, 0)
        self.inventory[item_id] = max(0, current - amount)

    def update_dates(self, timestamp: datetime):
        if self.first_seen is None:
            self.first_seen = timestamp
        self.last_seen = timestamp


@dataclass
class LogEntry:
    """Class for saving log entries to an object"""

    timestamp: datetime
    identification: bool
    action: str
    player_id: str
    data: Any
