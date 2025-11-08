# flight_search_api.py
import asyncio
from fastapi import FastAPI, Query
from flight_search_automation import scrape_flights

app = FastAPI()

@app.get("/flight-search")
async def flight_search(
    origin: str = Query(...),
    destination: str = Query(...),
    journey_date: str = Query(...)    # format: YYYY-MM-DD
):
    data = await scrape_flights(origin, destination, journey_date)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "flight_search_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
