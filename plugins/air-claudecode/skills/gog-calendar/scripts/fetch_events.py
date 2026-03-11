#!/usr/bin/env python3
"""Fetch calendar events from two gogcli accounts in parallel.

Usage:
    fetch_events.py <personal_account> <work_account> <from> <to> [extra_calendar_ids...]

Arguments:
    personal_account    Personal account email or alias
    work_account        Work account email or alias
    from                Start time (YYYY-MM-DD or RFC3339)
    to                  End time (YYYY-MM-DD or RFC3339)
    extra_calendar_ids  Optional additional calendar IDs (account:calendarId format)

Examples:
    fetch_events.py personal work 2026-02-20 2026-02-20
    fetch_events.py me@gmail.com work@company.com 2026-02-18 2026-02-22
    fetch_events.py personal work 2026-02-19 2026-02-19 work:c_188fhn2tujvjeirdhvhrfi68mie3k@resource.calendar.google.com
"""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor


def fetch_events(account: str, time_from: str, time_to: str, calendar_id: str = "") -> str:
    """Run gogcli events list for a single account/calendar and return stdout."""
    cmd = ["gog", "calendar", "events"]
    if calendar_id:
        cmd.append(calendar_id)
    cmd.extend([
        "--account", account,
        "--from", time_from,
        "--to", time_to,
        "--max", "50",
        "--json",
    ])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def main() -> None:
    if len(sys.argv) < 5:
        print(
            "Usage: fetch_events.py <personal_account> <work_account> <from> <to> [extra_calendar_ids...]",
            file=sys.stderr,
        )
        sys.exit(1)

    account_personal = sys.argv[1]
    account_work = sys.argv[2]
    time_from = sys.argv[3]
    time_to = sys.argv[4]
    extra_calendars = sys.argv[5:]

    account_map = {"personal": account_personal, "work": account_work}
    futures = []

    with ThreadPoolExecutor() as executor:
        future_personal = executor.submit(fetch_events, account_personal, time_from, time_to)
        future_work = executor.submit(fetch_events, account_work, time_from, time_to)

        extra_futures = []
        for extra in extra_calendars:
            if ":" not in extra:
                print(f"Warning: skipping invalid extra calendar '{extra}' (expected account:calendarId)", file=sys.stderr)
                continue
            acct_key, cal_id = extra.split(":", 1)
            account = account_map.get(acct_key, acct_key)
            extra_futures.append((cal_id, executor.submit(fetch_events, account, time_from, time_to, cal_id)))

        print("===PERSONAL===")
        print(future_personal.result())
        print("===WORK===")
        print(future_work.result())

        for cal_id, future in extra_futures:
            print(f"===EXTRA:{cal_id}===")
            print(future.result())


if __name__ == "__main__":
    main()
