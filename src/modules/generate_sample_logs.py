# Import libraries

import random
import time


# Funtion


def generate_logs():  # Function for generate sample logs

    with open("src/logs/inventory_logs.txt", "w") as f:  # For inventory logs
        for i in range(1000):
            timestamp = int(time.time()) - random.randint(0, 86400 * 30)
            player_id = random.randint(1, 100)
            action = random.choice(["ITEM_ADD", "ITEM_REMOVE"])
            items = "".join(
                [
                    f"({random.randint(1, 100)}, {random.randint(1, 5)})"
                    for _ in range(random.randint(1, 3))
                ]
            )
            f.write(f"[{timestamp}] {action} | {player_id}, {items}\n")

    with open("src/logs/money_logs.txt", "w") as f:  # For money logs
        for i in range(1000):
            timestamp = int(time.time()) - random.randint(0, 86400 * 30)
            player_id = random.randint(1, 100)
            action = random.choice(["MONEY_ADD", "MONEY_REMOVE"])
            count = random.randint(1, 10000)

            if action == "MONEY_ADD":
                reason = random.choice(["monster_drop", "daily_reward", "quest_reward"])

            else:
                reason = random.choice(["shop_purchase", "craft_cost"])

            f.write(f"{timestamp}|{player_id}|{action},{count},{reason}\n")
