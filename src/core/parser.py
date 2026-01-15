import re
from typing import List
from utils.helper import grouping_sub_amount
from utils.helper import rework_datetime
from core.models import LogEntry


def parsing_inventory_lines(lines: List[str]):
    """Create LogEntry list from inventory lines"""
    entries = []
    pattern_inventory = r"\[(\d+)\] (\w+) \| (\d+), \((.+?)\)"

    for line in lines:
        line = line.strip()
        match = re.search(pattern_inventory, line)
        if match:
            entry = LogEntry(
                timestamp=rework_datetime(match.group(1)),
                identification=False,  # It's inventory
                action=str(match.group(2)),
                player_id=str(match.group(3)),
                data=grouping_sub_amount(match.group(4)),
            )

            entries.append(entry)

    return entries


def parsing_money_lines(lines: List[str]):
    """Create LogEntry list from money logs"""
    entries = []
    pattern_money = r"(\d+)\|(\d+)\|([^,]+),(-?\d+),(.+)"

    for line in lines:
        line = line.strip()
        match = re.search(pattern_money, line)
        if match:
            entry = LogEntry(
                timestamp=rework_datetime(match.group(1)),
                identification=True,  # It's money
                action=str(match.group(3)),
                player_id=str(match.group(2)),
                data=match.group(4),
            )

            entries.append(entry)

    return entries
