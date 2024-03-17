# main imports
import os

# local imports
import botstate

LOC = os.path.split(os.path.realpath(__file__))[0]


def is_mod(ctx) -> bool:
    if ctx.author.id in botstate.get_key("trusted"):
        return True
    return False