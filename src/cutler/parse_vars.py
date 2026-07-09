import csv
import json

import click

def _coerce(value: str):
    # valid jsons are parsed as json; everything else is a string lmao
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value

def vars_from_csv(f, global_vars: dict[str, any]) -> list[dict[str, any]]:
    var_assignments = []
    for row in csv.DictReader(f):
        var_assignments.append({**global_vars, **{k: _coerce(v) for k, v in row.items()}})
    return var_assignments

def vars_from_jsonl(f, global_vars: dict[str, any]) -> list[dict[str, any]]:
    var_assignments = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        var_assignments.append({**global_vars, **json.loads(line)})
    return var_assignments

def vars_from_click_arg(vars_) -> dict[str, any]:
    var_assignments = {}
    for entry in vars_:
        name, sep, raw = entry.partition('=')
        if not sep:
            raise click.BadParameter(f'expected NAME=JSON, got {entry!r}', param_hint='--var')
        var_assignments[name] = _coerce(raw)
    return var_assignments
