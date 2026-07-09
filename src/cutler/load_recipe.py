import json
import os
from typing import Optional, Sequence

import nickel

from cutler import cutler as cl
from cutler.parse_recipe import parse_recipe


def load_recipe(recipe_path, var_assignments: Optional[Sequence[dict]] = None) -> cl.Recipe:
    recipe_path = os.path.abspath(recipe_path)
    if var_assignments is not None:
        expr = f'''
            let
                recipe_builder = (import {json.dumps(recipe_path)})
            in
                {'&'.join([f'(recipe_builder {json.dumps(va)})' for va in var_assignments])}
        '''
    else:
        expr = f'''
            (import {json.dumps(recipe_path)})
        '''

    raw = json.loads(nickel.run(expr, import_paths=[os.path.dirname(recipe_path)]))
    return parse_recipe(raw)
