# main imports

# local imports
import botstate


def is_mod(ctx) -> bool:
    if ctx.author.id in botstate.get_key("trusted"):
        return True
    return False