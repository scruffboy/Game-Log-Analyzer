from config import INVENTORY_LOGS, MONEY_LOGS
from core.parser import parsing_inventory_lines, parsing_money_lines
from core.database import save_logs_to_db
from utils.generate_sample_logs import generate_logs
from utils.helper import combine_and_sort_logs


def main():
    """Main programm logic"""
    # Generate test logs for example
    print("Generate test logs...")
    generate_logs()

    # Read content from log files and formatted in lines
    print("Read a files...")
    inventory_content = INVENTORY_LOGS.read_text().splitlines()
    money_content = MONEY_LOGS.read_text().splitlines()

    # Parsing lines and create LogEntry object
    print("Parsing files...")
    inventory_entries = parsing_inventory_lines(inventory_content)
    money_entries = parsing_money_lines(money_content)

    # Combine and sort entry logs
    all_logs = combine_and_sort_logs(inventory_entries, money_entries)

    # Write logs to database
    save_logs_to_db(all_logs)


if __name__ == "__main__":
    main()
