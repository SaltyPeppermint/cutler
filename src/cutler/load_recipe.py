import json
import os
from typing import Optional, Sequence

import nickel

from cutler import cutler as cl
from cutler.parse_recipe import parse_recipe


def _instance_expr(file_contents: str, var_assignments: dict) -> str:
    expr = f'({file_contents})'
    for name, value in var_assignments.items():
        expr = f'(let {name} = {json.dumps(value)} in {expr})'
    return expr


def load_recipe(f, var_assignments: Optional[Sequence[dict]] = None) -> cl.Recipe:
    file_contents = f.read()

    # TODO: find cleaner way to do this that doesn't result in wrong error messages
    # maybe just make a .merge method on Recipe
    exprs = [_instance_expr(file_contents, va) for va in (var_assignments or [{}])]
    expr = ' & '.join(exprs)

    # Let relative imports inside the recipe resolve against its own directory.
    raw = json.loads(nickel.run(expr, import_paths=[os.path.dirname(os.path.abspath(f.name))]))
    return parse_recipe(raw)
