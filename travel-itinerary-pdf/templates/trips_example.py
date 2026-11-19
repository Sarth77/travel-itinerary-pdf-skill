# SAMPLE trip data (three example destinations). Fares/rates were captured live on 19 Nov 2026 (IST)
# and are illustrative only: re-capture live prices for every new trip.
# Flights: Skyscanner live search, 2 adults, economy, round trip DEL, 21 -> 27 Nov 2026.
# Hotels: Booking.com live search, 2 adults, 1 room; totals include taxes & fees shown by Booking.com.

CAPTURED = "19 Nov 2026"

# Trip-wide settings used by build.py. Edit these first for a new trip.
META = dict(
    captured=CAPTURED,                 # date live prices were captured
    names=[],                          # traveller names for the cover, e.g. ["Aarav", "Meera"]; empty = generic
    prepared_for="You & your partner",    # fallback cover label when names is empty
    pax="2 Adults", rooms="1 room",
    theme="Couples Choice",            # e.g. Couples Choice, Family Fun, Friends Getaway, Solo Escape
    origin_city="New Delhi", origin_short="Delhi", origin_code="DEL",
    duration="6N/7D",
    dates_short="21\u201327 Nov 2026",
    dates_long="Sat 21 Nov \u2013 Fri 27 Nov 2026",
    dates_search="21 \u2192 27 Nov 2026", dates_book="21\u201327 Nov",
    out_hdr="Sat 21 Nov", ret_hdr="Fri 27 Nov",
    budget_lo=40000, budget_hi=50000,  # total budget range for the whole party, INR
    flight_source="Skyscanner",
)

def F(code, num, airline, frm, dep, to, arr, dur, stops="Non-stop", via=None):
    return dict(code=code, num=num, airline=airline, frm=frm, dep=dep, to=to, arr=arr, dur=dur, stops=stops, via=via)

SIKKIM = dict(
    slug="Sikkim", file="Sikkim_Couples_Itinerary_21-27Nov2026.pdf",
    title="Sikkim", subtitle="3N Gangtok • 3N Pelling",
    hero="d_pelling.jpg", hero2="d_tsomgo.jpg", hero3="d_rumtek.jpg",
    blurb=("Plan the perfect late-autumn escape to Sikkim. Wake up to clear November views of Kanchenjunga, "
           "stand at the frozen-edged Tsomgo Lake at 12,300 ft, wander Gangtok's monasteries and MG Marg together, "
           "then slow down in Pelling's homestays with sunrise over the world's third-highest peak."),
    highlights=[("hotel","2 Homestays"),("walk","9 Sightseeing spots"),("car","6 Transfers"),("plane","Non-stop flights"),("snow","Tsomgo Lake permit tour")],
    cities=[("Gangtok",3),("Pelling",3)],
    weather="Gangtok 7–17°C • Pelling 6–15°C • Tsomgo Lake −2 to 8°C. Late November is dry with the clearest mountain views of the year.",
    flights=dict(
        out=F("QP","1807","Akasa Air","DEL","13:40","IXB","15:55","2h 15m"),
        ret=F("6E","5379","IndiGo","IXB","17:20","DEL","19:35","2h 15m"),
        out_date="Sat, 21 Nov 2026", ret_date="Fri, 27 Nov 2026",
        price=32679, airport="Bagdogra (IXB)",
        options=[
            ("★ Recommended", "Akasa QP 1807 • 13:40→15:55 • Non-stop", "IndiGo 6E 5379 • 17:20→19:35 • Non-stop", 32679, "Best timings: no 4 AM start on the last day"),
            ("Cheapest non-stop", "Akasa QP 1807 • 13:40→15:55 • Non-stop", "SpiceJet SG 904 • 08:50→11:10 • Non-stop", 32382, "Needs a night near Siliguri on 26 Nov"),
            ("Same airline", "Akasa QP 1807 • 13:40→15:55 • Non-stop", "Akasa QP 1808 • 16:35→19:10 • Non-stop", 33449, "One booking, one baggage policy"),
            ("Earliest arrival", "IndiGo 6E 601 • 13:30→15:15 • Non-stop", "SpiceJet SG 189 • 19:20→21:40 • Non-stop", 34174, "40 min earlier into Bagdogra"),
            ("Lowest fare", "IndiGo 6E 897 + 6E 6134 • 12:20→18:00 • 1 stop CCU (2h 20m)", "SpiceJet SG 904 • 08:50→11:10 • Non-stop", 30830, "Saves ₹1,849 but arrives after dark"),
        ]),
    hotels={
        "gangtok": dict(name="Arcane Viewfinder Homestay", type="Homestay", img="h_arcane.webp", score="9.7", word="Exceptional", reviews=75,
                        area="Gangtok", near="0.6 km from the town centre (MG Marg area)", cin="21 Nov, Sat • 11 AM–5 PM*", cout="24 Nov, Tue • by 11:30 AM",
                        room="Queen Room x 1", nights=3, price=3780, meal="Room only (breakfast & packed lunch on request)", bed="1 queen bed",
                        incl=["Private bathroom with hair dryer & toiletries","Free WiFi & free parking","Room service","Packed lunches for day trips (paid)","Airport / car rental desk (paid)"],
                        policy="Non-refundable rate as listed on Booking.com", note="*You land at ~9 PM: message the host your arrival time after booking."),
        "pelling": dict(name="Mandavya Homestay", type="Homestay", img="h_mandavya.webp", score="8.8", word="Excellent", reviews=71,
                        area="Pelling", near="1.1 km from Upper Pelling, on the Pelling–Gyalshing road", cin="24 Nov, Tue • from 12:30 PM", cout="27 Nov, Fri • by 11 AM",
                        room="Standard Double Room x 1", nights=3, price=6559, meal="Room only (à la carte breakfast available)", bed="1 double bed",
                        incl=["Garden & terrace with sun deck","Outdoor fireplace / bonfire area","Flat-screen TV, private bathroom with bath","Free WiFi & free parking","Mini-market on site"],
                        policy="Non-refundable rate as listed on Booking.com", note="Upgrade option: The Nettle & Fern Farmstay, Superior King (9.1/10, 148 reviews) – ₹10,185 for 3 nights, free cancellation."),
    },
    days=[
        dict(date="Sat, 21 Nov 2026", city="Gangtok", items=[
            ("flight", None),
            ("transfer", dict(title="Bagdogra Airport → Gangtok", dur="4–4.5 Hours", kind="Shared Airport Cab", img="d_teesta.jpg",
                text="Pre-book a shared airport shuttle (e.g. Wizzride/Sikkim-registered operators) timed to your 15:55 landing. The road follows the Teesta River through Sevoke, Melli and Rangpo (Sikkim check-post: carry a photo ID) to Gangtok, arriving around 8:30–9 PM.",
                incl=["✔ Two seats in a shared cab, airport to Gangtok", "✔ Luggage on roof carrier", "✘ Private cab (option: ₹3,500–4,500 for the car)"])),
            ("hotel", "gangtok"),
            ("note", ("Evening", "Light dinner near MG Marg and an early night: tomorrow starts at 8 AM at 12,300 ft.")),
        ]),
        dict(date="Sun, 22 Nov 2026", city="Gangtok", items=[
            ("activity", dict(title="Tsomgo (Changu) Lake & Baba Mandir", dur="7 Hours", where="East Sikkim", img="d_tsomgo.jpg",
                text="Timings – 0800 hrs to 1500 hrs. Drive 38 km up the Nathula road to the glacial Tsomgo Lake (12,310 ft), its edges often frozen by late November. Optional yak ride at the lake, then continue to the Baba Harbhajan Singh memorial temple before returning to Gangtok.",
                incl=["✔ Shared vehicle seat x 2, Gangtok ↔ Tsomgo ↔ Baba Mandir", "✔ Restricted-area permit arranged by the tour operator", "✘ Nathula Pass (closed Mon & Tue; extra ₹2,500–3,000 pp)", "✘ Yak ride, snow boots on rent"],
                tip="Give the operator one day ahead: photo ID + 2 passport photos each. Wear thermals; the lake is below freezing in the morning.")),
            ("activity", dict(title="MG Marg Evening Walk", dur="2 Hours", where="Gangtok", img="d_mgmarg.jpg",
                text="Gangtok's pedestrian-only, litter-free promenade. Try momos and thukpa, browse local handicrafts and enjoy the lit-up boulevard.", incl=[], tip=None)),
        ]),
        dict(date="Mon, 23 Nov 2026", city="Gangtok", items=[
            ("activity", dict(title="Gangtok Monasteries & Viewpoints Tour", dur="6 Hours", where="Gangtok", img="d_rumtek.jpg",
                text="Timings – 0900 hrs to 1500 hrs by private small car. Rumtek Monastery (24 km, seat of the Karmapa lineage), Enchey Monastery, Namgyal Institute of Tibetology, Ganesh Tok & Hanuman Tok viewpoints over the Kanchenjunga range, and the Flower Exhibition Centre.",
                incl=["✔ Private hatchback for the day (Gangtok local circuit)", "✘ Entry tickets (budgeted separately)"], tip=None)),
            ("activity", dict(title="Gangtok Ropeway", dur="1 Hour", where="Deorali", img="d_gangtok.jpg",
                text="A short cable-car ride from Deorali to the Secretariat for a bird's-eye view of the hillside city at golden hour.", incl=[], tip=None)),
        ]),
        dict(date="Tue, 24 Nov 2026", city="Pelling", items=[
            ("checkout", "Arcane Viewfinder Homestay, Gangtok • by 11:30 AM"),
            ("transfer", dict(title="Gangtok → Pelling", dur="4.5–5 Hours", kind="Shared Jeep", img="d_pemayangtse.jpg",
                text="Take a morning shared jeep from Gangtok's Deorali/SNT stand towards Gyalshing/Pelling (115 km via Singtam and Ravangla or Jorethang). Book two front seats for the best views.",
                incl=["✔ Two seats, Gangtok to Pelling", "✘ Private car (option: ₹5,000–5,500, adds a Buddha Park, Ravangla stop)"])),
            ("hotel", "pelling"),
            ("note", ("Evening", "Sunset from the homestay terrace. Ask your host to wake you if the morning is clear.")),
        ]),
        dict(date="Wed, 25 Nov 2026", city="Pelling", items=[
            ("activity", dict(title="Kanchenjunga Sunrise", dur="1 Hour", where="Pelling", img="d_pelling.jpg",
                text="Around 5:45 AM the first light turns Kanchenjunga gold. November mornings give the best chance of an unbroken view.", incl=[], tip=None)),
            ("activity", dict(title="Pelling Heritage Walk", dur="5 Hours", where="Pelling", img="d_rabdentse.jpg",
                text="An easy walking day with short local-taxi hops: Pemayangtse Monastery (1705), the forest trail to Rabdentse Ruins, the second capital of Sikkim, then the Chenrezig statue and glass Skywalk at Sangachoeling.",
                incl=["✔ Local taxi hops within Pelling", "✘ Entry tickets (budgeted separately)"], tip=None)),
        ]),
        dict(date="Thu, 26 Nov 2026", city="Pelling", items=[
            ("activity", dict(title="West Sikkim Lakes & Waterfalls", dur="7 Hours", where="West Sikkim", img="d_khecheopalri.jpg",
                text="Timings – 0900 hrs to 1600 hrs by private car. The sacred Khecheopalri 'wishing' Lake in a forest bowl, Kanchenjunga Falls, Rimbi Waterfall and the riverside orange orchards, then return via Darap, a quiet Limboo village.",
                incl=["✔ Private small car for the day", "✘ Entry tickets (budgeted separately)"], tip=None)),
            ("activity", dict(title="Rimbi Waterfall", dur="30 Min", where="Rimbi", img="d_kfalls.jpg", text="A short stop on the way back to Pelling.", incl=[], tip=None)),
        ]),
        dict(date="Fri, 27 Nov 2026", city="Pelling", items=[
            ("checkout", "Mandavya Homestay, Pelling • leave by 7 AM"),
            ("transfer", dict(title="Pelling → Siliguri → Bagdogra Airport", dur="5.5–6 Hours", kind="Shared Jeep + Taxi", img="d_bagdogra.jpg",
                text="Board the first shared jeep from Pelling to Siliguri (around 7 AM), then a local taxi for the last 14 km to Bagdogra. You reach the airport by ~2 PM, well ahead of the 17:20 departure.",
                incl=["✔ Two shared-jeep seats + Siliguri–airport taxi", "✘ Private drop (option: ₹5,500–6,000)"])),
            ("flight", None),
        ]),
    ],
    costs=[
        ("Flights", "Return flights DEL ⇄ IXB, 2 adults (QP 1807 / 6E 5379)", 32679, "Live fare, Skyscanner"),
        ("Stay", "Arcane Viewfinder Homestay, Gangtok – 3 nights", 3780, "Live rate, Booking.com"),
        ("Stay", "Mandavya Homestay, Pelling – 3 nights", 6559, "Live rate, Booking.com"),
        ("Airport transfer", "Bagdogra → Gangtok, shared airport cab (2 seats)", 2000, "Estimate"),
        ("Sightseeing", "Tsomgo Lake + Baba Mandir shared tour incl. permit (2 pax)", 2000, "₹800–1,200 pp market rate"),
        ("Sightseeing", "Gangtok monasteries & viewpoints, private car (1 day)", 2500, "Estimate"),
        ("Transfer", "Gangtok → Pelling shared jeep (2 seats)", 1000, "Estimate"),
        ("Sightseeing", "Pelling local taxi hops (Day 5)", 800, "Estimate"),
        ("Sightseeing", "West Sikkim lakes & waterfalls, private car (1 day)", 3000, "Estimate"),
        ("Airport transfer", "Pelling → Siliguri shared jeep + taxi to IXB", 1500, "Estimate"),
        ("Entry fees", "Ropeway, monasteries, Rabdentse, Skywalk, falls (2 pax)", 700, "Estimate"),
        ("Meals", "7 days × ₹1,100 for two (homestay & local cafés)", 7700, "Estimate"),
    ],
    budget_note=("Today's Delhi–Bagdogra fares alone take ₹32,679 (about 65% of your ceiling), so this plan comes in above the ₹40,000–50,000 range. "
                 "Lean levers: the 1-stop fare via Kolkata (−₹1,849), shared jeeps instead of the West Sikkim private car (−₹2,400), "
                 "and a cheaper Pelling double room such as Mochilero Ostello at ₹5,750 (−₹809). Even with all three the trip lands near ₹59,000. "
                 "The two alternative plans fit the budget."),
    info=[
        "Indian citizens need no permit for Gangtok or Pelling. Tsomgo Lake needs a restricted-area permit, which your tour operator arranges from your photo ID + 2 passport photos.",
        "Carry original photo ID for the Rangpo check-post on entry to Sikkim.",
        "Single-use plastic bottles are restricted in parts of Sikkim; carry a refillable bottle.",
        "ATMs are reliable in Gangtok; carry cash for shared jeeps and Pelling.",
        "Pack thermals, a down jacket, gloves and a woollen cap: nights drop to 3–5°C and Tsomgo is below freezing.",
    ],
    credits_keys=["gangtok","mgmarg","tsomgo","rumtek","pemayangtse","khecheopalri","rabdentse","kfalls","teesta","bagdogra","pelling"],
)

KANGRA = dict(
    slug="Kangra Valley", file="KangraValley_Bir-Barot-Naddi_Couples_Itinerary_21-27Nov2026.pdf",
    title="Kangra Valley", subtitle="3N Bir • 1N Barot • 2N Naddi",
    hero="d_naddi.jpg", hero2="d_bir.jpg", hero3="d_uhl.jpg",
    blurb=("A quieter Himachal for two. Paragliders drift over Bir's Tibetan monasteries and tea gardens, "
           "the Uhl river runs clear through pine-lined Barot, and the snow-dusted Dhauladhar wall fills the window "
           "at Naddi, a short walk above McLeod Ganj but far from its crowds."),
    highlights=[("hotel","3 Stays"),("walk","10 Sightseeing spots"),("car","5 Transfers"),("plane","Non-stop flights"),("para","Paragliding capital")],
    cities=[("Bir",3),("Barot",1),("Naddi",2)],
    weather="Bir 6–20°C • Barot 2–16°C • Naddi 5–16°C. Dry, sunny days and fresh snow on the Dhauladhar peaks.",
    flights=dict(
        out=F("SG","2950","SpiceJet","DEL","08:35","DHM","10:05","1h 30m"),
        ret=F("SG","2453","SpiceJet","DHM","10:40","DEL","12:10","1h 30m"),
        out_date="Sat, 21 Nov 2026", ret_date="Fri, 27 Nov 2026",
        price=22366, airport="Dharamshala–Kangra, Gaggal (DHM)",
        options=[
            ("★ Recommended", "SpiceJet SG 2950 • 08:35→10:05 • Non-stop", "SpiceJet SG 2453 • 10:40→12:10 • Non-stop", 22366, "Lowest fare; a full first day in Bir"),
            ("Later start", "SpiceJet SG 2450 • 12:40→14:05 • Non-stop", "SpiceJet SG 2453 • 10:40→12:10 • Non-stop", 22766, "+₹400, no early morning"),
            ("Afternoon out", "Alliance Air 9I 711 • 14:20→16:10 • Non-stop", "SpiceJet SG 2453 • 10:40→12:10 • Non-stop", 23188, "Reaches Bir after dark"),
            ("Late return", "SpiceJet SG 2950 • 08:35→10:05 • Non-stop", "Alliance Air 9I 712 • 16:20→18:10 • Non-stop", 33246, "+₹10,880 for a half day more"),
        ]),
    hotels={
        "bir": dict(name="The Bunker Bir", type="Boutique Stay", img="h_bunker.webp", score="8.7", word="Excellent", reviews=137,
                    area="Bir", near="Village Kotli, 2.3 km from Bir's Tibetan Colony and landing site", cin="21 Nov, Sat • from 12 PM", cout="24 Nov, Tue • by 11 AM",
                    room="Superior Double Room x 1", nights=3, price=4875, meal="Room only (on-site restaurant)", bed="1 double bed",
                    incl=["Adults-only property","Private bathroom; mountain-view balcony in select rooms","Heating in rooms","Restaurant, garden, terrace & bonfire","Free WiFi & free parking"],
                    policy="Non-refundable rate as listed on Booking.com", note=None),
        "barot": dict(name="Barot Palace", type="Hotel", img="h_barot.webp", score="8.5", word="Very Good", reviews=30, stars=2,
                    area="Barot", near="In Barot village, beside the Uhl river", cin="24 Nov, Tue • from 1 PM", cout="25 Nov, Wed • by 11 AM",
                    room="Double Room with Garden View x 1", nights=1, price=1512, meal="Room only (restaurant on site)", bed="1 double bed",
                    incl=["Balcony with garden view","Electric kettle & desk","Private bathroom with toiletries","Restaurant & room service","24-hour front desk, free WiFi"],
                    policy="Non-refundable rate as listed on Booking.com", note=None),
        "naddi": dict(name="Naddiva Homestay", type="Homestay", img="h_naddiva.webp", score="9.4", word="Wonderful", reviews=67,
                    area="Naddi", near="Village Naddi, 1 km from the Naddi Dhauladhar viewpoint, 4 km above McLeod Ganj", cin="25 Nov, Wed • from 12 PM", cout="27 Nov, Fri • by 12 PM",
                    room="Deluxe Double Room x 1", nights=2, price=2835, meal="Room only (on-site coffee shop)", bed="1 double bed",
                    incl=["Adults-only, smoke-free homestay","Terrace with valley views","Coffee shop & room service","Daily housekeeping","Free WiFi & free parking"],
                    policy="Non-refundable rate as listed on Booking.com", note=None),
    },
    days=[
        dict(date="Sat, 21 Nov 2026", city="Bir", items=[
            ("flight", None),
            ("transfer", dict(title="Gaggal Airport → Bir", dur="2 Hours", kind="Private Taxi", img="d_tea.jpg",
                text="Kangra taxi from the airport stand (68 km) via Kangra and Palampur, with a stop at a roadside tea estate for fresh Kangra green tea.",
                incl=["✔ One-way private sedan, airport to hotel", "✔ Tea-garden photo stop"])),
            ("hotel", "bir"),
            ("activity", dict(title="Bir Tibetan Colony & Landing Site", dur="3 Hours", where="Bir", img="d_birmon.jpg",
                text="Walk the prayer-flagged lanes of the Tibetan Colony, visit Chokling Monastery's stupa, then watch paragliders land at sunset over the tea fields.", incl=[], tip=None)),
        ]),
        dict(date="Sun, 22 Nov 2026", city="Bir", items=[
            ("activity", dict(title="Billing Take-off Ridge", dur="5 Hours", where="Billing (2,400 m)", img="d_billing.jpg",
                text="Timings – 0930 hrs to 1430 hrs. Drive 14 km up to Billing, one of the world's best paragliding take-off sites. Watch the launches, walk the meadow ridge and lunch at a ridge-top café.",
                incl=["✔ Return taxi Bir ↔ Billing", "✘ Tandem paragliding (optional: ₹2,500–3,500 per person, 15–25 min)"],
                tip="Book tandem flights only with operators registered with Himachal Tourism; flights run in the late morning when thermals build.")),
            ("activity", dict(title="Paragliding Valley Views", dur="1 Hour", where="Bir", img="d_bir.jpg", text="Back at the landing site in the afternoon for the colourful mass landings.", incl=[], tip=None)),
        ]),
        dict(date="Mon, 23 Nov 2026", city="Bir", items=[
            ("activity", dict(title="Gunehar Village & Monastery Walk", dur="5 Hours", where="Bir", img=None,
                text="A slow day for two: walk to the old Gunehar village and its waterfall pool, visit Palpung Sherabling Monastery's forest setting, then café-hop in Bir and end with a bonfire at the Bunker.", incl=["✔ On foot / local auto"], tip=None)),
        ]),
        dict(date="Tue, 24 Nov 2026", city="Barot", items=[
            ("checkout", "The Bunker Bir • by 11 AM"),
            ("transfer", dict(title="Bir → Barot", dur="1.5–2 Hours", kind="Private Taxi", img="d_barotv.jpg",
                text="A 40 km mountain road via Ghatasani into the Chhota Bhangal valley, lined with pine and deodar.", incl=["✔ One-way private sedan"])),
            ("hotel", "barot"),
            ("activity", dict(title="Uhl River, Trout Farm & Barot Reservoir", dur="3 Hours", where="Barot", img="d_uhl.jpg",
                text="Stroll the Uhl riverbank, visit the government trout hatchery and walk across to Lohardi village. Barot sees few tourists in late November.", incl=[], tip=None)),
        ]),
        dict(date="Wed, 25 Nov 2026", city="Naddi", items=[
            ("checkout", "Barot Palace • by 11 AM"),
            ("transfer", dict(title="Barot → Baijnath → Naddi", dur="4.5 Hours", kind="Private Taxi", img="d_dharamshala.jpg",
                text="140 km via Jogindernagar and Palampur with a stop at the 13th-century Baijnath Shiva temple, then up through Dharamshala to Naddi.", incl=["✔ One-way private sedan with temple stop"])),
            ("hotel", "naddi"),
            ("activity", dict(title="Naddi Sunset Point", dur="1 Hour", where="Naddi", img="d_naddi.jpg",
                text="A 10-minute walk from the homestay to the viewpoint as the Dhauladhar turns pink.", incl=[], tip=None)),
        ]),
        dict(date="Thu, 26 Nov 2026", city="Naddi", items=[
            ("activity", dict(title="Dharamkot, Bhagsu & McLeod Ganj", dur="7 Hours", where="Dharamshala", img="d_bhagsu.jpg",
                text="Walk the forest path from Naddi to Dharamkot and Bhagsu waterfall, then descend to McLeod Ganj for the Tsuglagkhang (Dalai Lama temple) complex and Tibetan lunch. Fit couples can instead hike towards Triund (9 km, start by 8 AM).",
                incl=["✔ Local taxi back up to Naddi", "✘ Guide for the Triund trek"], tip=None)),
        ]),
        dict(date="Fri, 27 Nov 2026", city="Naddi", items=[
            ("checkout", "Naddiva Homestay • leave by 9 AM"),
            ("transfer", dict(title="Naddi → Gaggal Airport", dur="50 Min", kind="Private Taxi", img="d_dharamshala.jpg",
                text="20 km downhill to Kangra airport for the 10:40 departure.", incl=["✔ One-way private sedan"])),
            ("flight", None),
        ]),
    ],
    costs=[
        ("Flights", "Return flights DEL ⇄ DHM, 2 adults (SG 2950 / SG 2453)", 22366, "Live fare, Skyscanner"),
        ("Stay", "The Bunker Bir – 3 nights", 4875, "Live rate, Booking.com"),
        ("Stay", "Barot Palace – 1 night", 1512, "Live rate, Booking.com"),
        ("Stay", "Naddiva Homestay, Naddi – 2 nights", 2835, "Live rate, Booking.com"),
        ("Airport transfer", "Gaggal Airport → Bir, private sedan", 2600, "Estimate"),
        ("Sightseeing", "Bir ↔ Billing return taxi", 1000, "Estimate"),
        ("Transfer", "Bir → Barot, private sedan", 2400, "Estimate"),
        ("Transfer", "Barot → Baijnath → Naddi, private sedan", 4300, "Estimate"),
        ("Sightseeing", "McLeod Ganj local taxi (Day 6)", 600, "Estimate"),
        ("Airport transfer", "Naddi → Gaggal Airport", 900, "Estimate"),
        ("Entry fees", "Monasteries, Baijnath, trout farm (mostly free)", 200, "Estimate"),
        ("Meals", "7 days × ₹1,000 for two (cafés & dhabas)", 7000, "Estimate"),
    ],
    budget_note=("This plan sits at the top of your range. Tandem paragliding is not included: add ₹5,000–7,000 for two. "
                 "To create room, take shared jeeps between Bir and Billing (−₹700) or skip the Barot night and stay 4 nights in Bir."),
    info=[
        "No permits needed. Carry a photo ID for hotel check-in.",
        "SpiceJet DHM flights are weather-sensitive in winter; keep the afternoon of 27 Nov free in case of a delay.",
        "Barot has patchy mobile data (BSNL/Jio best); download offline maps.",
        "Carry cash: Barot and Billing have few card terminals.",
        "Pack thermals and a warm jacket; Barot nights drop close to freezing.",
    ],
    credits_keys=["naddi","bir","uhl","tea","birmon","billing","triund","barotv","dharamshala","bhagsu"],
)

GARHWAL = dict(
    slug="Garhwal Hills", file="GarhwalHills_Chakrata-Kanatal_Couples_Itinerary_21-27Nov2026.pdf",
    title="Garhwal Hills", subtitle="3N Chakrata • 3N Kanatal",
    hero="d_chakrata.jpg", hero2="d_tehri.jpg", hero3="d_surkanda.jpg",
    blurb=("Fifty minutes from Delhi by air, yet far from the Mussoorie crowds. Chakrata is a quiet army cantonment "
           "wrapped in deodar forest with Himalayan views from Deoban; Kanatal sits on a ridge facing the snow peaks, "
           "a short walk from the Surkanda Devi temple and above the blue expanse of Tehri Lake."),
    highlights=[("hotel","2 Stays"),("walk","8 Sightseeing spots"),("car","6 Transfers"),("plane","50-min flights"),("leaf","Deodar forests")],
    cities=[("Chakrata",3),("Kanatal",3)],
    weather="Chakrata 4–16°C • Kanatal 4–15°C. Clear, crisp days and the first snow on the Bandarpunch and Swargarohini peaks.",
    flights=dict(
        out=F("6E","6524","IndiGo","DEL","07:30","DED","08:20","50m"),
        ret=F("6E","6464","IndiGo","DED","20:05","DEL","20:55","50m"),
        out_date="Sat, 21 Nov 2026", ret_date="Fri, 27 Nov 2026",
        price=15926, airport="Dehradun, Jolly Grant (DED)",
        options=[
            ("★ Recommended", "IndiGo 6E 6524 • 07:30→08:20 • Non-stop", "IndiGo 6E 6464 • 20:05→20:55 • Non-stop", 15926, "Full last day, room for Tehri Lake"),
            ("Lowest fare", "IndiGo 6E 6524 • 07:30→08:20 • Non-stop", "IndiGo 6E 6530 • 08:55→09:45 • Non-stop", 14778, "−₹1,148 but a 5 AM start from Kanatal"),
            ("Evening return", "IndiGo 6E 6524 • 07:30→08:20 • Non-stop", "IndiGo 6E 6227 • 17:05→18:00 • Non-stop", 16556, "Home before dinner"),
            ("Air India out", "Air India AI 437 • 09:20→10:20 • Non-stop", "IndiGo 6E 6530 • 08:55→09:45 • Non-stop", 16401, "Later morning start"),
        ]),
    hotels={
        "chakrata": dict(name="DS Residency Homestay, Chakrata", type="Homestay", img="h_dsres.webp", score="9.0", word="Wonderful", reviews=17,
                    area="Chakrata", near="New Block Office Road, 4 km from Chakrata market", cin="21 Nov, Sat • from 12 PM", cout="24 Nov, Tue • by 10 AM",
                    room="Double Room x 1", nights=3, price=7654, meal="As per rate; home-cooked meals on request", bed="1 double bed",
                    incl=["Mountain views & garden","Room heating","Non-smoking rooms","Free WiFi","Free private parking"],
                    policy="Free cancellation • No prepayment needed (Booking.com)", note=None),
        "kanatal": dict(name="Wild Way Resort", type="Resort", img="h_wildway.webp", score="9.7", word="Exceptional", reviews=14, stars=3,
                    area="Kanatal", near="Kaudia (Kodiya) forest range, 0.6 km from Kanatal", cin="24 Nov, Tue • from 12 PM", cout="27 Nov, Fri • by 10 AM",
                    room="Double Room x 1", nights=3, price=6300, meal="Room only", bed="1 double bed",
                    incl=["24-hour front desk","Smoke-free property","Free WiFi","Free private parking","Airport shuttle on request (paid)"],
                    policy="Free cancellation (Booking.com)", note=None),
    },
    days=[
        dict(date="Sat, 21 Nov 2026", city="Chakrata", items=[
            ("flight", None),
            ("transfer", dict(title="Jolly Grant Airport → Chakrata", dur="3.5 Hours", kind="Private Taxi", img="d_chakrata.jpg",
                text="115 km via Dehradun, Vikasnagar and Kalsi (stop at the Ashokan rock edict), then the winding climb to Chakrata at 2,118 m.",
                incl=["✔ One-way private sedan", "✔ Kalsi photo stop"])),
            ("hotel", "chakrata"),
            ("note", ("Evening", "Sunset walk to Chilmiri Neck on the cantonment ridge. Chakrata is an army area: photography of installations is not allowed.")),
        ]),
        dict(date="Sun, 22 Nov 2026", city="Chakrata", items=[
            ("activity", dict(title="Deoban Deodar Forest & Himalayan View", dur="4 Hours", where="Deoban (2,800 m)", img="d_deoban.jpg",
                text="Timings – 0800 hrs to 1200 hrs. Drive 13 km to Deoban for a 180° view of the snow peaks through ancient deodar and oak forest. Gentle forest walk and picnic breakfast.",
                incl=["✔ Private car for the day (Deoban + Tiger Falls)"], tip="Carry snacks and water: there are no shops at Deoban.")),
            ("activity", dict(title="Tiger Falls", dur="3 Hours", where="near Chakrata", img=None,
                text="Afternoon at Tiger Falls, a 50 m single-drop cascade reached by a 1.5 km walk down from the road head.", incl=["✘ Entry ticket at gate (budgeted)"], tip=None)),
        ]),
        dict(date="Mon, 23 Nov 2026", city="Chakrata", items=[
            ("activity", dict(title="Slow Day: Village Trails & Ram Tal", dur="5 Hours", where="Chakrata", img="d_lakhamandal.jpg",
                text="A free day together. Walk the Jaunsari village trails and Ram Tal horticulture garden, or hire a car for Lakhamandal, an ancient Shiva temple complex on the Yamuna (optional, ~₹3,000).", incl=["✔ On foot"], tip=None)),
        ]),
        dict(date="Tue, 24 Nov 2026", city="Kanatal", items=[
            ("checkout", "DS Residency Homestay • by 10 AM"),
            ("transfer", dict(title="Chakrata → Mussoorie → Kanatal", dur="5 Hours", kind="Private Taxi", img="d_dhanaulti.jpg",
                text="140 km via Yamuna Bridge, Kempty Falls and the Mussoorie bypass, then along the Dhanaulti ridge to Kanatal.", incl=["✔ One-way private sedan with Kempty Falls stop"])),
            ("hotel", "kanatal"),
            ("note", ("Evening", "Bonfire and stargazing: Kanatal has very little light pollution.")),
        ]),
        dict(date="Wed, 25 Nov 2026", city="Kanatal", items=[
            ("activity", dict(title="Surkanda Devi Temple at Sunrise", dur="4 Hours", where="Kaddukhal", img="d_surkanda.jpg",
                text="Taxi 8 km to Kaddukhal, then the ropeway or a 2 km climb to Surkanda Devi (2,757 m) for a panorama of Chaukhamba, Bandarpunch and the Gangotri peaks.",
                incl=["✔ Local taxi to Kaddukhal and back", "✘ Ropeway ticket (budgeted)"], tip=None)),
            ("activity", dict(title="Kaudia Forest Walk", dur="2 Hours", where="Kanatal", img="d_kanatal.jpg", text="Afternoon walk in the Kaudia (Kodiya) forest behind the resort.", incl=[], tip=None)),
        ]),
        dict(date="Thu, 26 Nov 2026", city="Kanatal", items=[
            ("activity", dict(title="Dhanaulti Eco Park & Apple Orchards", dur="4 Hours", where="Dhanaulti", img="d_dhanaulti.jpg",
                text="12 km to Dhanaulti's twin eco-parks (Amber & Dhara) among deodars; walk through apple orchards and potato farms. Back for a late lunch and a lazy evening.",
                incl=["✔ Local taxi Kanatal ↔ Dhanaulti"], tip=None)),
        ]),
        dict(date="Fri, 27 Nov 2026", city="Kanatal", items=[
            ("checkout", "Wild Way Resort • by 10 AM"),
            ("activity", dict(title="Tehri Lake en route to the Airport", dur="3 Hours", where="New Tehri", img="d_tehri.jpg",
                text="Drive 40 km down to Tehri Lake, one of Asia's largest dam reservoirs. Optional boat ride (₹1,000–2,000), then continue via Chamba and Rishikesh.",
                incl=["✔ Covered in the airport transfer below", "✘ Boating / water sports"], tip=None)),
            ("transfer", dict(title="Kanatal → Tehri → Jolly Grant Airport", dur="4 Hours driving", kind="Private Taxi", img="d_dehradun.jpg",
                text="Leave Tehri by 3:30 PM to reach the airport by ~6:30 PM for the 20:05 flight.", incl=["✔ One-way private sedan incl. Tehri halt"])),
            ("flight", None),
        ]),
    ],
    costs=[
        ("Flights", "Return flights DEL ⇄ DED, 2 adults (6E 6524 / 6E 6464)", 15926, "Live fare, Skyscanner"),
        ("Stay", "DS Residency Homestay, Chakrata – 3 nights", 7654, "Live rate, Booking.com"),
        ("Stay", "Wild Way Resort, Kanatal – 3 nights", 6300, "Live rate, Booking.com"),
        ("Airport transfer", "Jolly Grant → Chakrata, private sedan", 3000, "Estimate"),
        ("Sightseeing", "Deoban + Tiger Falls, private car (1 day)", 1800, "Estimate"),
        ("Transfer", "Chakrata → Kanatal, private sedan", 3500, "Estimate"),
        ("Sightseeing", "Surkanda Devi local taxi", 800, "Estimate"),
        ("Sightseeing", "Dhanaulti local taxi", 1000, "Estimate"),
        ("Airport transfer", "Kanatal → Tehri Lake → Jolly Grant", 3200, "Estimate"),
        ("Entry fees", "Tiger Falls, Surkanda ropeway, Dhanaulti eco-park (2 pax)", 600, "Estimate"),
        ("Meals", "7 days × ₹1,000 for two", 7000, "Estimate"),
    ],
    budget_note=("This plan sits at the top of your range. Both stays have free cancellation, so you can book now and adjust. "
                 "The 08:55 return flight saves ₹1,148 but means leaving Kanatal at 5 AM; Lakhamandal and Tehri boating are optional extras."),
    info=[
        "No permits needed. Chakrata is a cantonment: do not photograph army installations.",
        "Fuel up in Vikasnagar or Mussoorie; pumps are sparse near Chakrata.",
        "Mobile coverage is good in Kanatal and patchy around Deoban.",
        "Carry cash for local taxis and dhabas.",
        "Pack thermals and a warm jacket; mornings are near freezing.",
    ],
    credits_keys=["deoban","chakrata","surkanda","mussoorie","lakhamandal","dhanaulti","kanatal","tehri","dehradun"],
)

TRIPS = [SIKKIM, KANGRA, GARHWAL]
