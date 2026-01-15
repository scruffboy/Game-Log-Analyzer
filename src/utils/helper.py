from datetime import datetime


def grouping_sub_amount(items_str):
    """Formatting item data"""
    items_str = items_str.strip().rstrip(",")
    parts = items_str.split(", ")
    items_list = []

    for i in range(0, len(parts), 2):
        if parts[i].isdigit() and parts[i + 1].isdigit():
            part = (int(parts[i]), int(parts[i + 1]))
            items_list.append(part)

    return items_list


def rework_datetime(timestamp: str):
    """Formatting a timestamp"""
    try:
        timestamp = timestamp.strip()
        dt = datetime.fromtimestamp(int(timestamp))
        return dt
    except (ValueError, TypeError):
        print(f"Time conversion error: {timestamp}")
        dt = datetime.now()
        return dt


def write_logs(sorted_logs):
    """Writing logs to combined.txt"""
    with open("src/logs/combined_log.txt", "w") as file:
        for log in sorted_logs:
            if log[1] == 0:
                item_str = " ".join(
                    "(%s, %s)" % (item, amount) for item, amount in log[4]
                )
                line = "%s %s | %s %s\n" % (log[0], log[3], log[2], item_str)
            else:
                line = "%s %s | %s | %s | %s\n" % (
                    log[0],
                    log[3],
                    log[2],
                    log[4],
                    log[5],
                )

            file.write(line)

        print("Success! Logs written.")


def answers_write_output(
    player_dict, item_stats, item_first_seen, item_last_seen, all_time_ordered
):
    """Function for write answers to output.txt"""
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


def combine_and_sort_logs(invent_entries, money_entries):
    """Combine two lists of LogEntry and sort them by timestamp."""
    combined = invent_entries + money_entries
    combined.sort(key=lambda x: x.timestamp)

    return combined
