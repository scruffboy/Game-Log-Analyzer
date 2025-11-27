# Import libraries

import datetime
import re
from pathlib import Path


# Import modules

from src.modules import generate_sample_logs


# Class for Players:


class Player(object):
    """Class for saving status of player"""

    def __init__(self, player_id):

        self.player_id = player_id
        self.money = 0
        self.inventory = {}
        self.first_seen = None
        self.last_seen = None

    def add_money(self, amount):  # Function for add money
        self.money += amount

    def remove_money(self, amount):  # Function for remove money
        self.money -= amount

    def add_item(self, item_id, amount):  # Function for add item
        current = self.inventory.get(item_id, 0)
        self.inventory[item_id] = current + amount

    def remove_item(self, item_id, amount):  # Function for remove item
        current = self.inventory.get(item_id, 0)
        self.inventory[item_id] = max(0, current - amount)

    def update_dates(self, timestamp):  # Function for update date
        if self.first_seen is None:
            self.first_seen = timestamp
        self.last_seen = timestamp


# Funtions for logic of program:


def rework_datetime(
    invent_massive, money_massive
):  # Function for formatting a timestamp

    # Formatted massives
    invent_formatted = []
    money_formatted = []

    # For invent_massive
    for item in invent_massive:
        timestamp = item[0]
        dt = datetime.datetime.fromtimestamp(int(timestamp))
        formatted = dt.strftime("[%y-%m-%d %H:%M:%S]")
        invent_formatted.append((formatted,) + item[1:])

    # For money_massive
    for item in money_massive:
        timestamp = item[0]
        dt = datetime.datetime.fromtimestamp(int(timestamp))
        formatted = dt.strftime("[%y-%m-%d %H:%M:%S]")
        money_formatted.append((formatted,) + item[1:])

    return invent_formatted, money_formatted


def grouping_sub_amount(items_str):  # Function for grouping items

    items_str = items_str.strip().rstrip(",")

    parts = items_str.split(", ")

    # Formatted massive
    items_list = []

    for i in range(0, len(parts), 2):
        if parts[i].isdigit() and parts[i + 1].isdigit():
            part = (int(parts[i]), int(parts[i + 1]))

            items_list.append(part)

    return items_list


def parsing_files():  # Function for parse of files

    # Path for files
    INVENT_PATH = Path("src/logs/inventory_logs.txt")
    MONEY_PATH = Path("src/logs/money_logs.txt")

    # Patterns for search data
    pattern_invent = r"\[(\d+)\] (\w+) \| (\d+), \((.+?)\)"
    pattern_money = r"(\d+)\|(\d+)\|([^,]+),(-?\d+),(.+)"

    # Massives with data
    invent_massive = []
    money_massive = []

    # Parse for Invent_file
    with INVENT_PATH.open("r") as f:
        for line in f:
            line = line.strip()
            match = re.search(pattern_invent, line)

            if match:
                timestamp = match.group(1)
                identification = 0
                action_type = match.group(2)
                player_id = match.group(3)
                items_str = match.group(4)

                items_form = grouping_sub_amount(items_str)

                invent_massive.append(
                    (timestamp, identification, action_type, player_id, items_form)
                )

    # Parse for Money_file
    with MONEY_PATH.open("r") as f:
        for line in f:
            line = line.strip()
            match = re.search(pattern_money, line)

            if match:
                timestamp = match.group(1)
                identification = 1
                action_type = match.group(3)
                player_id = match.group(2)
                amount = match.group(4)
                reason = match.group(5)

                money_massive.append(
                    (timestamp, identification, action_type, player_id, amount, reason)
                )

    invent_massive, money_massive = rework_datetime(invent_massive, money_massive)

    return invent_massive, money_massive


def combinate_sort_logs(
    invent_massive, money_massive
):  # Function for combinate and sort logs

    combined = invent_massive + money_massive

    sorted_combined = sorted(combined, key=lambda x: (x[0], x[1]))

    return sorted_combined


def write_logs(sorted_logs):  # Function for write logs to combined.txt

    with open("src/logs/combined_log.txt", "w") as file:
        for log in sorted_logs:
            if log[1] == 0:  # For inventory
                item_str = " ".join(
                    "(%s, %s)" % (item, amount) for item, amount in log[4]
                )
                line = "%s %s | %s %s\n" % (log[0], log[3], log[2], item_str)

            else:  # For money
                line = "%s %s | %s | %s | %s\n" % (
                    log[0],
                    log[3],
                    log[2],
                    log[4],
                    log[5],
                )

            file.write(line)

        print("Success! Logs written.")


def process_logs(sorted_logs):  # Function for get info from logs

    player_dict = {}  # Dictionary with players objects

    # Dicts for save info about items
    item_stats = {}  # For items
    item_first_seen = {}  # For first seen
    item_last_seen = {}  # For last seen
    all_time_ordered = []  # For all items in order of appearance

    for log in sorted_logs:  # Search logs
        player_id = log[3]

        try:
            if player_id not in player_dict:
                player_dict[player_id] = Player(player_id)

            player = player_dict[player_id]

            player.update_dates(log[0])

            if log[1] == 0:  # For item
                if log[2] == "ITEM_ADD":
                    for item_id, amount in log[4]:
                        player.add_item(item_id, amount)

                        # Update stats about items
                        if item_id not in item_stats:
                            item_stats[item_id] = 0
                        item_stats[item_id] += 1

                        if item_id not in item_first_seen:
                            item_first_seen[item_id] = log[0]
                        item_last_seen[item_id] = log[0]

                        all_time_ordered.append(item_id)

                elif log[2] == "ITEM_REMOVE":
                    for item_id, amount in log[4]:
                        player.remove_item(item_id, amount)

                        # Update stats about items
                        if item_id not in item_stats:
                            item_stats[item_id] = 0
                        item_stats[item_id] += 1

                        if item_id not in item_first_seen:
                            item_first_seen[item_id] = log[0]
                        item_last_seen[item_id] = log[0]

                        all_time_ordered.append(item_id)

            else:  # For money
                if log[2] == "MONEY_ADD":
                    player.add_money(int(log[4]))

                elif log[2] == "MONEY_REMOVE":
                    player.remove_money(int(log[4]))

        except Exception:
            print("Error!")

    return player_dict, item_stats, item_first_seen, item_last_seen, all_time_ordered


def answers_write_output(
    player_dict, item_stats, item_first_seen, item_last_seen, all_time_ordered
):  # Function for write answers to output.txt

    try:
        top10_items = sorted(item_stats, key=item_stats.get, reverse=True)[
            :10
        ]  # Top 10 items
        top10_players = sorted(
            player_dict.values(), key=lambda player: player.money, reverse=True
        )[
            :10
        ]  # Top 10 players
        first10_items = all_time_ordered[:10]  # 10 first items
        last10_items = all_time_ordered[-10:]  # 10 last items

    except Exception:
        print("Error!")

    try:
        with open("src/logs/output.txt", "w") as file:  # Write file
            file.write("Top 10 items:\n")  # For 10 items
            for item_id in top10_items:
                file.write("%s, %s\n" % (item_id, item_stats[item_id]))

            file.write("\n")  # For space

            file.write("Top 10 players:\n")  # For 10 players
            for player in top10_players:
                file.write(
                    "%s, %s, %s, %s\n"
                    % (
                        player.player_id,
                        player.money,
                        player.first_seen,
                        player.last_seen,
                    )
                )

            file.write("\n")  # For space

            file.write("First 10 items:\n")  # For 10 firts items
            for item in first10_items:
                file.write("%s, %s\n" % (item, item_first_seen[item]))

            file.write("\n")  # For space

            file.write("Last 10 items:\n")  # For 10 last items
            for item in last10_items:
                file.write("%s, %s\n" % (item, item_last_seen[item]))

    except Exception:
        print("Error!")


def interactive_mod(player_dict):  # Interactive mod

    while True:
        item_id_str = input("Enter ID_item or 'exit':")  # Enter ID item

        if item_id_str == "exit":  # Quit
            break

        try:
            item_id = int(item_id_str)
        except ValueError:
            print("Invalid item ID!")
            continue

        total_count = 0
        players_with_item = 0
        all_players = []

        for player in player_dict.values():  # Search info about item
            if item_id in player.inventory:
                count = player.inventory[item_id]
                total_count += count
                players_with_item += 1
                all_players.append((player.player_id, count))

        total10_players = sorted(all_players, key=lambda x: x[1], reverse=True)[:10]

        print("Item: %s" % item_id)
        print("Total count: %s" % total_count)
        print("Players with item: %s" % players_with_item)
        print("Top 10 players:")

        for (
            player_id,
            count,
        ) in total10_players:  # Print player -> player_id, item_count
            print("%s, %s" % (player_id, count))


def main():  # Main logic

    generate_sample_logs.generate_logs()  # Generate logs

    invent_logs, money_logs = parsing_files()  # Parsing files

    sorted_logs = combinate_sort_logs(invent_logs, money_logs)  # Sorting logs

    write_logs(sorted_logs)  # Record logs to combined.txt

    player_dict, item_stats, item_first_seen, item_last_seen, all_time_ordered = (
        process_logs(sorted_logs)
    )  # Search logs and get info about players

    answers_write_output(
        player_dict, item_stats, item_first_seen, item_last_seen, all_time_ordered
    )  # Write answers to output.txt

    interactive_mod(player_dict)  # Interactive mod for user


if __name__ == "__main__":

    main()
