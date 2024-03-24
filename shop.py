import math

# UPDATES TO THIS REQUIRE A BOT RESTART ATM

SHOP = {
    "optimized_bait": {
        "price": [
            (lambda x : 10 * math.floor(25.6 * x + 6.4)),
            (lambda x : x // 10)
        ],
        "item_name": [
            "FishCoin",
            "Glistening Coin"
        ],
        "item_path": [
            "money",
            ["items","Glistening Coin"]
        ],
        "description": "Gain 0.2 more bait every hour!",
        "limit": -1
    },
    "estrogen": {
        "price": [
            (lambda x : 1)
        ],
        "item_name": [
            "FishCoin"
        ],
        "item_path": [
            "money"
        ],
        "description": "#girl",
        "limit": -1
    },
    "difficult_bait": {
        "price": [
            (lambda x : 30 * x + 10),
            (lambda x : 30 * x + 10),
            (lambda x : 30 * x + 10),
            (lambda x : 30 * x + 10),
            (lambda x : 3 * x + 2)
        ],
        "item_name": [
            "Minnow",
            "Halibut",
            "Smelt",
            "Milkfish",
            "Seaweed"
        ],
        "item_path": [
            ["fish","Minnow","amount"],
            ["fish","Halibut","amount"],
            ["fish","Smelt","amount"],
            ["fish","Milkfish","amount"],
            ["items","Seaweed","amount"]
        ],
        "description": "Increases the effectiveness of your bait on Salmon, Crabs, Sea Nettles, and Sardines.",
        "limit": 2
    },
    "challenging_bait": {
        "price": [
            (lambda x : 30 * x + 10),
            (lambda x : 30 * x + 10),
            (lambda x : 30 * x + 10),
            (lambda x : 30 * x + 10),
            (lambda x : 5 * x + 5)
        ],
        "item_name": [
            "Salmon",
            "Crab",
            "Sea Nettle",
            "Sardine",
            "Seaweed"
        ],
        "item_path": [
            ["fish","Salmon","amount"],
            ["fish","Crab","amount"],
            ["fish","Sea Nettle","amount"],
            ["fish","Sardine","amount"],
            ["items","Seaweed","amount"]
        ],
        "description": "Increases the effectiveness of your bait on Squid and Rockfish.",
        "limit": 2
    },
    "legendary_bait": {
        "price": [
            (lambda x : 30 * x + 10),
            (lambda x : 30 * x + 10),
            (lambda x : 10 * x + 10)
        ],
        "item_name": [
            "Squid",
            "Rockfish",
            "Seaweed"
        ],
        "item_path": [
            ["fish","Squid","amount"],
            ["fish","Rockfish","amount"],
            ["items","Seaweed","amount"]
        ],
        "description": "Increases the effectiveness of your bait on Swordfish.",
        "limit": 2
    },
    "special_bait": {
        "price": [
            (lambda x : 30 * x + 10),
            (lambda x : 20 * x + 20)
        ],
        "item_name": [
            "Swordfish",
            "Seaweed"
        ],
        "item_path": [
            ["fish","Swordfish","amount"],
            ["items","Seaweed","amount"]
        ],
        "description": "Increases the chance to catch... something?",
        "limit": 2
    }
}