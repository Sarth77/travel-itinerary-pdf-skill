---
name: travel-itinerary-pdf
description: Build polished, MakeMyTrip-quote-style travel itinerary PDFs (cover, itinerary summary, live flight options, day-wise plan with hotel cards and destination photos, itemised cost breakdown vs budget, important info, how to book). Use whenever the user asks for a trip plan, holiday itinerary, travel package, honeymoon/couple/family trip, "MMT-style" or "MakeMyTrip-style" PDF, or wants live flight + hotel prices and a day-by-day plan for a destination, including offbeat alternatives.
---

# Travel Itinerary PDF (MMT-style)

Produces one A4 PDF per destination in the user's preferred house style: the layout of a MakeMyTrip holiday quote
(blue section titles, light-blue cards, salmon city headers, timeline of day items, grey inclusion boxes),
filled with **live** flight fares and hotel rates plus real photos. See `reference/mmt_reference_pages.png`
(the user's original reference) and `reference/output_example_sikkim.png` (approved output).

## Style rules
- Live prices only for flights and hotels, captured "today"; label the capture date in the PDF. Everything else
  (cabs, jeeps, entry fees, meals) is shown as an **Estimate** with its basis.
- Always an itemised cost table for the whole party and a budget meter against the user's range.
- **Be honest about budget**: if a destination can't fit, say so on the cover pill and in the Budget Check, give the
  lean levers with rupee savings, and offer alternatives that do fit.
- When asked for alternatives, recommend 1–2 **less-crowded / offbeat** places that fit the same dates, origin airport
  and budget, and build a full PDF for each with the same detail.
- Real photos: hotel photos from the property's Booking.com listing; destination photos from Wikimedia Commons with
  credits on the last page. Never use stock images unrelated to the place; drop a photo rather than mislabel it.
- No MakeMyTrip logo, name or fake "travel expert": brand mark is the neutral "HolidayPlan"; disclaimer says it is an
  independent itinerary in a holiday-quote layout. Keep the cover "Prepared for" generic unless the user gives a name.
- Deliver PDFs into the session's working folder with descriptive names, e.g.
  `Sikkim_Couples_Itinerary_21-27Nov2026.pdf`, then send them with SendUserFile (display: attach).

## Workflow

### 0. Setup & preflight (once per session, before the intake questions finish)
Run the checks silently while asking the intake questions; only bother the user when something can't be fixed
automatically.

**A. Local toolchain (auto-fix, no permission needed: everything installs inside the scratch work folder)**
```bash
SK=~/.claude/skills/travel-itinerary-pdf
WORK=<temp dir>/trip                   # never inside the skill folder
mkdir -p $WORK/img
$SK/scripts/preflight.sh $WORK --fix   # builds $WORK/venv (pymupdf, playwright, pillow) + Chromium, checks network
```
Read each `MISSING`/`FAIL` line; its text after `::` is the fix.
- `python3` / `jq` / `curl` missing: these are system installs. Ask once with AskUserQuestion ("Install jq with
  Homebrew?" → "Yes, install it" / "I'll do it myself"), then run `brew install <pkg>` (macOS) or give the apt command.
  If Homebrew itself is missing, don't install it: give the user the official one-line command from brew.sh.
- `reach … no connection`: say which part will be missing (photos, fonts, fares), and continue with what works.
- If the user attaches a reference PDF, render it with PyMuPDF (`page.get_pixmap(dpi=60)`); `pdftoppm` is usually absent.

**B. Data tools (MCP connectors): check, then fall back**
Load and probe in one ToolSearch call: `select:mcp__skyscanner__search_flights,mcp__skyscanner__search_airports`, and
look for the Firecrawl tools (`firecrawl_search`, `alexandria_library_read`, `firecrawl_scrape`; their server prefix
is a UUID, so search `+firecrawl alexandria`). They are usually **claude.ai connectors** rather than local servers.
Then call `mcp__ccd_connectors__session_connectors_status` (load via ToolSearch) to see each connector's status:
- `connected` → use it.
- `disabled` → `set_session_connector_enabled`; `failed` → `reconnect_session_connector` (takes effect at end of turn).
- `needs_auth` → only the user can sign in: tell them to type `/mcp` in the session and sign in there (or in
  claude.ai → Settings → Connectors); pass the server UUID to `mcp__mcp-registry__suggest_connectors` to show a button.
- **not listed at all** → it was removed: search the registry
  (`search_mcp_registry` with "flights") and offer it via `suggest_connectors`, and use the browser fallback meanwhile.

| Need | Primary | If missing / disconnected | Last-resort fallback |
|---|---|---|---|
| Live flights | Skyscanner connector | `mcp__ccd_connectors__session_connectors_status` → `set_session_connector_enabled` or `reconnect_session_connector`; if it's not installed, `mcp__mcp-registry__suggest_connectors` / `search_mcp_registry` ("flights", "skyscanner") and show the result so the user can add it at claude.ai → Settings → Connectors | Built-in browser (`mcp__Claude_Browser__*`) on skyscanner.co.in or Google Flights, read with `get_page_text` |
| Live hotels + photos | Firecrawl connector → Alexandria `booking-com` | Same connector steps; or a **local** Firecrawl MCP (needs a Firecrawl API key, see C). A local server gives search/scrape of Booking.com pages; the structured `booking-com` provider may exist only on the connector | Built-in browser on booking.com search results for the dates; photos from the property page |
| Web lookups (taxi rates etc.) | `firecrawl_search` | `WebSearch` / `WebFetch` (load via ToolSearch) | Built-in browser |
| Destination photos | `fetch_commons.py` (no key needed) | — | Skip a photo rather than use a wrong one |

Ask before enabling/reconnecting a connector or adding an MCP server (it's a persistent config change):
one AskUserQuestion, e.g. "Skyscanner isn't connected. Reconnect it now?" → "Reconnect (Recommended)" /
"Use browser instead". If the user declines, use the fallback and say in the final reply which prices came from it.

**C. API keys (only when a local server needs one)**
- Never ask the user to paste a key into chat, never type or echo a key, never write it into the skill or a PDF.
- Give the user the command to run themselves in their own terminal, with a placeholder, e.g. a local Firecrawl MCP:
  ```bash
  claude mcp add firecrawl -s user -e FIRECRAWL_API_KEY=YOUR_KEY_HERE -- npx -y firecrawl-mcp
  ```
  Key from firecrawl.dev → dashboard → API keys. After they say done, ask them to restart the session (new MCP servers
  load at session start) or continue with the fallback for now.
- Keys are optional for this skill: with no connectors at all, everything still works through the built-in browser
  plus `fetch_commons.py`, just slower.

**D. Record what you used**: note in the final reply which source each price came from (connector, local MCP or
browser) and anything that could not be checked.

### 1. Intake: one question at a time, in the input box (mandatory)
Do not search flights or hotels until the required answers are known.

**Hard rules for asking (a written questionnaire in chat is not acceptable):**
- Ask with the `AskUserQuestion` tool **only**, **one question per call**, and wait for the answer before the next.
  Never print the question list in chat, never put two questions in one call, never batch.
- Write nothing in chat before or between questions except at most one short line ("Let's plan your trip.").
- Every question has 2–4 clickable options (best guess first, marked "(Recommended)" where sensible). The tool
  always adds an "Other" text field: that field is how the user types free answers (names, exact dates, a place).
  Say so in the question when typing is expected: "…or type it in Other".
- Each `header` is ≤12 characters. Each question must make sense on its own (the user sees only the dialog).
- Skip any question the user's message or memory already answers; for remembered defaults ask a confirm question
  ("Flying from Delhi (DEL) again?" → "Yes, Delhi (DEL)" / "Different city").
- Option labels are short (1–5 words); put detail in the option description.
- After the last question, show a one-line summary in chat and start the research (no extra "shall I proceed?").

**Question sequence (one call each; follow-ups only when the answer needs them):**

| # | header | question | options (Other = type) |
|---|---|---|---|
| 1 | Travellers | Who is travelling? | 2 adults (couple) • 1 adult (solo) • Family with kids • Group of friends |
| 1a | Group size | *(only if family/group)* How many adults and children, with each child's age? Type it in Other, e.g. "2 adults, kids 6 & 9". | 2 adults + 1 child • 2 adults + 2 children • 4 adults |
| 2 | Names | Names to print on the PDF cover? Type them in Other, e.g. "Aarav & Meera". | Skip, keep it generic • *(if remembered)* Same as last trip: … |
| 3 | Destination | Where do you want to go? Type a place in Other, or pick a vibe and I'll suggest. | Suggest: mountains/snow • Suggest: beach • Suggest: offbeat & quiet • Suggest: culture/heritage |
| 3a | Pick place | *(only if a vibe was chosen)* Which destination? Run a quick live-fare check first; put the round-trip fare and a one-line reason in each option's description. | 3 suggested places |
| 4 | From | Which city or airport are you flying from? | Delhi (DEL) • Mumbai (BOM) • Bengaluru (BLR) • *(remembered city first)* |
| 5 | Start date | When do you want to leave? Type an exact date in Other, e.g. "21 Nov". | 2–3 concrete dates computed from today (e.g. "Fri 4 Dec"), plus "Flexible this month" |
| 6 | Length | How long is the trip? | 3N / 4D • 4N / 5D • 5N / 6D • 6N / 7D |
| 7 | Budget | Total budget for everyone, including flights? Type your own range in Other. | 4 ranges scaled to party size and distance (e.g. "₹40–50k", "₹50–70k", "₹70k–1L", "₹1L+") |
| 8 | Preferences | Use recommended preferences, or customise them? | Use recommended (Recommended): description lists the defaults • Customise |

If **Customise**, continue one call each: 8a Trip type (couple, honeymoon, family, friends) → 8b Stay (homestay,
3★ rated 8.5+, 4★, resort) → 8c Food (veg, non-veg, Jain; meals in budget?) → 8d Pace (relaxed, balanced, packed)
→ 8e Flights (non-stop only, morning, evening, any) → 8f Occasion/needs (none, anniversary, elderly, infant) →
8g Alternatives (1 quieter option, 2, none). Rooms default to 1 per 2 adults; ask only for odd numbers or groups.

Recommended defaults: couple theme, 1 room per 2 adults, 3★ or homestay rated 8.5+ with private bathroom,
veg-friendly meals in budget, balanced pace, non-stop flights at sensible times, 1 quieter alternative.

### 1b. Brief
From the answers, fix: origin airport, dates, nights, travellers, rooms, total budget range, theme, destination(s).
Put names in `META["names"]` (list) and the party label in `META["pax"]` (e.g. "2 Adults", "2 Adults + 1 Child").
Compute weekdays for each date. Pick sensible city splits (2–3 bases for 6 nights; avoid >5 h drives on arrival day).
Check that check-in windows fit arrival times; add a host note when they don't.

### 2. Live flights (round trip, all travellers)
- Preferred (if step 0B found it): Skyscanner MCP `mcp__skyscanner__search_flights` with `origin_airport_code`, `destination_airport_code`,
  `depart_date`, `return_date`, `adults`. Results are large and get saved to a file; summarise with
  `$SK/scripts/flights_summary.sh <saved.json> 14`. Prices returned are totals for all adults.
- Run all candidate airports in parallel (e.g. for Sikkim IXB; alternatives DHM, DED, GAU, PGH…). An `AirportNotFound`
  error means that airport isn't covered (e.g. PYG, KUU) — skip it.
- If the Skyscanner MCP is unavailable: use the built-in browser (`mcp__Claude_Browser__*`) on Skyscanner or Google
  Flights and read the page with `get_page_text`, or `firecrawl_scrape`. Record airline, flight number, times, stops
  and the exact total.
- Choose a **recommended** pair (sensible timings, non-stop) plus 3–5 alternatives (cheapest, same airline, earliest,
  lowest-fare 1-stop) for the options table. Flight fares decide which alternatives fit the budget — use them to
  shortlist offbeat destinations before researching hotels.

### 3. Live hotels (Booking.com via Firecrawl Alexandria)
Direct scraping of booking.com search pages returns nothing; use the structured provider:
```
mcp__<firecrawl-connector-id>__alexandria_library_read  calls=[
  {"provider":"booking-com","capability":"hotels/search","options":{
     "query":"Gangtok","country_code":"in","checkin":"2026-11-21","checkout":"2026-11-24",
     "adults":2,"currency":"INR","sort":"price","filters":"review_score=80","rows":20}}, ...one per stop ]
```
- Up to 10 calls per request. The result is retained in a workspace; read it with the `firecrawl` `bash` capability
  (`jq` over `response.json`, `.data.alexandria[i].data.results[]`). **Result order may not match call order** — check
  `resolved_name`/`nights` per index.
- Useful fields: `name, review_score, review_count, price_including_excluded_charges.amount` (stay total incl. taxes),
  `recommended_units[0].room_name`, `free_cancellation`, `no_prepayment`, `photo_url`, `page_name`, `hotel_id`.
- Reject dorm beds and shared-bathroom rooms for couples. Prefer score ≥ 8.5 with ≥ 15 reviews; offer one upgrade option.
- Details (check-in/out times, facilities, description): `{"provider":"booking-com","capability":"hotels/hotel",
  "options":{"country_code":"in","page_name":"<slug>","checkin":..,"checkout":..,"currency":"INR"}}`.
  Use `house_rules.checkin_from/checkin_until/checkout_until` and facilities for "Room Inclusions".
- A single property by URL: `hotels/search` with `"query":"https://www.booking.com/hotel/in/<slug>.html"`.
- Don't guess meal plans from `meal_plan_id`; say "Room only / as per rate" unless the description states it.
- Download photos: `$WORK/venv/bin/python -I $SK/scripts/fetch_hotel_photos.py $WORK/img key=<photo_url> ...`

### 4. Destination photos
Write `{key: "search text"}` JSON (see `templates/commons_queries_example.json`), then
`$WORK/venv/bin/python -I $SK/scripts/fetch_commons.py $WORK/img queries.json`. It skips files already present, backs
off on HTTP 429 and merges credits into `img/credits.json`. Re-run until complete. Then build a contact sheet with PIL
and **look at it** (if one file keeps returning 429 after re-runs, change its query or skip it): delete mismatches (wrong place/subject) and re-query or set that item's `img=None`.

### 5. Local costs
Quick `firecrawl_search` for current shared-cab / tour rates when unsure. Typical bases: shared jeeps/cabs per seat,
private sedan for transfers, one private car day for sightseeing, ₹1,000–1,100/day meals for two, small entry fees.
Prefer shared transport when the budget is tight; mention the private option and its price in the exclusions.

### 6. Write the trip data and build
Copy `templates/trips_example.py` to `$WORK/trips.py` and edit:
- `META`: capture date, prepared_for, pax, rooms, theme, origin, duration, date strings, budget_lo/hi, flight_source.
- One dict per destination in `TRIPS` (`SIKKIM` shows every field): `file`, `title`, `subtitle`, hero images,
  `blurb`, `highlights` (icons: hotel, walk, car, plane, snow, para, leaf, meal, pin, out), `cities` (name, nights),
  `weather`, `flights` (out/ret via `F(...)`, `price`, `airport`, `options`), `hotels`, `days` (items: `("flight",None)`,
  `("transfer",{...})`, `("hotel",key)`, `("checkout",text)`, `("activity",{...})`, `("note",(title,text))`),
  `costs` (category, details, amount, basis), `budget_note`, `info`, `credits_keys`.
- The cost total is computed from `costs`; the cover pill shows within / at top / above budget automatically.
```bash
$WORK/venv/bin/python $SK/scripts/build.py $WORK/trips.py $WORK/img "<working dir>"
```

### 7. Review (always)
Render every page with PyMuPDF at ~55 dpi into a 5-across contact sheet and look at it; zoom a day page and the last
page at ~110 dpi. Check: no orphaned day headers, photos match captions, totals match the table, credits readable,
no stray hard-coded dates. Fix and rebuild before sending.

### 8. Hand-off
Send PDFs with SendUserFile. In the reply give a table per destination (flights + price, stays, total), state plainly
which plans exceed the budget and why, list caveats (non-refundable rates, late check-in, optional extras not
included), and remind that nothing is booked and fares move.
