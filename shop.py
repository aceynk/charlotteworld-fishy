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
        "description": "Gain 0.2 more bait every hour!"
    }
}