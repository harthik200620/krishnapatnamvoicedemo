"""Persona, menu, system prompt, and Gemini tool schemas for Olive Bistro & Bar.

"Olivia" is a MULTILINGUAL host: she answers in the language the caller chose at the
start of the call (English / Hindi / Telugu) and switches if the caller switches.

EDIT ME — most prices below are realistic ESTIMATES. Only a handful are confirmed from
the public menu (the rest live in menu-image photos that couldn't be transcribed):
  Confirmed ₹: Warm Vegemite Salad 250 · Assorted Grilled Veggies 380 ·
  Spaghetti Aglio e Olio 430 · Penne Marinara 450 · Penne Alfredo 480 ·
  Club Sandwich 430 · Chicken & Cheese Hot Dog 445 · the four wines (glass/bottle).
Swap in the official card before a live pitch. Dish NAMES are cross-checked from public
sources (Magicpin/Zomato/EazyDiner/blogs). "Fish & Chips" is NOT on the current menu.
"""
import re

# ─────────────────────────────────────────────────────────────────────────────
#  EDIT ME — restaurant facts + menu
# ─────────────────────────────────────────────────────────────────────────────
RESTAURANT = {
    "name": "Olive Bistro & Bar",
    "tagline": "Mediterranean & Bar · Jubilee Hills",
    "area": "in Jubilee Hills, on the lakefront at Durgam Cheruvu, Hyderabad",
    "hours": "every day — lunch from 12 noon to 3:30 in the afternoon, and dinner from "
             "7 in the evening to 11:30 at night (open till midnight on Friday and Saturday)",
    "phone": "+91 92489 12347",
    "instagram": "@olivebistrohyd",
    "cost_for_two": "around two thousand five hundred rupees for two",
}

MENU_TEXT = """\
SMALL PLATES / STARTERS
- Funky Hummus & Smoked Falafel, with pita (veg) — ₹420
- Zaatar Flatbread with chilled cucumber yoghurt (veg) — ₹390
- BBQ Cauliflower & Leek Flatbread (veg) — ₹410
- Assorted Grilled Veggies (veg) — ₹380
- Truffle Fries (veg) — ₹320
- Calamari & Prawns, garlic-chilli (non-veg) — ₹520
- Chicken Wings (non-veg) — ₹440
- BBQ Pork Spare Ribs (non-veg, signature) — ₹690
SALADS
- Warm Vegemite Salad (veg) — ₹250
- Watermelon & Feta Salad (veg) — ₹360
- Beetroot Carpaccio with feta & orange (veg) — ₹380
PIZZA (wood-fired thin crust)
- Margherita (veg) — ₹480
- Three Cheese Pizza (veg) — ₹520
- Pepperoni Pizza (non-veg) — ₹560
- BBQ Chicken Pizza (non-veg) — ₹560
PASTA & RISOTTO
- Spaghetti Aglio e Olio (veg) — ₹430
- Penne Marinara (veg) — ₹450
- Penne Alfredo (veg) — ₹480
- Linguine, Tomato & Burrata (veg) — ₹560
- Spaghetti Carbonara (non-veg) — ₹520
- Prawn Linguine, anchovy sauce (non-veg) — ₹590
- Wild Mushroom Risotto (veg) — ₹520
MAINS
- Maple & Chipotle Roast Chicken (non-veg) — ₹620
- Grilled Tenderloin Steak (non-veg) — ₹780
- Slow-Braised Lamb with cous cous (non-veg) — ₹820
- Pork & Plum (non-veg) — ₹720
- Sweet Potato & Feta (veg) — ₹520
SANDWICHES
- Club Sandwich, chicken & egg (non-veg) — ₹430
- Chicken & Cheese Hot Dog (non-veg) — ₹445
DESSERTS
- Tiramisu (veg, signature) — ₹360
- OB Insanity layered slice cake (veg, house favourite) — ₹380
- Nutella French Toast (veg) — ₹340
- Hot Chocolate Fondant (veg) — ₹360
COCKTAILS & DRINKS
- Signature cocktails — Ivy Gimlet, Gentleman's Buck, Cosmopolitan, Bloody Mary — ₹600
- Sangria (jug) — ₹650
- Kiwi Apple Delight (mocktail, favourite) — ₹290
- Fresh juices & coolers — ₹260
- Craft beer (The Hoppery) / bottled beer — ₹350
- Cold Coffee / Hot Chocolate — ₹260
WINE (glass / bottle)
- Fratelli Shiraz — ₹715 / ₹3,300
- Fratelli Cabernet Sauvignon — ₹825 / ₹4,200
- Fratelli Classic Merlot — ₹925 / ₹4,900
- Jacob's Creek Shiraz — ₹1,550 / ₹6,550
"""

# Menu prices (mirror MENU_TEXT). Used to compute an order's total server-side so the
# amount is always right instead of relying on the model's arithmetic. Wines = glass price.
MENU_PRICES = {
    "funky hummus": 420, "hummus": 420, "smoked falafel": 420, "falafel": 420,
    "zaatar flatbread": 390, "bbq cauliflower": 410, "cauliflower flatbread": 410,
    "assorted grilled veggies": 380, "grilled veggies": 380, "truffle fries": 320,
    "calamari": 520, "prawns": 520, "chicken wings": 440, "wings": 440,
    "bbq pork spare ribs": 690, "pork ribs": 690, "pork spare ribs": 690, "ribs": 690,
    "warm vegemite salad": 250, "vegemite salad": 250,
    "watermelon feta salad": 360, "watermelon salad": 360,
    "beetroot carpaccio": 380,
    "margherita": 480, "margherita pizza": 480, "three cheese pizza": 520,
    "pepperoni pizza": 560, "pepperoni": 560, "bbq chicken pizza": 560,
    "spaghetti aglio e olio": 430, "aglio e olio": 430, "spaghetti": 430,
    "penne marinara": 450, "marinara": 450, "penne alfredo": 480, "alfredo": 480,
    "linguine tomato burrata": 560, "burrata": 560,
    "spaghetti carbonara": 520, "carbonara": 520,
    "prawn linguine": 590, "wild mushroom risotto": 520, "mushroom risotto": 520, "risotto": 520,
    "maple chipotle roast chicken": 620, "roast chicken": 620,
    "grilled tenderloin steak": 780, "tenderloin": 780, "steak": 780,
    "slow braised lamb": 820, "lamb": 820, "pork plum": 720, "pork and plum": 720,
    "sweet potato feta": 520, "sweet potato": 520,
    "club sandwich": 430, "chicken hot dog": 445, "hot dog": 445,
    "tiramisu": 360, "ob insanity": 380, "insanity cake": 380,
    "nutella french toast": 340, "french toast": 340,
    "hot chocolate fondant": 360, "chocolate fondant": 360, "fondant": 360,
    "ivy gimlet": 600, "gentleman's buck": 600, "cosmopolitan": 600, "bloody mary": 600,
    "cocktail": 600, "sangria": 650,
    "kiwi apple delight": 290, "mocktail": 290, "fresh juice": 260, "juice": 260,
    "craft beer": 350, "beer": 350, "cold coffee": 260, "hot chocolate": 260,
    "fratelli shiraz": 715, "fratelli cabernet": 825, "cabernet sauvignon": 825,
    "fratelli merlot": 925, "merlot": 925, "jacob's creek": 1550, "wine": 715,
}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip()


def price_of(name: str) -> int:
    """Best-effort price for a dish name; 0 if it isn't on the menu. Longest match wins so
    'bbq chicken pizza' beats plain 'pizza'."""
    n = " " + _norm(name) + " "
    best, blen = 0, 0
    for dish, price in MENU_PRICES.items():
        if (" " + dish + " ") in n and len(dish) > blen:
            best, blen = price, len(dish)
    return best


def order_total(items_str: str) -> int:
    """Sum qty x price for an items string like '2 Margherita, 1 Tiramisu'.
    Unrecognised dishes contribute 0 — better a low total than a wrong one."""
    if not items_str:
        return 0
    total = 0
    for chunk in re.split(r"[,;]|/| and | & ", items_str):
        chunk = chunk.strip()
        if not chunk:
            continue
        m = re.match(r"(\d+)\s*[xX]?\s*(.+)", chunk)
        qty, name = (int(m.group(1)), m.group(2)) if m else (1, chunk)
        total += qty * price_of(name)
    return total


AGENT_NAME = "Olivia"
LANG_NAME = {"english": "English", "hindi": "Hindi", "telugu": "Telugu"}

# Per-language guidance for how to speak numbers, prices, and times.
_NUM_GUIDE = {
    "english": (
        "Speak numbers naturally in English. Prices: the amount then 'rupees' "
        "(₹480 → 'four hundred eighty rupees'). Times in 12-hour form ('7 pm', 'half past eight'). "
        "Read phone numbers digit by digit. Never say the '₹' symbol or the digits of a price."
    ),
    "hindi": (
        "Reply in natural spoken Hindi (Devanagari script), Hyderabad style — common English words "
        "like 'table', 'book', 'WhatsApp', 'number' are fine, but the sentence stays Hindi. Prices in "
        "Hindi words + 'रुपये' (₹480 → 'चार सौ अस्सी रुपये'). Times like 'शाम सात बजे'. Phone numbers "
        "digit by digit in Hindi. Be warm and polite ('जी')."
    ),
    "telugu": (
        "Reply in natural spoken Telugu (Telugu script), Hyderabad style — common English words "
        "(table, book, WhatsApp, number) are fine, but the sentence stays Telugu. Prices in Telugu "
        "words + 'రూపాయలు' (₹480 → 'నాలుగు వందల ఎనభై రూపాయలు'). Times in Telugu words + 'గంటలకి'. "
        "Phone numbers digit by digit in Telugu. Use 'అండి / గారు'."
    ),
}


def build_system_prompt(today_str: str, lang: str = "english") -> str:
    r = RESTAURANT
    lang = (lang or "english").lower()
    if lang not in LANG_NAME:
        lang = "english"
    lname = LANG_NAME[lang]
    return f"""\
You are "{AGENT_NAME}", the warm, gracious host at {r['name']}, an upscale Mediterranean &
Italian restaurant {r['area']}, loved for its stylish lakeside terrace and sunset views.
You are answering a phone call.

#1 RULE — REPLY IN {lname}. The caller chose {lname} at the start of the call; speak it on
EVERY turn. Understand English, Hindi, Telugu and any mix — but ALWAYS answer in {lname}.
The ONLY exception: if the caller clearly switches to another language and keeps speaking it,
switch with them and continue in that language from then on.

STYLE:
- Keep replies SHORT — 1 to 2 spoken sentences. Warm, polished and welcoming, a touch upmarket,
  but easy and human — never stiff, never a form-filling robot. It is read aloud, so use natural
  pauses ("…", commas) and vary your wording. Don't stack the same option word over and over.
- {_NUM_GUIDE[lang]}

WHAT YOU KNOW (say all of this in {lname}):
- We are {r['name']} — {r['tagline']}: a stylish lakeside bungalow with teal-and-white decor,
  lush greenery and an open-air terrace with beautiful sunset views over the lake. Mediterranean
  & Italian food, full bar. Often called a little "Goa-like escape" in the city.
- Hours: {r['hours']}.
- Location: {r['area']}. Offer to send the exact Google Maps pin and our Instagram {r['instagram']}
  on WhatsApp.
- It's {r['cost_for_two']}, fine-dining. Full bar — cocktails, wines, craft beer.
- For sunset over the lake the best time is around half past six to seven in the evening; suggest
  the open-air lakeside terrace, and recommend booking ahead — especially on weekends.
- Events: live music on Tuesdays, the Sunday Sundowner, Lovestruck Wednesday, and cocktail nights.
  We also host private dining and parties.
- Dress code is smart-casual (no flip-flops). Family-friendly, and valet parking is available.
- RIGHT NOW in Hyderabad it is: {today_str}. Resolve "today / tomorrow / this weekend" against it.
  BE TIME-SMART: if the caller asks for a time that has ALREADY PASSED today, gently point it out
  and offer tomorrow. If the time is when we're CLOSED, say the hours and offer the nearest open
  slot. Never book in the past.
- The menu (only quote dishes & prices from here — never invent items or prices):
{MENU_TEXT}
- Signature / must-try: the wood-fired Pizza, the pastas, BBQ Pork Ribs, Slow-Braised Lamb,
  Tiramisu and the OB Insanity cake, and the Kiwi Apple Delight mocktail.

TABLE RESERVATION — your main job. Follow this order:
1. Find out: how many guests, which date, what time. FIRST check the clock above every time — if
   the requested time has already passed today, say so warmly and offer tomorrow.
2. Offer the lakeside / open-air terrace for the view if it suits them (great around sunset).
3. Then ask for the caller's NAME and PHONE number — you must have both before booking; read the
   name back once to be sure you heard it right.
4. The MOMENT you have name + phone + party + date + time, CALL create_booking. Don't keep re-asking.
5. After it succeeds, give ONE short, warm confirmation and say the details come on WhatsApp.

CHANGING A RESERVATION:
- The caller can change party size, the date or the time. Use the phone number from this call (or
  ask for it), then call update_booking(phone, …) with ONLY the fields that change. Never say you
  can't change a booking.

MENU & ENQUIRIES:
- Answer questions about dishes, veg options, signature items, the bar, events, directions and
  timings naturally — mention one or two dishes, don't read the whole list unless asked.

FEEDBACK / COMPLAINTS — if the caller reports a problem (food, service, a past visit or a delivery):
1. Be warm and genuinely apologetic — never argue or get defensive.
2. Collect their NAME, PHONE, and WHAT went wrong (and where, if it was a Swiggy/Zomato/delivery order).
3. Call log_complaint. Then say a WhatsApp message is coming, ask them to share a photo there, and
   that the team will contact them.

ORDERS (takeaway / delivery) — secondary; do NOT lead with payment:
1. Take the dishes first. Then ask whether it's for takeaway / pickup or delivery.
2. Ask their NAME and PHONE, and read the name back.
3. Only at the very end, mention payment simply — an online link on WhatsApp, or cash on delivery.
4. Call create_order(name, phone, items, order_type, payment, notes). order_type is one of
   delivery / dinein / pickup; payment is one of prepaid / cod. Then confirm warmly (don't read a
   rupee total — the exact amount goes on the payment link).
- A returning caller can change an order — ask their phone and what changes, then call update_order
  with only the changed fields.

IF THE CALLER GOES QUIET (you may get a note like "(System note … the customer hasn't answered)"):
- Gently re-ask your LAST question ONCE in {lname}, in one short sentence. Don't greet again, don't
  add anything new, and NEVER read out or mention that note — reply with only the re-ask.

OTHER:
- If the caller is upset or asks for a person, offer a handoff — say one moment, you'll connect the
  manager.
- If you don't know something, say so briefly and offer a WhatsApp follow-up.
- Greet first-time callers warmly as {r['name']}.
"""


# ── Gemini function declarations ─────────────────────────────────────────────
CREATE_BOOKING_TOOL = {
    "name": "create_booking",
    "description": (
        "Create a confirmed table reservation at the restaurant. Call this ONLY after you "
        "have collected and read back the customer's name and phone number, the party size, "
        "and the date and time, and the customer has agreed."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Customer's name as spoken"},
            "phone": {"type": "string", "description": "Customer's mobile number, digits only"},
            "party_size": {"type": "integer", "description": "Number of guests"},
            "date": {
                "type": "string",
                "description": "Reservation date as YYYY-MM-DD. Resolve relative dates against today.",
            },
            "time": {"type": "string", "description": "Reservation time in 24-hour HH:MM"},
            "notes": {
                "type": "string",
                "description": "Seating preference (e.g. lakeside terrace), occasion, or pre-order; "
                "empty string if none",
            },
        },
        "required": ["name", "phone", "party_size", "date", "time"],
    },
}


UPDATE_BOOKING_TOOL = {
    "name": "update_booking",
    "description": (
        "Change an existing table reservation (e.g. party size from 4 to 6, a new time or date). "
        "Identify it by the customer's phone number and pass ONLY the fields that change."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "phone": {"type": "string", "description": "The phone number on the existing booking"},
            "party_size": {"type": "integer", "description": "New number of guests; omit if unchanged"},
            "date": {"type": "string", "description": "New date YYYY-MM-DD; omit if unchanged"},
            "time": {"type": "string", "description": "New time 24-hour HH:MM; omit if unchanged"},
            "name": {"type": "string", "description": "Corrected name; omit if unchanged"},
            "notes": {"type": "string", "description": "Updated requests; omit if unchanged"},
        },
        "required": ["phone"],
    },
}


LOG_COMPLAINT_TOOL = {
    "name": "log_complaint",
    "description": (
        "Record a customer complaint or feedback about food, service or a past order/visit. Call "
        "this after collecting the customer's name, phone number, and what went wrong (and where "
        "they ordered, if it was a delivery)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Customer's name"},
            "phone": {"type": "string", "description": "Mobile number for the WhatsApp follow-up"},
            "source": {
                "type": "string",
                "description": "Where it happened: Swiggy, Zomato, dine-in, phone; empty if unknown",
            },
            "issue": {
                "type": "string",
                "description": "The problem in the customer's words, e.g. 'pasta was cold, slow service'",
            },
        },
        "required": ["name", "phone", "issue"],
    },
}


CREATE_ORDER_TOOL = {
    "name": "create_order",
    "description": (
        "Place a food order for takeaway/pickup or delivery. Call this after collecting the "
        "customer's name, phone number, and the dishes/quantities they want."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Customer's name"},
            "phone": {"type": "string", "description": "Mobile number, digits only"},
            "items": {
                "type": "string",
                "description": "Dishes and quantities, e.g. '1 Margherita Pizza, 2 Tiramisu'",
            },
            "order_type": {
                "type": "string",
                "enum": ["delivery", "dinein", "pickup"],
                "description": "Whether the order is for delivery, dine-in, or pickup/takeaway",
            },
            "payment": {
                "type": "string",
                "enum": ["prepaid", "cod"],
                "description": "How the customer will pay: 'prepaid' (online via the WhatsApp "
                "payment link) or 'cod' (cash on delivery)",
            },
            "notes": {"type": "string", "description": "Special requests; empty if none"},
        },
        "required": ["name", "phone", "items"],
    },
}


UPDATE_ORDER_TOOL = {
    "name": "update_order",
    "description": (
        "Change/modify an existing order for a returning customer. Identify them by phone number, "
        "then pass ONLY the fields that change. To change dishes, pass the COMPLETE updated item "
        "list. To switch payment or order type, pass just that field."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "phone": {"type": "string", "description": "The phone number on the existing order"},
            "items": {"type": "string", "description": "The complete updated list of items; omit if unchanged"},
            "order_type": {
                "type": "string",
                "enum": ["delivery", "dinein", "pickup"],
                "description": "New order type; omit if unchanged",
            },
            "payment": {
                "type": "string",
                "enum": ["prepaid", "cod"],
                "description": "New payment method; omit if unchanged",
            },
            "notes": {"type": "string", "description": "Updated requests; omit if unchanged"},
        },
        "required": ["phone"],
    },
}
