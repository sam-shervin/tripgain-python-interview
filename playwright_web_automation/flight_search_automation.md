# Flight Search Automation Script

## Overview

`flight_search_automation.py` automates a round-trip flight search on [budgetticket.in](https://www.budgetticket.in) using Playwright's asynchronous Chromium driver. The routine fills out the origin, destination, and journey date, triggers a search, and scrapes the resulting flight cards into structured JSON.

## Inputs

- **origin** (`str`): City or airport code entered into the origin field.
- **destination** (`str`): City or airport code entered into the destination field.
- **journey_date** (`str`): Travel date formatted as `YYYY-MM-DD` (local time). This is converted to UTC for the output metadata.

## Workflow

1. Launches a Chromium browser instance (non-headless by default with a small delay for stability).
2. Navigates to the home page and populates the origin and destination autocomplete inputs.
3. Opens the date picker, advances to the correct month/year, and selects the requested day.
4. Submits the search form and waits for results to load.
5. Scrolls through the results to ensure all flight cards are rendered.
6. Extracts airline, flight number, departure/arrival times, and price from each card.
7. Writes a summary JSON payload to `flight_results.json` and returns it to the caller.

## Output

- A dictionary containing:
  - `search_datetime_utc`: ISO 8601 timestamp for when the scrape ran.
  - `origin`, `destination`: Echoed search parameters.
  - `journey_date_utc`: Midnight UTC representation of the requested date.
  - `total_flights`: Number of result cards scraped.
  - `flights`: List of flight detail dictionaries.
- The same payload is persisted to `flight_results.json` in the working directory.

## Execution

Run directly for a quick scrape:

```bash
python flight_search_automation.py
```

The `__main__` block seeds a Bangalore → Delhi search on `2025-11-14`. Adjust the arguments in `asyncio.run(...)` or invoke `scrape_flights` from other code to customize the query.

## Notes

- Requires Playwright and its Chromium browser binaries, plus `aiofiles` for async file writes.
- `headless=False` keeps the browser visible; set to `True` for unattended runs.
- Basic retry/backoff isn’t implemented—intermittent UI or network failures will raise exceptions but are logged per card.
