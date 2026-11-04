# -*- coding: utf-8 -*-
"""Original practice prompt bank for the Krillion fan practice tool.

Every prompt and answer list here was written for this site. Nothing is copied
from krillion.io or from any daily Krillion dive. Tiers are our own editorial
estimates of how obvious an answer is; they are not official Krillion tiers.
"""

# Each answer: "main answer|alias|alias". Order = roughly most obvious first.
PROMPTS = [
    dict(id="country-s", cat="Geography", q="Name a country that starts with the letter S",
         answers=["Spain", "Sweden", "Switzerland", "South Africa", "Saudi Arabia", "Singapore",
                  "South Korea", "Sudan", "Syria", "Senegal", "Serbia", "Slovakia", "Slovenia",
                  "Somalia", "Sri Lanka", "Suriname", "Samoa", "Sierra Leone", "South Sudan",
                  "Solomon Islands", "Saint Lucia", "Eswatini|Swaziland"]),
    dict(id="pizza", cat="Food", q="Name a pizza topping",
         answers=["Pepperoni", "Cheese|mozzarella", "Mushroom", "Onion", "Ham", "Sausage",
                  "Bacon", "Pineapple", "Olives", "Bell pepper|capsicum", "Jalapeno|jalapeño",
                  "Anchovies", "Spinach", "Chicken", "BBQ sauce|barbecue sauce", "Prosciutto",
                  "Artichoke", "Truffle", "Eggplant|aubergine", "Pesto", "Feta", "Sweetcorn|corn"]),
    dict(id="board-game", cat="Games", q="Name a board game",
         answers=["Monopoly", "Scrabble", "Chess", "Clue|Cluedo", "Risk", "Catan|Settlers of Catan",
                  "Ticket to Ride", "Sorry", "Candy Land", "Pandemic", "Carcassonne", "Splendor",
                  "Dominion", "Backgammon", "Go", "Azul", "Terraforming Mars", "Wingspan",
                  "Gloomhaven", "Twilight Struggle", "Diplomacy", "Checkers|draughts"]),
    dict(id="heist-movie", cat="Movies", q="Name a movie that features a heist",
         answers=["Ocean's Eleven|Oceans Eleven", "Inception", "Heat", "The Italian Job",
                  "Reservoir Dogs", "Mission: Impossible|Mission Impossible", "Die Hard",
                  "Fast Five", "Baby Driver", "The Town", "Inside Man", "Snatch",
                  "Point Break", "Gone in 60 Seconds", "Rififi", "The Score",
                  "Logan Lucky", "Widows", "Sexy Beast", "The Sting", "Dog Day Afternoon",
                  "Sneakers"]),
    dict(id="japan-city", cat="Geography", q="Name a city in Japan",
         answers=["Tokyo", "Osaka", "Kyoto", "Hiroshima", "Nagoya", "Sapporo", "Fukuoka",
                  "Kobe", "Yokohama", "Nara", "Sendai", "Kanazawa", "Nagasaki", "Naha",
                  "Matsumoto", "Hakodate", "Kagoshima", "Okayama", "Kumamoto", "Nikko",
                  "Toyama", "Aomori"]),
    dict(id="pasta", cat="Food", q="Name a type of pasta",
         answers=["Spaghetti", "Penne", "Macaroni", "Lasagna|lasagne", "Fusilli", "Rigatoni",
                  "Ravioli", "Linguine", "Fettuccine", "Gnocchi", "Tortellini", "Farfalle",
                  "Angel hair|capellini", "Ziti", "Cannelloni", "Tagliatelle", "Orzo",
                  "Bucatini", "Orecchiette", "Pappardelle", "Conchiglie|shells", "Vermicelli"]),
    dict(id="ocean-animal", cat="Nature", q="Name an animal that lives in the ocean",
         answers=["Shark", "Whale", "Dolphin", "Octopus", "Jellyfish", "Crab", "Sea turtle",
                  "Lobster", "Clownfish", "Blue whale", "Orca|killer whale", "Squid", "Eel",
                  "Seahorse", "Stingray", "Manatee", "Walrus", "Narwhal", "Anglerfish",
                  "Giant squid", "Sea otter", "Starfish|sea star"]),
    dict(id="shakespeare", cat="Books", q="Name a Shakespeare play",
         answers=["Hamlet", "Romeo and Juliet", "Macbeth", "Othello", "King Lear",
                  "A Midsummer Night's Dream", "The Tempest", "Julius Caesar",
                  "The Merchant of Venice", "Much Ado About Nothing", "Twelfth Night",
                  "Richard III", "Henry V", "The Taming of the Shrew", "Antony and Cleopatra",
                  "As You Like It", "Measure for Measure", "Titus Andronicus", "Coriolanus",
                  "Cymbeline", "The Comedy of Errors", "King John"]),
    dict(id="element", cat="Science", q="Name a chemical element",
         answers=["Oxygen", "Carbon", "Hydrogen", "Gold", "Silver", "Iron", "Helium", "Nitrogen",
                  "Sodium", "Calcium", "Uranium", "Neon", "Copper", "Lead", "Mercury",
                  "Titanium", "Zinc", "Potassium", "Argon", "Plutonium", "Sulfur|sulphur",
                  "Magnesium"]),
    dict(id="beatles", cat="Music", q="Name a Beatles song",
         answers=["Hey Jude", "Let It Be", "Yesterday", "Come Together", "Here Comes the Sun",
                  "A Hard Day's Night", "Help!", "Yellow Submarine", "Penny Lane",
                  "Eleanor Rigby", "All You Need Is Love", "Something", "Blackbird",
                  "Norwegian Wood", "Strawberry Fields Forever", "Revolution",
                  "Lucy in the Sky with Diamonds", "While My Guitar Gently Weeps",
                  "Golden Slumbers", "Octopus's Garden", "Day Tripper", "Ticket to Ride"]),
    dict(id="detective", cat="Fiction", q="Name a fictional detective",
         answers=["Sherlock Holmes", "Hercule Poirot", "Miss Marple", "Nancy Drew", "Batman",
                  "Inspector Gadget", "Columbo", "Jessica Fletcher", "Philip Marlowe",
                  "Sam Spade", "Benoit Blanc", "Inspector Morse", "Father Brown",
                  "Kurt Wallander", "Lisbeth Salander", "Precious Ramotswe", "Vera Stanhope",
                  "Harry Hole", "Auguste Dupin", "Easy Rawlins", "Dirk Gently", "Enola Holmes"]),
    dict(id="africa-country", cat="Geography", q="Name a country in Africa",
         answers=["Egypt", "South Africa", "Nigeria", "Kenya", "Morocco", "Ethiopia", "Ghana",
                  "Algeria", "Tunisia", "Tanzania", "Uganda", "Senegal", "Zimbabwe", "Namibia",
                  "Botswana", "Rwanda", "Madagascar", "Mozambique", "Cameroon", "Chad",
                  "Mali", "Angola"]),
    dict(id="retro-game", cat="Games", q="Name a video game released before 2000",
         answers=["Super Mario Bros.", "Tetris", "Pac-Man", "Doom", "Sonic the Hedgehog",
                  "The Legend of Zelda", "Final Fantasy VII", "Street Fighter II",
                  "Pokemon Red and Blue|Pokémon Red and Blue", "Half-Life", "StarCraft",
                  "The Legend of Zelda: Ocarina of Time|Ocarina of Time", "Age of Empires",
                  "Metal Gear Solid", "Crash Bandicoot", "Civilization II", "Myst",
                  "System Shock 2", "Planescape: Torment", "Chrono Trigger",
                  "Super Metroid", "GoldenEye 007"]),
    dict(id="state-capital", cat="Geography", q="Name a US state capital",
         answers=["Phoenix", "Sacramento", "Austin", "Boston", "Denver", "Atlanta", "Albany",
                  "Springfield", "Columbus", "Tallahassee", "Annapolis", "Harrisburg",
                  "Olympia", "Juneau", "Cheyenne", "Boise", "Bismarck", "Lansing",
                  "Montpelier", "Pierre", "Santa Fe", "Nashville"]),
    dict(id="prehistoric", cat="Nature", q="Name a prehistoric creature",
         answers=["Tyrannosaurus rex|T. rex|T-rex", "Triceratops", "Velociraptor",
                  "Stegosaurus", "Brachiosaurus", "Diplodocus", "Ankylosaurus", "Spinosaurus",
                  "Allosaurus", "Pterodactyl|pterosaur", "Brontosaurus", "Parasaurolophus",
                  "Iguanodon", "Carnotaurus", "Deinonychus", "Archaeopteryx",
                  "Giganotosaurus", "Maiasaura", "Utahraptor", "Therizinosaurus",
                  "Megalodon", "Woolly mammoth|mammoth"]),
    dict(id="language", cat="Technology", q="Name a programming language",
         answers=["Python", "Java", "JavaScript", "C++", "C", "Ruby", "PHP", "Swift", "Go",
                  "TypeScript", "C#", "SQL", "Kotlin", "Rust", "Perl", "Fortran", "COBOL",
                  "Scala", "Haskell", "Lisp", "R", "Lua"]),
    dict(id="superhero", cat="Fiction", q="Name a superhero",
         answers=["Superman", "Batman", "Spider-Man", "Wonder Woman", "Iron Man",
                  "Captain America", "Thor", "Hulk|The Hulk", "Flash|The Flash", "Aquaman",
                  "Wolverine", "Black Panther", "Green Lantern", "Doctor Strange",
                  "Daredevil", "Nightcrawler", "Blue Beetle", "Squirrel Girl",
                  "Static Shock", "The Tick", "Storm", "Supergirl"]),
    dict(id="cheese", cat="Food", q="Name a type of cheese",
         answers=["Cheddar", "Mozzarella", "Parmesan", "Brie", "Gouda", "Swiss", "Feta",
                  "Blue cheese", "Camembert", "Ricotta", "Goat cheese|chevre|chèvre",
                  "Provolone", "Manchego", "Gruyere|gruyère", "Roquefort", "Halloumi",
                  "Burrata", "Gorgonzola", "Pecorino", "Comte|comté", "Stilton", "Mascarpone"]),
    dict(id="olympic", cat="Sports", q="Name an Olympic sport",
         answers=["Swimming", "Athletics|track and field", "Gymnastics", "Football|soccer",
                  "Basketball", "Tennis", "Cycling", "Boxing", "Rowing", "Volleyball",
                  "Wrestling", "Table tennis", "Fencing", "Archery", "Judo", "Handball",
                  "Badminton", "Sailing", "Equestrian", "Skateboarding", "Surfing",
                  "Weightlifting"]),
    dict(id="scientist", cat="Science", q="Name a famous scientist",
         answers=["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin",
                  "Nikola Tesla", "Galileo Galilei", "Stephen Hawking", "Alan Turing",
                  "Louis Pasteur", "Ada Lovelace", "Gregor Mendel", "Niels Bohr",
                  "Richard Feynman", "Rosalind Franklin", "Katherine Johnson",
                  "Carl Linnaeus", "Michael Faraday", "Emmy Noether", "Chien-Shiung Wu",
                  "Abdus Salam", "James Clerk Maxwell", "Ibn al-Haytham"]),
]

# Answers that fit the "Too Clever" idea: the famous 'obscure' pick that a lot of
# players reach for. Normalised lowercase, compared against the main answer only.
CLEVER = {
    "pizza": "pineapple",
    "board-game": "azul",
    "heist-movie": "rififi",
    "detective": "batman",
    "prehistoric": "brontosaurus",
    "language": "haskell",
    "superhero": "squirrel girl",
    "olympic": "skateboarding",
}

TIER_NAMES = ["Plankton", "Too Clever", "Schooler", "Rare", "Deep Cut", "One in a Krillion"]
TIER_POINTS = [10, 15, 30, 60, 85, 100]


def tier_for(prompt_id, main_answer, index):
    clever = CLEVER.get(prompt_id)
    if clever and main_answer.lower() == clever:
        return 2
    if index < 3:
        return 1
    if index < 8:
        return 3
    if index < 13:
        return 4
    if index < 19:
        return 5
    return 6
