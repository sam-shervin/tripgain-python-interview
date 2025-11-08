# flight_search_automation.py
import asyncio
import json
import time
from datetime import datetime, timezone
from playwright.async_api import async_playwright
import aiofiles

async def scrape_flights(origin, destination, journey_date):
    # Parse journey_date → "YYYY-MM-DD"
    dt = datetime.strptime(journey_date, "%Y-%m-%d")
    day = dt.strftime("%d")
    month = dt.strftime("%B")
    year = dt.strftime("%Y")

    journey_date_utc = dt.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()

        await page.goto("https://www.budgetticket.in")

        # ---------------- ORIGIN ----------------
        origin_in = page.locator("input[placeholder='Select Origin City']").first
        await origin_in.click()
        await origin_in.fill("")
        await origin_in.type(origin)
        await asyncio.sleep(2)
        await page.keyboard.press("Enter")

        # -------------- DESTINATION --------------
        dest_in = page.locator("input[placeholder='Select Destination City']").first
        await dest_in.click()
        await dest_in.fill("")
        await dest_in.type(destination)
        await asyncio.sleep(2)
        await page.keyboard.press("Enter")

        # ------------------ DATE ------------------
        await page.locator("label.datepicker.search-date").first.click()
        await asyncio.sleep(1)

        calendar = page.locator("div.modalDatePicker").first

        async def get_visible_month_year():
            header = await calendar.locator("div#divFareCalendar0 #spnMonth").inner_text()
            m, y = header.split(" - ")
            return m.strip(), y.strip()

        visible_m, visible_y = await get_visible_month_year()

        while not (visible_m == month and visible_y == year):
            await calendar.locator("span.right").first.click()
            await asyncio.sleep(0.5)
            visible_m, visible_y = await get_visible_month_year()

        # ✅ Correct date click
        await calendar.locator(f"td.emp_Cells >> text='{day}'").first.click()

        await asyncio.sleep(1)

        # ----------------- SEARCH -----------------
        await page.locator("input[type='submit'][value='Search']").click()
        await asyncio.sleep(5)

        # ---- SCROLL TO LOAD ALL RESULTS ----
        prev_height = await page.evaluate("document.body.scrollHeight")
        while True:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1.5)
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height

        # ---------------- SCRAPE ------------------
        flights = []
        cards = await page.locator("div.search-card.card.mt-0.OnwardTripClear").all()

        for card in cards:
            try:
                airline = await card.locator("p.h6.responsive-bold.mb-0.ng-binding").first.text_content()
                flight_num = await card.locator("p.mb-0.d-inline.d-lg-block.ng-binding").first.text_content()

                dep_time = await card.locator(
                    "div.col-4.col-md-3.text-right.p-0 span.text-mild-dark.d-block.ng-binding.h4"
                ).first.text_content()

                arr_time = await card.locator(
                    "div.col-4.col-md-3.text-left.p-0 span.text-mild-dark.d-block.valign-wrapper.ng-binding.h4"
                ).first.text_content()

                price = await card.locator(
                    "div.col-2.col-md-2.p-0.valign-wrapper p.text-gray.roboto_font.mb-0.text-primary.ng-binding.ng-scope.h4"
                ).first.text_content()

                flights.append({
                    "airline": airline.strip(),
                    "flight_number": flight_num.strip(),
                    "departure_time": dep_time.strip(),
                    "arrival_time": arr_time.strip(),
                    "price": price.strip(),
                })
            except Exception as e:
                print(f"Error extracting flight data: {e}")
                continue

        # -------------- OUTPUT JSON --------------
        result = {
            "search_datetime_utc": datetime.now(timezone.utc).isoformat(),
            "origin": origin,
            "destination": destination,
            "journey_date_utc": journey_date_utc,
            "total_flights": len(flights),
            "flights": flights,
        }
        async with aiofiles.open("flight_results.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(result, indent=2, ensure_ascii=False))

        print(f"Total flights extracted: {len(flights)}")
        print("Saved to flight_results.json")

        await browser.close()
        return result


# Allow running the script manually
if __name__ == "__main__":
    asyncio.run(scrape_flights("Bangalore", "Delhi", "2025-11-14"))
