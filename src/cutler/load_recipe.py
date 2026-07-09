import json
import os
from typing import Optional, Sequence

import nickel

from cutler import cutler as cl
from cutler.parse_recipe import parse_recipe


def _nickel_str(s: str) -> str:
    if type(s) is not str:
        raise RuntimeError('trying to pass non-string as nickel string')
    return json.dumps(s).replace('%{', r'\%{')

def _nickel_obj(va: dict) -> str:
    return f"(std.deserialize 'Json {_nickel_str(json.dumps(va))})"

def load_recipe(recipe_path, data) -> cl.Recipe:
    recipe_path = os.path.abspath(recipe_path)
    if data is not None:
        expr = f'''
            (import {_nickel_str(recipe_path)}) {_nickel_obj(data)}
        '''
    else:
        expr = f'''
            (import {_nickel_str(recipe_path)})
        '''

    raw = json.loads(nickel.run(expr, import_paths=[os.path.dirname(recipe_path)]))
    return parse_recipe(raw)
