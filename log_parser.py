import argparse
import os
import json
from collections import Counter


class LogParser:
    def __init__(self, file_path: str):
        """
        Initializes the parser with the path to the log file.

        Args:
            file_path (str): The path to the .jsonl log file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File doesn't exists {file_path}")

        self.file_path = file_path
        self.logs = self._load_logs()

    def _load_logs(self) -> list[dict]:
        """
        Loads and parses log entries from the file line by line.
        Skips any lines that are not valid JSON.

        Returns:
            list[dict]: A list of parsed log entries (dictionaries).
        """
        parsed_logs = []
        with open(self.file_path, "r") as file:
            for i, line in enumerate(file, 1):
                try:
                    if not line.strip():
                        continue
                    parsed_logs.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Warning: Skipping malformed JSON on line {i}")
        return parsed_logs

    def display_summary(self):
        """
        Calculates and displays a summary of log entries by their level.
        """
        if not self.logs:
            print("No valid log entries found.")
            return

        level_counts = Counter(log.get("level", "UNKNOWN") for log in self.logs)

        print(f"\n📊 Log Level Summary for '{os.path.basename(self.file_path)}'")
        print("━" * 50)

        total_logs = 0
        # Print each level's count, sorted for consistency
        for level, count in sorted(level_counts.items()):
            print(f"{level:<10}: {count}")
            total_logs += count

        print("━" * 50)
        print(f"{'Total':<10}: {total_logs}\n")


def main():
    """
    Main function to parse command-line arguments and run the log parser.
    """
    parser = argparse.ArgumentParser(
        description="A tool to parse and analyze JSON log files (.jsonl)."
    )
    parser.add_argument("filename", help="The path to the .jsonl log file.")

    # --- Arguments for future phases will go here ---

    args = parser.parse_args()

    try:
        parser = LogParser(file_path=args.filename)
        # For Phase 1, we only display the summary
        parser.display_summary()

    except FileNotFoundError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
