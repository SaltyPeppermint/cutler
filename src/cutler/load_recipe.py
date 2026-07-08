import json
import os

import nickel

from cutler import cutler as cl
from cutler.parsing import parse_recipe

def load_recipe(file: str) -> cl.Recipe:
    expr = f'(import {json.dumps(os.path.abspath(file))})'
    raw = json.loads(nickel.run(expr))
    return parse_recipe(raw)
