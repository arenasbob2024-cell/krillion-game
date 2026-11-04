# -*- coding: utf-8 -*-
"""Static site builder for the Krillion Game Guide (independent fan site)."""
import json, os, html
from prompts import PROMPTS, TIER_NAMES, TIER_POINTS, tier_for

BASE = "https://krillion-game-lyart.vercel.app"
NAME = "Krillion Game Guide"
DATE = "2026-11-04"
TAG = "Independent Krillion guide and practice tool"

NAV = [
    ("", "Home"),
    ("practice", "Practice"),
    ("how-to-play", "How to play"),
    ("strategy", "Strategy"),
    ("about", "About"),
]

DISCLAIMER = (
    "Independent fan guide and practice tool. Not affiliated with, endorsed by, or sponsored by "
    "Krillion or krillion.io. Krillion is the name of a game owned by its developer; all rights stay "
    "with its owner. Our practice prompts, answer lists and tiers are original estimates, not official "
    "Krillion data. Always play the official Daily Dive at "
    '<a href="https://krillion.io/" rel="noopener nofollow">krillion.io</a>.'
)


def url_for(slug):
    return BASE + "/" + (slug + "/" if slug else "")


def ld_graph(slug, title, desc, faqs=None, app=False):
    url = url_for(slug)
    graph = [
        {
            "@type": "WebPage",
            "@id": url + "#page",
            "url": url,
            "name": title,
            "description": desc,
            "inLanguage": "en",
            "datePublished": DATE,
            "dateModified": DATE,
            "isPartOf": {"@type": "WebSite", "@id": BASE + "/#site"},
        }
    ]
    if app:
        graph.append({
            "@type": "WebApplication",
            "@id": BASE + "/practice/#app",
            "name": "Krillion Practice Dive",
            "url": url_for("practice"),
            "description": "A free browser practice game with an original prompt bank: seven prompts, 25 seconds each, rarity-style scoring.",
            "applicationCategory": "GameApplication",
            "operatingSystem": "Any (web browser)",
            "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        })
    if slug:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": title.split(":")[0], "item": url},
            ],
        })
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })
    return {"@context": "https://schema.org", "@graph": graph}


def nav_html(slug):
    out = []
    for s, label in NAV:
        cur = ' aria-current="page"' if s == slug else ""
        out.append('<a href="/%s"%s>%s</a>' % (s + "/" if s else "", cur, label))
    return '<nav class="site" aria-label="Site">' + "".join(out) + "</nav>"


def crumb(title):
    short = title.split(":")[0]
    return '<p class="breadcrumb"><a href="/">Home</a> › ' + html.escape(short) + "</p>"


def page(slug, title, desc, h1, lede, body, faqs=None, app=False, extra_head="", body_class=""):
    url = url_for(slug)
    ld = json.dumps(ld_graph(slug, title, desc, faqs, app), ensure_ascii=False).replace("</", "<\\/")
    faq_html = ""
    if faqs:
        faq_html = '<section id="faq"><h2>Frequently asked questions</h2>' + "".join(
            "<h3>%s</h3><p>%s</p>" % (html.escape(q), html.escape(a)) for q, a in faqs
        ) + "</section>"
    doc = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="index,follow">
<link rel="canonical" href="%(url)s">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css?v=20261104">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%(name)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#04121f">
<script type="application/ld+json">%(ld)s</script>
%(extra)s
</head>
<body class="%(body_class)s">
<main>
<header class="site">
  <a class="brand" href="/">Krillion <span>Game Guide</span></a>
  %(nav)s
</header>
%(crumb)s
<h1>%(h1)s</h1>
%(lede)s
%(body)s
%(faq)s
<div class="disclaimer">%(disclaimer)s</div>
<footer class="site">
  <p><a href="/about/">About &amp; editorial policy</a> · <a href="/privacy/">Privacy</a> · <a href="/how-to-play/">How to play</a> · <a href="/strategy/">Strategy</a> · <a href="/practice/">Practice dive</a></p>
  <p>Updated %(date)s. Official game: <a href="https://krillion.io/" rel="noopener nofollow">krillion.io</a>.</p>
</footer>
</main>
%(scripts)s
</body>
</html>
""" % dict(
        title=html.escape(title), desc=html.escape(desc), url=url, name=NAME,
        ld=ld, extra=extra_head, body_class=body_class, nav=nav_html(slug),
        crumb=crumb(title) if slug else "", h1=h1, lede=lede, body=body, faq=faq_html,
        disclaimer=DISCLAIMER, date=DATE, scripts=""
    )
    path = os.path.join(slug, "index.html") if slug else "index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True) if slug else None
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)


def split_lede(body):
    first, rest = body.split("</p>", 1)
    return first + "</p>", rest


def card(href, h, p):
    return '<div class="card"><h3><a href="%s">%s</a></h3><p>%s</p></div>' % (href, h, p)


def tier_table():
    blurbs = {
        "Plankton": "The answer almost everyone blurts out first.",
        "Too Clever": "The famous “obscure” pick that lots of players still reach for.",
        "Schooler": "A solid, mid-common answer.",
        "Rare": "Genuinely less common, but still findable.",
        "Deep Cut": "A deeper answer few players name.",
        "One in a Krillion": "The designated gem for that prompt — the deepest single answer.",
    }
    rows = "".join(
        "<tr><td><b>%s</b></td><td>+%d</td><td>%s m</td><td>%s</td></tr>"
        % (n, p, format(p * 10, ","), blurbs[n])
        for n, p in zip(TIER_NAMES, TIER_POINTS)
    )
    return ("<table><tr><th>Tier</th><th>Points</th><th>Depth added</th><th>What it means</th></tr>"
            + rows + "</table>")


def source_note():
    return (
        '<p class="small"><b>Sources checked %s:</b> the official game at '
        '<a href="https://krillion.io/" rel="noopener nofollow">krillion.io</a> (home screen: '
        '“7 prompts · 25 seconds each · rarer answers sink deeper”) and the official '
        '<a href="https://krillion.io/faq" rel="noopener nofollow">FAQ</a> (answer-set curation, '
        'rarity method, “Too Clever”, solo developer). Tier names and point values are as shown in the '
        'game’s how-to-play screen and reproduced by several player guides in October–November 2026; '
        'the live client is authoritative if values change. We are not affiliated with the game.</p>'
    ) % DATE


# ---------------------------------------------------------------- home
home_body = """
<p class="lede">Krillion is a free daily trivia game played in the browser. Every day gives everyone the same seven open-answer prompts, about 25 seconds per prompt, and one rule that flips normal trivia on its head: the less obvious your valid answer, the deeper your submarine sinks.</p>

<p><a class="button" href="/practice/">Play the free practice dive</a> <a class="button ghost" href="https://krillion.io/" rel="noopener nofollow">Official game ↗</a></p>

<div class="note"><b>Play the real game at <a href="https://krillion.io/" rel="noopener nofollow">krillion.io</a>.</b> This page is an independent guide. The official site is the only place that hosts the official Daily Dive, its prompts, its answers and its scoring.</div>

<h2>Krillion at a glance</h2>
<table>
<tr><th>What</th><th>Details</th></tr>
<tr><td>Game</td><td>Krillion — a daily rare-answer trivia dive</td></tr>
<tr><td>Where</td><td>Browser at krillion.io; no download or account needed for the core game</td></tr>
<tr><td>Maker</td><td>A solo developer who signs the official FAQ as “kp”</td></tr>
<tr><td>Daily format</td><td>7 prompts, same for everyone, about 25 seconds per answer</td></tr>
<tr><td>Scoring</td><td>Six rarity tiers, 10–100 points each; 1 point = 10 m of depth</td></tr>
<tr><td>Maximum</td><td>700 points = 7,000 m, the trench floor</td></tr>
<tr><td>Cost</td><td>Free daily dive; the site also sells optional unlocks and shows ads</td></tr>
<tr><td>Daily reset</td><td>A new dive each day; player guides report 00:00 UTC (the in-game timer wins)</td></tr>
</table>

<h2>How a dive works</h2>
<ol>
<li><b>Open the Daily Dive.</b> Seven prompts appear in the same order for every player worldwide.</li>
<li><b>Type one answer per prompt.</b> There are no multiple-choice buttons — you produce the answer yourself.</li>
<li><b>Beat the timer.</b> You get roughly 25 seconds per prompt. A blank or unrecognised entry scores nothing.</li>
<li><b>Read your tier and sink.</b> A valid answer lands in one of six rarity tiers; rarer tiers add more points and more depth.</li>
<li><b>Finish all seven and compare.</b> Your total depth is shareable. The Daily Dive is one scored attempt per day.</li>
</ol>

<h2>Scoring tiers</h2>
<p>The exact tier depends on the prompt: the same word can be common for one question and rare for another. These are the six values the game uses:</p>
""" + tier_table() + """
<p>Seven Plankton answers make 70 points (700 m). Seven Rare answers make 420 points (4,200 m). Seven perfect <b>One in a Krillion</b> answers make 700 points (7,000 m). That is why consistency beats gambling on one lucky answer.</p>

<div class="cta">
<h2>Practise the skill before your next dive</h2>
<p>Our free <a href="/practice/">Practice Dive</a> uses an <b>original question bank</b> written for this site: 7 prompts per round, 25 seconds each, rarity-style scoring, and a depth meter. It is a training tool — not the official game, not official prompts, and not official tiers.</p>
<p><a class="button" href="/practice/">Start a practice dive</a></p>
</div>

<h2>What makes Krillion different from other trivia games?</h2>
<div class="grid">
""" + card("/how-to-play/", "Open answers, not multiple choice", "You have to retrieve an answer from memory and spell it well enough for the validator.") + card("/strategy/", "Rarity is the score", "Being correct is only the entry ticket. The points come from naming something other players did not.") + card("/practice/", "A skill you can drill", "Three or four minutes a day is enough to train recall, category reading and time management.") + """
</div>

<h2>What Krillion is not</h2>
<ul>
<li><b>Not a quiz with one right answer.</b> Most prompts accept a large set of valid answers; the game ranks them by rarity.</li>
<li><b>Not a daily-answer archive.</b> This site does not publish today’s prompts or answers, and we do not scrape the official game.</li>
<li><b>Not the official site.</b> Several unofficial domains use the Krillion name. The game’s own FAQ points players to krillion.io; treat everything else as a fan project.</li>
</ul>

<h2>Modes beyond the Daily Dive</h2>
<p>The official site also links an <b>Unlimited</b> mode, <b>Themed packs</b>, an <b>Archive</b> of past dives and a beta party mode called <b>Puffer Party</b>. Modes and prices can change; check the official menu before you plan around them.</p>

""" + source_note()

home_faq = [
    ("What is Krillion?", "Krillion is a free browser game where everyone gets the same seven open-answer trivia prompts each day. Valid answers score by rarity, and every point moves your dive 10 metres deeper toward a 7,000-metre trench floor."),
    ("Is Krillion free?", "Yes. The Daily Dive is free to play in the browser. The official site also sells optional unlocks and shows ads, which can be removed with a purchase."),
    ("How long is a Krillion dive?", "About three to four minutes: seven prompts with roughly 25 seconds each, plus the result screens."),
    ("When does Krillion reset?", "A new dive appears each day. Player guides report the reset at 00:00 UTC; the countdown in the official client is authoritative."),
    ("Is this site the official Krillion game?", "No. This is an independent guide and practice tool. The official game lives at krillion.io and is not affiliated with us."),
    ("Does the practice tool use real Krillion prompts?", "No. Every prompt and answer in our practice dive was written for this site. Our tiers are editorial estimates, so scores are not comparable to the official game."),
    ("What is the maximum score in Krillion?", "700 points, which equals 7,000 metres: seven answers in the top 100-point tier."),
]

page("", "Krillion Game: Daily Dive Rules, Scoring & Free Practice",
     "Krillion game guide: how the daily dive works, all six scoring tiers, the 25-second timer, and a free practice dive with our own original question bank.",
     "Krillion Game: How to Play the Daily Dive",
     *split_lede(home_body),
     faqs=home_faq)


# ---------------------------------------------------------------- how to play
how_body = """
<p class="lede">This page is the full rules reference for the Krillion Daily Dive: what you type, how long you have, how the six tiers score, and how depth is calculated. It is written for players who want the mechanics straight before their first run.</p>

<h2>The 30-second version</h2>
<ol>
<li>Go to <a href="https://krillion.io/" rel="noopener nofollow">krillion.io</a> and open the Daily Dive.</li>
<li>You get seven prompts, the same for everyone that day.</li>
<li>For each prompt, type one valid answer within about 25 seconds.</li>
<li>Valid answers score 10, 15, 30, 60, 85 or 100 points by rarity.</li>
<li>Add the seven scores; multiply by 10 to get your depth in metres.</li>
</ol>

<h2>Step by step</h2>
<ol>
<li><b>Start the dive.</b> The Daily Dive is the scored daily mode. You do not need an account for the core game.</li>
<li><b>Read the prompt precisely.</b> Prompts ask for a member of a category — a country, a city, a food, a character, a work, a species. Every word in the prompt narrows the answer set.</li>
<li><b>Type one answer.</b> The validator checks your spelling against a curated answer set that includes aliases. Autocorrect is deliberately generous, so a one-letter slip can still match.</li>
<li><b>Submit before the timer.</b> If an entry is not recognised, it scores nothing and the clock keeps running. You get one scored answer per prompt.</li>
<li><b>Watch the tier reveal.</b> The game shows the accepted answer, its rarity tier and the points you earned, then moves on.</li>
<li><b>Repeat for all seven prompts.</b> The result screen shows your total depth, which you can share.</li>
</ol>

<h2>The timer</h2>
<p>Each prompt gives you roughly <b>25 seconds</b>. The game previews the next prompt briefly before the answer window opens, so you cannot bank time from one prompt to the next. Miss the window and that prompt is a zero.</p>
<p>Time management matters more than most players expect: reading the prompt carefully for three seconds and typing a clean answer beats rushing a half-remembered name and losing the prompt to a typo.</p>

<h2>Scoring: the six tiers</h2>
""" + tier_table() + """
<h3>How rarity is decided</h3>
<p>The official FAQ explains that answer sets are built by aggregating sources such as dictionaries, wiki pages and encyclopedias, then merging and cleaning them. Rarity is not one universal formula: some prompts are scored mechanically against a database of how often a word appears in what people read and write; others use a combination of LLM assistance and a manual pass.</p>
<p>Two consequences follow. First, a tier belongs to an answer <i>within a prompt</i>, not to the word forever. Second, the top “One in a Krillion” answer is chosen partly for rarity and partly because it is satisfying to land on — it is a curated gem, not a pure frequency measure.</p>

<h3>Depth maths</h3>
<table>
<tr><th>Run</th><th>Points</th><th>Depth</th></tr>
<tr><td>Seven Plankton answers</td><td>70</td><td>700 m</td></tr>
<tr><td>Seven Schooler answers</td><td>210</td><td>2,100 m</td></tr>
<tr><td>Seven Rare answers</td><td>420</td><td>4,200 m</td></tr>
<tr><td>Six Rare + one Krillion</td><td>460</td><td>4,600 m</td></tr>
<tr><td>Seven One in a Krillion answers</td><td>700</td><td>7,000 m (trench floor)</td></tr>
</table>

<h2>What counts as a valid answer?</h2>
<ul>
<li><b>It must fit the category as written.</b> A country that starts with S is not any country beginning with “Saint” unless the prompt allows it; read the qualifier.</li>
<li><b>Aliases count.</b> The validator checks alternate names, so “T. rex” and “Tyrannosaurus rex” can both match if the prompt is about dinosaurs.</li>
<li><b>Spelling is forgiving, not infinite.</b> A letter or two off an alias can still match — sometimes producing a funny mismatch. Aim for a clean spelling of a name you know.</li>
<li><b>Blank, invalid or unrecognised entries score zero.</b> There is no partial credit for a miss.</li>
</ul>

<h2>Daily reset and other modes</h2>
<p>A new Daily Dive appears each day. Player guides report the reset at <b>00:00 UTC</b>; the in-game countdown is the authority. Beyond the daily, the official menu links an Unlimited mode, themed packs, an archive and the beta Puffer Party mode. Themed packs are useful for practice because they repeat categories you can study; they do not replace the scored daily.</p>

<h2>Five mistakes that cost depth</h2>
<ol>
<li><b>Typing your first thought.</b> The first answer that comes to mind is usually Plankton. Pause and generate two more candidates.</li>
<li><b>Chasing “clever” instead of rare.</b> The Too Clever tier exists precisely because the famous obscure pick is still common.</li>
<li><b>Ignoring a qualifier.</b> “A country in Africa” and “a country that starts with S” have different answer sets; mixing them costs the prompt.</li>
<li><b>Burning the clock on spelling.</b> If you cannot spell it confidently, pick a slightly more common answer you can type cleanly.</li>
<li><b>Treating one bad dive as a trend.</b> Seven prompts is a tiny sample; review your misses across several days before changing strategy.</li>
</ol>

<h2>Practice the mechanics</h2>
<p>Our <a href="/practice/">Practice Dive</a> uses the same shape — seven prompts, 25 seconds, six rarity tiers, a 7,000 m depth meter — but an original question bank and our own tier estimates. Use it to drill category reading and time management; use the official game for the real scored attempt.</p>

""" + source_note()

how_faq = [
    ("How many prompts are in a Krillion dive?", "Seven prompts, the same for every player on that day."),
    ("How long do you get per prompt?", "About 25 seconds per prompt. The game previews each prompt before the answer window opens."),
    ("How many points is a perfect Krillion dive?", "700 points: seven answers in the 100-point One in a Krillion tier, equal to 7,000 metres."),
    ("Can you retry a prompt in Krillion?", "You get one scored answer per prompt. Unrecognised entries score nothing and the timer keeps running; the official client decides whether you can retype before time expires."),
    ("Does Krillion require an account?", "No for the core Daily Dive. An account is used for purchases and syncing unlocks."),
    ("Is Krillion the same as a clone site?", "No. The official game is at krillion.io. Several unofficial domains reuse the name; the official FAQ is the authority on rules and scoring."),
]

page("how-to-play", "How to Play Krillion: Rules, Timer & Scoring (2026)",
     "Full Krillion rules: seven prompts, 25 seconds each, six rarity tiers from 10 to 100 points, 1 point = 10 m, and how the official answer validator works.",
     "How to Play Krillion: Rules, Timer and Scoring",
     *split_lede(how_body),
     faqs=how_faq)


# ---------------------------------------------------------------- strategy
strategy_body = """
<p class="lede">Krillion rewards a specific skill: producing a valid answer that is less obvious than everyone else’s first thought. These are the habits that reliably add depth, plus the traps that quietly cost points. Every example below comes from our own practice bank, not from a real Krillion dive.</p>

<h2>The maths that should guide you</h2>
<p>Seven average answers beat one brilliant answer and six blanks. Rare answers score 60 points; Plankton scores 10. A player who lands seven Rare answers finishes at 420 points (4,200 m). A player who gambles for the 100-point gem and misses three prompts finishes at 400 points at best. <b>Your floor matters as much as your ceiling.</b></p>

<h2>1. Read the prompt as a constraint, not a topic</h2>
<p>“Name a country that starts with S” is not “name a country”. The letter is the whole puzzle. Underline the qualifier in your head: a starting letter, a region, a time period, a medium. Then generate answers that satisfy every part.</p>
<p><b>Drill:</b> take a prompt and say the constraints out loud before you think of an answer.</p>

<h2>2. Generate three candidates before you type</h2>
<p>The first answer you think of is usually the most common one — that is what makes it first. Spend three seconds listing two more valid candidates, then choose the least obvious one you can spell. This single habit moves most players from Plankton toward Schooler and Rare.</p>
<div class="card"><p><b>Example (our bank):</b> “Name a pizza topping.” First thought: pepperoni (common). Second: mushroom (common). Third: artichoke (much rarer). Choose the third if you are confident it is valid.</p></div>

<h2>3. Step sideways within the category</h2>
<p>Obvious answers cluster around the same subcategories. If a prompt asks for a movie with a heist, most players name Hollywood blockbusters. Step sideways: older films, non-English films, documentaries, animated films. The category stays valid; the answer becomes less crowded.</p>

<h2>4. Watch for the Too Clever trap</h2>
<p>Too Clever is a real tier, and it is worth only 15 points — five more than Plankton. It catches the “famous obscure” answer: the pick that feels like a deep cut because it is quirky, but that thousands of other players also reach for. If your answer is a well-known piece of trivia, it is probably Too Clever, not Deep Cut.</p>
<p>Ask yourself: “Would this answer appear in a listicle called ‘obscure facts about X’?” If yes, keep looking.</p>

<h2>5. Specificity is not the same as obscurity</h2>
<p>A specific answer is only deeper if it is still valid and less commonly named. Naming a tiny village when the prompt asks for a city can fail the validator; naming a mid-sized city that fits the prompt exactly can score well. Precision beats weirdness.</p>

<h2>6. Protect your 25 seconds</h2>
<p>A practical split: <b>4 seconds</b> reading and checking the qualifier, <b>9 seconds</b> generating two or three candidates, <b>8 seconds</b> typing and checking the spelling, <b>4 seconds</b> buffer to submit. The buffer matters: a great answer submitted after the timer is worth zero.</p>

<h2>7. Spelling discipline</h2>
<p>The validator is generous with aliases, but a name you cannot spell is a risk you do not need. Prefer an answer you can type cleanly over a marginally rarer one you will mangle. On a phone, autocorrect can help or hurt; check the word before you submit.</p>

<h2>8. Build a personal depth list</h2>
<p>After each dive, note the prompts where you scored Plankton or missed. For each, write two less obvious valid answers you could have used. Ten minutes of review beats another ten random dives, because you are training recall for categories that actually appear.</p>

<h2>9. Practise with a timer</h2>
<p>Untimed practice builds knowledge; timed practice builds the skill the game actually scores. Our <a href="/practice/">Practice Dive</a> gives you seven prompts and 25 seconds each, with an original answer bank. Use it for one focused round a day: pick a single rule (three candidates, or sideways subcategories) and apply it to every prompt.</p>

<h2>10. Review the distribution, not just the total</h2>
<p>A 350-point run built from seven Schooler answers is a more stable strategy than a 350-point run with one 100-point gem and three zeros. Over a month, the stable distribution wins. Track how many prompts you leave blank — that number is the easiest one to fix.</p>

""" + source_note()

strategy_faq = [
    ("What is the best strategy for Krillion?", "Generate two or three valid answers before typing, choose the least obvious one you can spell, and never leave a prompt blank. Consistency across seven prompts beats chasing one rare answer."),
    ("What is the Too Clever tier?", "A 15-point tier for the famous ‘obscure’ answer that many players still name. It is only five points above Plankton, so it is a trap rather than a win."),
    ("Should I guess in Krillion?", "No. An invalid guess scores zero, and the timer keeps running. If you are unsure, name a valid answer you can spell rather than a risky one."),
    ("Does the practice tool use official Krillion prompts?", "No. Our practice prompts and answer lists are original, and our tiers are estimates. Use the official game for scored attempts."),
]

page("strategy", "Krillion Strategy: How to Find Rarer Answers",
     "Practical Krillion strategy: generate multiple candidates, avoid the Too Clever trap, manage the 25-second timer, and train recall with a daily practice drill.",
     "Krillion Strategy: How to Find Rarer Answers",
     *split_lede(strategy_body),
     faqs=strategy_faq)


# ---------------------------------------------------------------- practice
practice_body = """
<p class="lede">A free training dive in the shape of Krillion: seven prompts, 25 seconds per prompt, six rarity tiers and a 7,000-metre depth meter. The question bank is written for this site, and the tiers are our own estimates — this is a practice tool, not the official game.</p>

<section class="dive" id="dive" aria-label="Krillion practice dive">
  <div class="dive-top">
    <span class="badge">Practice dive</span>
    <span id="promptNo">Ready</span>
  </div>
  <div class="depth" aria-hidden="true"><div class="fill" id="depthFill"></div><div class="label" id="depthLabel">0 m / 7,000 m</div></div>

  <div id="startPane">
    <p>7 prompts · 25 seconds each · original question bank · runs entirely in your browser.</p>
    <p class="small">Tip: say two or three valid answers in your head before you type. The first one is usually Plankton.</p>
    <button id="startBtn" type="button">Start practice dive</button>
  </div>

  <div id="playPane" hidden>
    <p class="cat" id="cat"></p>
    <h2 id="promptText"></h2>
    <form id="answerForm" autocomplete="off">
      <label class="sr-only" for="answerInput">Your answer</label>
      <input id="answerInput" name="answer" maxlength="60" placeholder="Type one answer…" autocapitalize="off" spellcheck="false">
      <button id="submitBtn" type="submit">Submit</button>
    </form>
    <div class="timer" aria-hidden="true"><div class="fill" id="timerFill"></div></div>
    <p id="timerText">25.0s</p>
    <div id="feedback" role="status" aria-live="polite"></div>
  </div>

  <div id="endPane" hidden>
    <p class="result-big" id="resultScore">0 / 700 pts</p>
    <p class="result-sub" id="resultDepth">Depth reached: 0 m</p>
    <p id="resultDetail"></p>
    <div class="tierlist" id="tierList"></div>
    <p><button id="againBtn" type="button">Play another dive</button> <button id="shareBtn" type="button" class="ghost">Copy result</button></p>
  </div>
</section>

<h2>How this practice tool works</h2>
<ul>
<li><b>Seven prompts per round</b>, drawn from a bank of 20 categories written for this site.</li>
<li><b>25 seconds per prompt.</b> Type an answer and submit. Our validator checks a curated answer list with aliases and tolerates a one-letter typo on longer words.</li>
<li><b>Six tiers, same point values as the official game</b> (10/15/30/60/85/100). They are assigned by our own editorial judgement of how obvious each answer is — they are <b>not</b> Krillion’s real tiers and cannot be compared with official scores.</li>
<li><b>Depth</b> is points × 10. Seven top-tier answers make 7,000 m.</li>
<li><b>Nothing leaves your browser.</b> There are no accounts, no cookies and no network calls; your best score is stored in localStorage only.</li>
</ul>

<h2>Why the answer bank is small</h2>
<p>The official game validates tens of thousands of possible answers per prompt. Our bank recognises roughly 20–22 answers per prompt, so a perfectly valid answer can be missing. When that happens, the tool says so and lets you try another answer before the timer expires. Treat the bank as a drill, not as a dictionary.</p>

<h2>What this tool will not do</h2>
<ul>
<li>It does not show today’s official prompts, answers or results.</li>
<li>It does not copy, embed or mirror krillion.io.</li>
<li>It does not claim to predict your official score. Use it to practise recall, category reading and the 25-second rhythm.</li>
</ul>

<h2>Ready for the real thing?</h2>
<p>Play the official Daily Dive at <a href="https://krillion.io/" rel="noopener nofollow">krillion.io</a>. If you want the rules first, read <a href="/how-to-play/">how scoring works</a>; if you want tactics, read the <a href="/strategy/">strategy guide</a>.</p>
"""

page("practice", "Krillion Practice Dive: Free 7-Prompt Training Game",
     "Play a free Krillion-style practice dive: seven prompts, 25 seconds each, rarity tiers and a depth meter. Original question bank, no sign-up, runs in your browser.",
     "Krillion Practice Dive",
     *split_lede(practice_body),
     app=True,
     extra_head='<script src="/data.js?v=20261104c" defer></script>\n<script src="/practice.js?v=20261104c" defer></script>')


# ---------------------------------------------------------------- about
about_body = """
<p class="lede">Krillion Game Guide is an independent fan project: a plain-language rules reference, a strategy guide and a free practice tool for a daily browser game we enjoy. It is not the official game and has no connection to its developer.</p>

<h2>Who runs this site</h2>
<p>This site is built and maintained by an independent developer as part of a small collection of free browser tools. We do not publish a personal name or a biography because there is no public author brand behind the site; the work is the site itself. If that changes, this page will say so.</p>

<h2>Editorial policy</h2>
<ul>
<li><b>Facts carry sources.</b> Rules, modes and scoring statements are checked against the official game at krillion.io and its FAQ, with the check date shown on the page.</li>
<li><b>Estimates are labelled.</b> Our practice tiers are editorial estimates and are marked as such everywhere they appear.</li>
<li><b>No daily answers.</b> We do not publish today’s prompts, answers or results, and we do not scrape the official game.</li>
<li><b>Corrections.</b> If a rule or value changes, the official client wins; we update the page rather than defend an old claim.</li>
<li><b>No fake credentials.</b> We do not claim to be the developer, an official partner or a professional trivia organisation.</li>
</ul>

<h2>What the practice tool is</h2>
<p>The practice dive is our own implementation: an original question bank, a client-side validator, and a scoring model that mirrors the official tier values for training purposes. It runs entirely in your browser. It is not a clone of the official game, does not use its prompts or answer data, and does not reproduce its artwork or interface.</p>

<h2>Intellectual property</h2>
<p>“Krillion” and the official game belong to their developer. We use the name only to describe and discuss the game, with a clear non-affiliation notice on every page. We do not host, embed or redistribute the official game or its assets. If the owner has a concern about this fan site, we will respond and change or remove material as appropriate.</p>

<h2>What we do not do</h2>
<ul>
<li>We do not sell anything, run ads or collect accounts.</li>
<li>We do not publish “daily answer” lists or spoilers.</li>
<li>We do not mirror other fan sites’ content.</li>
</ul>

<h2>Privacy</h2>
<p>See the <a href="/privacy/">privacy page</a>: no analytics, no cookies, no account, and only local browser storage for your practice best score.</p>
"""

page("about", "About Krillion Game Guide — Independent Fan Site",
     "About Krillion Game Guide: an independent fan project with a rules reference, strategy guide and original practice tool. Not affiliated with krillion.io.",
     "About Krillion Game Guide",
     *split_lede(about_body))


# ---------------------------------------------------------------- privacy
privacy_body = """
<p class="lede">This page explains what data this website does and does not handle. The short version: no accounts, no analytics, no advertising scripts and no cookies set by us.</p>

<h2>What we collect</h2>
<p><b>Nothing that identifies you.</b> We do not run analytics, advertising pixels, social embeds or third-party scripts. There is no contact form, newsletter or login.</p>

<h2>Local storage</h2>
<p>The practice tool stores one value in your browser’s <code>localStorage</code>: your best practice score. It never leaves your device and is not transmitted to us. Clearing your browser storage deletes it.</p>

<h2>Server logs</h2>
<p>The site is served by Vercel, a static hosting provider. Like any web server, Vercel may process standard request data (IP address, user agent, requested URL, timestamp) to deliver the site and protect it from abuse. We do not receive or analyse that data in this project. See Vercel’s privacy policy for details.</p>

<h2>External links</h2>
<p>Pages link to the official game at krillion.io. Once you follow an external link, that site’s privacy policy applies. We do not control it.</p>

<h2>Children</h2>
<p>The site is a general-audience guide and does not knowingly collect personal information from anyone, including children.</p>

<h2>Changes</h2>
<p>If this site ever adds analytics or another data-processing feature, this page will be updated first and the change date below will move.</p>

<p class="small">Last updated: 2026-11-04.</p>
"""

page("privacy", "Privacy Policy — Krillion Game Guide",
     "Krillion Game Guide privacy policy: no analytics, no cookies, no accounts. Only a local best-score value is stored in your browser.",
     "Privacy Policy",
     *split_lede(privacy_body))


# ---------------------------------------------------------------- data.js
def build_data():
    prompts = []
    for p in PROMPTS:
        answers = []
        for i, raw in enumerate(p["answers"]):
            main = raw.split("|")[0]
            aliases = [a.strip() for a in raw.split("|")]
            answers.append({"a": aliases, "t": tier_for(p["id"], main, i) - 1})
        prompts.append({"id": p["id"], "cat": p["cat"], "q": p["q"], "answers": answers})
    data = {"prompts": prompts, "tiers": TIER_NAMES, "points": TIER_POINTS}
    with open("data.js", "w", encoding="utf-8") as f:
        f.write("window.KR_PRACTICE=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")


build_data()

# ---------------------------------------------------------------- sitemap / robots / config
slugs = ["", "practice", "how-to-play", "strategy", "about", "privacy"]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for s in slugs:
    sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (url_for(s), DATE))
sm.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(sm) + "\n")
open("robots.txt", "w", encoding="utf-8").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE)

vercel = {
    "framework": None,
    "buildCommand": None,
    "installCommand": None,
    "outputDirectory": ".",
    "cleanUrls": True,
    "headers": [{
        "source": "/(.*)",
        "headers": [
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            {"key": "Content-Security-Policy",
             "value": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"}
        ]
    }]
}
open("vercel.json", "w", encoding="utf-8").write(json.dumps(vercel, indent=2) + "\n")
vi = ["*", "!index.html", "!style.css", "!practice.js", "!data.js", "!icon.svg",
      "!robots.txt", "!sitemap.xml", "!vercel.json"]
for s in ["practice", "how-to-play", "strategy", "about", "privacy"]:
    vi += ["!" + s, "!" + s + "/", "!" + s + "/**"]
open(".vercelignore", "w", encoding="utf-8").write("\n".join(vi) + "\n")
open(".gitignore", "w", encoding="utf-8").write("__pycache__/\n.DS_Store\n.vercel/\n")

print("built:", len(slugs), "pages,", len(PROMPTS), "practice prompts")
