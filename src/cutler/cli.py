import click

from cutler.cutler import exec_recipe
from cutler.load_recipe import load_recipe


@click.command()
@click.argument('recipe_file', type=click.Path(exists=True))
def main(recipe_file):
    recipe = load_recipe(recipe_file)
    exec_recipe(recipe)


if __name__ == "__main__":
    main()
