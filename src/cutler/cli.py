import asyncio

import click

from cutler.cutler import exec_recipe
from cutler.load_recipe import load_recipe
from cutler.parse_vars import vars_from_click_arg, records_from_csv, records_from_jsonl


@click.command()
@click.argument('recipe_path', type=click.Path(exists=True))
@click.option(
    '-v', '--var', 'var_args', multiple=True, metavar='NAME=JSON',
    help='Set a recipe variable. The recipe will be given a dict with all variables.'
)
@click.option(
    '--records-from-csv', 'records_csv_file', type=click.File(), default=None,
    help='The recipe will be passed a dict that contains a `records` key, which will contain all the rows from the CSV. Values that are valid JSON are parsed as JSON. Otherwise, string is assumed.'
)
@click.option(
    '--records-from-jsonl', 'records_jsonl_file', type=click.File(), default=None,
    help='The recipe will be passed a dict that contains a `records` key, which will contain all the rows from the JSONL data.'
)
def main(recipe_path, var_args, records_csv_file, records_jsonl_file):
    data = vars_from_click_arg(var_args)

    if records_csv_file is not None:
        data['records'] = records_from_csv(records_csv_file)
    if records_jsonl_file is not None:
        data['records'] = records_from_jsonl(records_jsonl_file)

    recipe = load_recipe(recipe_path, data or None)
    asyncio.run(exec_recipe(recipe))


if __name__ == "__main__":
    main()
