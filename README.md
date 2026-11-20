# Travel Itinerary PDF: a Claude Code skill

A [Claude Code](https://claude.com/claude-code) skill that plans a trip and delivers a polished, holiday-quote-style
**A4 PDF itinerary** with **live** flight fares, **live** hotel rates, real photos, a day-by-day plan and an itemised
budget. It can also suggest quieter alternative destinations, each with its own PDF.

![Cover preview](docs/preview-cover.png)

## What you get
- **Cover:** destination, dates, travellers (optional names), highlights, estimated total and a budget status badge.
- **Your Itinerary:** a city-by-city summary of every day.
- **Flight Details:** the recommended round trip plus 3–5 live alternatives, with the date prices were captured.
- **Day Wise Details:** flights, transfers, activities with photos, and hotel cards with room type, check-in/out
  times, rate, inclusions and cancellation policy.
- **Cost Breakdown:** an itemised table (live prices vs estimates), a budget meter, and an honest note when the plan
  goes over budget, with ways to save.
- **Important Information & How to Book:** permits, packing, policies, booking steps and photo credits.

## How it works
1. **Intake:** asks one question at a time (travellers, optional names, destination or "suggest", departure city,
   date, length, budget, preferences), skipping anything you already said.
2. **Preflight:** installs its PDF toolchain into a temp folder and checks the data connectors, falling back to the
   built-in browser when one is missing.
3. **Research:** live flights (Skyscanner connector, or the browser), live hotels and photos (Booking.com via the
   Firecrawl connector, or the browser), destination photos from Wikimedia Commons, and local taxi/tour rates.
4. **Build:** one Python script renders HTML into a PDF with headless Chromium.
5. **Review:** renders every page to images and checks them before handing over.

## Install
```bash
git clone https://github.com/Sarth77/travel-itinerary-pdf-skill.git
mkdir -p ~/.claude/skills
cp -R travel-itinerary-pdf-skill/travel-itinerary-pdf ~/.claude/skills/
```
Start a new Claude Code session, then type `/travel-itinerary-pdf`, or just ask "plan a trip to …".

### Requirements
- Python **3.12.13**, `jq`, `curl`. The Python version is pinned in `travel-itinerary-pdf/.python-version`;
  install it with `uv python install 3.12.13` if needed and set `PYTHON_BIN` to that interpreter. The skill builds its own virtualenv with
  exact versions of `pip`, `pymupdf`, `playwright`, `pillow` and their transitive dependencies, plus the
  Chromium revision selected by the pinned Playwright version via `scripts/preflight.sh <work_dir> --fix`.
- Optional connectors for faster live data: **Skyscanner** (flights) and **Firecrawl** (hotels and web search).
  Add them at claude.ai → Settings → Connectors. Without them the skill uses the built-in browser.
- No API key is required. If you run a *local* Firecrawl MCP server instead of the connector, add your own key in
  your terminal (never paste it into a chat):
  ```bash
  claude mcp add firecrawl -s user -e FIRECRAWL_API_KEY=YOUR_KEY_HERE -- npx -y firecrawl-mcp
  ```

## Repository layout
```
travel-itinerary-pdf/
  SKILL.md                      # the workflow Claude follows (intake, preflight, research, build, review)
  scripts/build.py              # trips.py + images → PDFs
  scripts/preflight.sh          # dependency / network check, --fix installs the venv + Chromium
  scripts/setup_env.sh          # venv bootstrap
  scripts/fetch_commons.py      # Wikimedia Commons photos + credits (handles rate limits)
  scripts/fetch_hotel_photos.py # hotel listing photos
  scripts/flights_summary.sh    # summarise a Skyscanner result file with jq
  templates/trips_example.py    # complete sample: 3 destinations, every field documented
  templates/commons_queries_example.json
```

## Try the builder directly
```bash
SK=travel-itinerary-pdf
PYTHON_BIN="$(uv python find 3.12.13)" $SK/scripts/preflight.sh /tmp/trip --fix
/tmp/trip/venv/bin/python -I $SK/scripts/fetch_commons.py /tmp/trip/img $SK/templates/commons_queries_example.json
/tmp/trip/venv/bin/python $SK/scripts/build.py $SK/templates/trips_example.py /tmp/trip/img /tmp/trip/out --allow-unverified
```
Images the sample references but that you haven't downloaded will show as blank boxes; the skill fills them during
a real run.

## Rate evidence and freshness
Normal builds reject missing, malformed, future-dated or older-than-24-hour evidence **before creating output**.
The builder validates researcher-supplied records; it does not call flight/hotel APIs or independently verify that
a source returned the quoted amount. The researcher must read the exact search/booking result for the itinerary,
including party size, all taxes, room and meal plan, then record the actual capture time and URL. A successful
preflight network check only proves connectivity, not access to live search results.

Set `META.departure_date` and `META.return_date` as ISO dates. Each hotel needs `checkin_date` and `checkout_date`.
Attach `rate` to the selected `flights` dictionary and each hotel. Append an evidence dictionary as the **sixth**
item of **every** flight option tuple; the first five items retain their original meaning.

Each evidence dictionary has this structure (values must come from actual research):
```python
{
    "source": "Booking.com",                  # provider actually used
    "url": "https://www.booking.com/hotel/in/property.html", # exact search/listing URL
    "captured_at": "2026-11-20T14:30:00+05:30", # actual capture, timezone required
    "currency": "INR",
    "amount": 3780,                           # total for the whole party/stay, including taxes
    "context": {                              # must exactly match the rendered selection
        "property": "Arcane Viewfinder Homestay",
        "checkin": "2026-11-21", "checkout": "2026-11-24",
        "travellers": "2 Adults", "rooms": "1 room", "room": "Queen Room x 1",
        "meal": "Room only (breakfast & packed lunch on request)", "taxes": "included",
    },
}
```
For flights, context keys are `origin`, `destination` (airport codes), `departure`, `return_date` (ISO dates),
`travellers` (exact `META.pax` label), `cabin` (`economy`), `taxes` (`included`), `onward`, `returning`.
For selected flights the last two values are the exact `out`/`ret` dictionaries; for an alternative they are its
onward/return display strings. `scripts/rates.py` provides `flight_context(meta, flights, option=None)` and
`hotel_context(meta, hotel)` to construct these contexts after checking the source. Separate quotes can have
separate URLs, providers and capture times; these appear next to each fare/rate in the PDF.

Cancellation terms are optional. Add `cancellation={"text": "...", "evidence": {...}}` to the selected flights
and/or hotel. Evidence uses the same fields and exact rate context as above and must be fresh. Flight text must
state the terms for both selected legs/fare families, including differences. Hotel text must state deadlines
with timezone, cancellation fees and prepayment terms where supplied by the source. Missing, stale or mismatched
policy evidence displays **Not verified for this fare/room rate; confirm ... at checkout**. Legacy `policy` prose
never counts as verification; alternatives do not inherit selected flight policy.

The shipped historical sample intentionally has no evidence. Only `--allow-unverified` permits it to render;
this mode prominently labels all prices **UNVERIFIED SAMPLE** on the cover, flight/hotel details and cost table.
It must not be used to present a current travel quote. No amounts or budget calculations change in either mode.

## Validation
```bash
/tmp/trip/venv/bin/python -m unittest discover -s tests -v
```
Tests exercise rate freshness/context checks, policy fallback, origins and totals, preflight failure statuses,
and Chromium PDF builds in sample and validated-fixture modes. Fixture prices are synthetic test inputs.
`preflight.sh` returns 0 only when every required check passes; any missing tool, dependency drift, failed setup,
failed browser launch or unreachable network endpoint returns nonzero. Fixes are checked again before success.
`requirements.in` lists direct pins and `requirements.txt` pins the full toolchain; update both deliberately.

## Privacy and safety
- Traveller names only appear in the PDF; they are never sent to search tools.
- The skill never asks for, types, or stores API keys or payment details, and it never books anything. Every price
  must be re-checked on the booking page.
- The sample data contains no personal information. Its prices are illustrative and were captured in Nov 2026.

## Disclaimer
Independent project, not affiliated with MakeMyTrip, Skyscanner, Booking.com or Firecrawl. The layout is inspired by
common holiday-quote documents; the generated PDFs carry a neutral "HolidayPlan" mark and a disclaimer.

**Preview photo credits (Wikimedia Commons):** "Kangchenjunga, India" by My Discovery (CC BY 2.0); "Changu (Tsomgo)
Lake" by Kuldeepburjbhalaike (CC BY-SA 4.0); "Rumtek Monastery 04" by Bernard Gagnon (CC BY-SA 4.0).

## License
Code and docs: [MIT](LICENSE). Photos keep their own licenses as credited.
