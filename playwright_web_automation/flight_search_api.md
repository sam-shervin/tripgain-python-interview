# Flight Search API Service

## Overview

`flight_search_api.py` wraps the scraping routine in a FastAPI application, exposing an HTTP endpoint that returns live flight search results as JSON. It imports `scrape_flights` from `flight_search_automation.py` and delegates the browser automation to that module.

## Endpoint

- **Method**: `GET`
- **Path**: `/flight-search`
- **Query Parameters**:
  - `origin` _(required)_: Origin city or airport code.
  - `destination` _(required)_: Destination city or airport code.
  - `journey_date` _(required)_: Travel date in `YYYY-MM-DD` format.
- **Response**: JSON payload identical to the structure returned by `scrape_flights`, including metadata, flight count, and a list of itineraries.

## Running Locally

Start the API with Uvicorn:

```bash
uvicorn flight_search_api:app --host 0.0.0.0 --port 8000 --reload
```

Then request results, for example:

```bash
curl "http://localhost:8000/flight-search?origin=BLR&destination=DEL&journey_date=2025-11-14"
```

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- Playwright stack (`playwright`, `aiofiles`) via the scraper module.

Ensure the Playwright browser binaries are installed (`playwright install`) before running the API, since each request launches Chromium.

## Notes

- The endpoint is fully asynchronous; concurrent requests await the underlying scrape routine sequentially per invocation.
- Consider adding caching or background job orchestration for production usage to avoid repeated browser launches.
