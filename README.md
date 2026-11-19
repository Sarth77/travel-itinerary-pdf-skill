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
- Python 3.9+, `jq`, `curl` (macOS: `brew install python jq`). The skill builds its own virtualenv with
  `pymupdf`, `playwright`, `pillow` and Chromium via `scripts/preflight.sh <work_dir> --fix`.
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
$SK/scripts/preflight.sh /tmp/trip --fix
/tmp/trip/venv/bin/python -I $SK/scripts/fetch_commons.py /tmp/trip/img $SK/templates/commons_queries_example.json
/tmp/trip/venv/bin/python $SK/scripts/build.py $SK/templates/trips_example.py /tmp/trip/img /tmp/trip/out
```
Images the sample references but that you haven't downloaded will show as blank boxes; the skill fills them during
a real run.

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
