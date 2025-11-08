# Flight Search Sample Output

## Overview

`flight_results.json` is a saved payload produced by `scrape_flights` in `flight_search_automation.py`. It captures flight options for a Gauhati (GAU) to Delhi (DEL) search on 11 November 2025.

## Top-Level Fields

- `search_datetime_utc` _(str)_: ISO 8601 timestamp indicating when the scrape finished.
- `origin` _(str)_ / `destination` _(str)_: Echoed query parameters used for the search.
- `journey_date_utc` _(str)_: Travel date normalized to midnight UTC (`YYYY-MM-DDTHH:MM:SSZ`).
- `total_flights` _(int)_: Number of flight cards successfully parsed.
- `flights` _(list[dict])_: Collection of itinerary details.

## Flight Entry Schema

Each flight dictionary contains:

- `airline`: Marketing carrier name.
- `flight_number`: One or more flight numbers (comma-separated if multiple legs).
- `departure_time`: Scheduled departure local time (with `+1 day` if overnight).
- `arrival_time`: Scheduled arrival local time, including `+1 day` markers when applicable.
- `price`: Fare shown on the site, including currency symbol and thousand separators.

## Sample Record

```json
{
  "airline": "SpiceJet",
  "flight_number": "SG-3453,189",
  "departure_time": "10:10",
  "arrival_time": "22:00",
  "price": "₹ 6,042.00"
}
```

## Usage Tips

- Treat the JSON as a snapshot; rerunning the scraper will overwrite the file with fresh data.
- Prices are stored as strings to preserve formatting—convert to numeric values before calculations if needed.
- Times reflect what the site displays and may require timezone interpretation relative to origin/destination airports.
