import click

from cutler.cutler import exec_recipe
from cutler.load_recipe import load_recipe


@click.command()
@click.argument('recipe_files', type=click.Path(exists=True), nargs=-1)
def main(recipe_files):
    recipe = load_recipe(recipe_files)
    exec_recipe(recipe)


if __name__ == "__main__":
    main()
