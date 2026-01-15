from models import Player


def process_logs(sorted_logs):
    """Processing and analysis of logs"""
    player_dict = {}  # Dictionary with players objects

    # Dicts for save info about items
    item_stats = {}
    item_first_seen = {}
    item_last_seen = {}
    all_time_ordered = []

    for log in sorted_logs:
        player_id = log[3]

        try:
            if player_id not in player_dict:
                player_dict[player_id] = Player(player_id)

            player = player_dict[player_id]
            player.update_dates(log[0])

            if log[1] == 0:
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
            else:
                if log[2] == "MONEY_ADD":
                    player.add_money(int(log[4]))
                elif log[2] == "MONEY_REMOVE":
                    player.remove_money(int(log[4]))
        except Exception:
            print("Error!")

    return player_dict, item_stats, item_first_seen, item_last_seen, all_time_ordered
