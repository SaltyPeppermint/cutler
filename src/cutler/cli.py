import asyncio

import click

from cutler.cutler import exec_recipe
from cutler.load_recipe import load_recipe
from cutler.parse_vars import vars_from_click_arg, vars_from_csv, vars_from_jsonl


@click.command()
@click.argument('recipe_path', type=click.Path(exists=True))
@click.option(
    '-v', '--var', 'var_args', multiple=True, metavar='NAME=JSON',
    help='Set a recipe variable. Valid json values are parsed as json, invalid ones are used as strings. Can be passed multiple times.',
)
@click.option(
    '--vars-from-csv', 'vars_csv_file', type=click.File(), default=None,
    help='Instantiate the recipe once per CSV row. CSV fields are used as variables.',
)
@click.option(
    '--vars-from-jsonl', 'vars_jsonl_file', type=click.File(), default=None,
    help='Instantiate the recipe once per JSONL line. Each JSON object provides variables.',
)
def main(recipe_path, var_args, vars_csv_file, vars_jsonl_file):
    global_vars = vars_from_click_arg(var_args)

    var_assignments = []
    if vars_csv_file is not None:
        var_assignments += vars_from_csv(vars_csv_file, global_vars)
    if vars_jsonl_file is not None:
        var_assignments += vars_from_jsonl(vars_jsonl_file, global_vars)
    if not var_assignments:
        var_assignments = [global_vars] if global_vars else None

    recipe = load_recipe(recipe_path, var_assignments)
    asyncio.run(exec_recipe(recipe))


if __name__ == "__main__":
    main()
