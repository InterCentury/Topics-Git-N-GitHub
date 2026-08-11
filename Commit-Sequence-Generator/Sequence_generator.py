from pathlib import Path
from datetime import datetime, timedelta
import sys


# ============================================================
# COLORS
# ============================================================

RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"


# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = Path("Input.txt")
OUTPUT_FILE = Path("Output.txt")


# ============================================================
# UI HELPERS
# ============================================================

def clear_screen():
    print("\033[2J\033[H", end="")


def banner():
    print()
    print(f"{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}{BOLD}║              GIT SEQUENCE GENERATOR                ║{RESET}")
    print(f"{CYAN}{BOLD}╚══════════════════════════════════════════════════════╝{RESET}")
    print()


def section(title):
    print()
    print(f"{BLUE}{BOLD}┌─ {title}{RESET}")
    print(f"{BLUE}│{RESET}")


def success(text):
    print(f"{GREEN}✓{RESET} {text}")


def error(text):
    print(f"{RED}✗{RESET} {text}")


def info(text):
    print(f"{CYAN}ℹ{RESET} {text}")


def warning(text):
    print(f"{YELLOW}⚠{RESET} {text}")


def ask(label):
    return input(f"{MAGENTA}{BOLD}❯ {label}: {RESET}").strip()


# ============================================================
# INPUT FILE
# ============================================================

def load_files():
    if not INPUT_FILE.exists():
        error(f"{INPUT_FILE} was not found.")
        print()
        info(f"Create {INPUT_FILE} and put one relative file path per line.")
        sys.exit(1)

    files = []

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Ignore comments
            if line.startswith("#"):
                continue

            files.append(line)

    if not files:
        error(f"{INPUT_FILE} is empty.")
        sys.exit(1)

    return files


# ============================================================
# DATE PARSING
# ============================================================

def get_start_date():
    while True:
        value = ask("Start date (YYYY-MM-DD)")

        try:
            return datetime.strptime(value, "%Y-%m-%d").date()

        except ValueError:
            error("Invalid date.")
            info("Example: 2026-08-10")


def get_commits_per_day():
    while True:
        value = ask("Commits per day")

        try:
            number = int(value)

            if number <= 0:
                raise ValueError

            return number

        except ValueError:
            error("Enter a positive whole number.")


def get_skip_dates():
    print()
    print(
        f"{GRAY}"
        "Enter dates separated by commas.\n"
        "Example: 2026-08-15, 2026-08-20\n"
        "Press ENTER if you don't want to skip any dates."
        f"{RESET}"
    )

    value = ask("Skip dates")

    if not value:
        return set()

    skip_dates = set()

    for item in value.split(","):
        item = item.strip()

        if not item:
            continue

        try:
            date = datetime.strptime(item, "%Y-%m-%d").date()
            skip_dates.add(date)

        except ValueError:
            warning(f"Ignoring invalid date: {item}")

    return skip_dates


# ============================================================
# PATH QUOTING
# ============================================================

def quote_path(path):
    """
    Quote paths so spaces and special characters
    don't break the generated Git command.
    """

    path = path.replace('"', '\\"')
    return f'"{path}"'


# ============================================================
# COMMAND GENERATION
# ============================================================

def generate_commands(files, start_date, commits_per_day, skip_dates):

    output = []

    current_date = start_date
    commit_number = 0

    total_files = len(files)

    file_index = 0

    while file_index < total_files:

        # Skip requested dates
        if current_date in skip_dates:
            current_date += timedelta(days=1)
            continue

        for daily_index in range(commits_per_day):

            if file_index >= total_files:
                break

            relative_path = files[file_index]

            commit_number += 1

            # Give each commit a different time.
            # Starts around noon and increments by 2 minutes.
            hour = 12 + ((daily_index * 2) // 60)
            minute = (daily_index * 2) % 60

            commit_datetime = datetime.combine(
                current_date,
                datetime.min.time()
            ).replace(
                hour=min(hour, 23),
                minute=minute
            )

            timestamp = commit_datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            quoted_path = quote_path(relative_path)

            output.append(
                f"# Commit {commit_number}/{total_files}"
            )

            output.append(
                f'git add {quoted_path}'
            )

            output.append(
                f'git commit --date="{timestamp}" '
                f'-m "init + {relative_path}"'
            )

            output.append(
                "git push origin main"
            )

            output.append("")

            file_index += 1

        current_date += timedelta(days=1)

    return output, commit_number, current_date


# ============================================================
# WRITE OUTPUT
# ============================================================

def write_output(commands):
    with OUTPUT_FILE.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(commands))


# ============================================================
# MAIN
# ============================================================

def main():

    clear_screen()
    banner()

    section("Loading input")

    files = load_files()

    success(f"Loaded {BOLD}{len(files):,}{RESET} file paths")

    section("Configuration")

    start_date = get_start_date()
    commits_per_day = get_commits_per_day()
    skip_dates = get_skip_dates()

    section("Configuration summary")

    print(
        f"  {GRAY}Start date       {RESET}: "
        f"{CYAN}{start_date}{RESET}"
    )

    print(
        f"  {GRAY}Commits / day    {RESET}: "
        f"{CYAN}{commits_per_day}{RESET}"
    )

    print(
        f"  {GRAY}Files            {RESET}: "
        f"{CYAN}{len(files):,}{RESET}"
    )

    if skip_dates:
        print(
            f"  {GRAY}Skipped dates    {RESET}: "
            f"{YELLOW}{len(skip_dates)}{RESET}"
        )

        for date in sorted(skip_dates):
            print(f"                     {YELLOW}• {date}{RESET}")

    else:
        print(
            f"  {GRAY}Skipped dates    {RESET}: "
            f"{GREEN}None{RESET}"
        )

    section("Generating")

    print()

    commands, total_commits, end_date = generate_commands(
        files,
        start_date,
        commits_per_day,
        skip_dates
    )

    write_output(commands)

    success(f"Generated {BOLD}{total_commits:,}{RESET} commit sequences")
    success(f"Output written to {BOLD}{OUTPUT_FILE}{RESET}")

    print()

    print(f"{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}{BOLD}║                    COMPLETE                         ║{RESET}")
    print(f"{CYAN}{BOLD}╚══════════════════════════════════════════════════════╝{RESET}")

    print()

    print(
        f"  {GRAY}Input{RESET}      → "
        f"{WHITE}{INPUT_FILE}{RESET}"
    )

    print(
        f"  {GRAY}Output{RESET}     → "
        f"{GREEN}{OUTPUT_FILE}{RESET}"
    )

    print(
        f"  {GRAY}Total files{RESET} → "
        f"{CYAN}{len(files):,}{RESET}"
    )

    print()

    input(
        f"{GRAY}Press ENTER to exit...{RESET}"
    )


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
        warning("Cancelled by user.")
        sys.exit(0)

    except Exception as e:
        print()
        error(f"Unexpected error: {e}")
        sys.exit(1)