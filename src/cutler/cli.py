import click

from cutler.cutler import exec_recipe
from cutler.load_recipe import load_recipe
from cutler.parse_vars import vars_from_click_arg, vars_from_csv


@click.command()
@click.argument('recipe_file', type=click.File())
@click.option(
    '-v', '--var', 'var_args', multiple=True, metavar='NAME=JSON',
    help='Set a recipe variable; value is parsed as JSON. Repeatable.',
)
@click.option(
    '--vars-from-csv', 'vars_csv_file', type=click.File(), default=None,
    help='Instantiate the recipe once per CSV row. CSV fields are used as variables.',
)
def main(recipe_file, var_args, vars_csv_file):
    global_vars = vars_from_click_arg(var_args)

    if vars_csv_file is not None:
        var_assignments = vars_from_csv(vars_csv_file, global_vars)
    else:
        var_assignments = [global_vars]

    recipe = load_recipe(recipe_file, var_assignments)
    exec_recipe(recipe)


if __name__ == "__main__":
    main()
