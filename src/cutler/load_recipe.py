import json
import os

import nickel

from cutler import cutler as cl
from cutler.parsing import parse_recipe

def load_recipe(files: list[str]) -> cl.Recipe:
    imports = [f'(import {json.dumps(os.path.abspath(file))})' for file in files]
    expr = ' & '.join(imports)
    raw = json.loads(nickel.run(expr))
    return parse_recipe(raw)
