import asyncio

import click

from cutler.cutler import exec_recipe
from cutler.load_recipe import load_recipe
from cutler.parse_vars import vars_from_click_arg, records_from_csv, records_from_jsonl, coerce


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
@click.option(
    '-j', '--max-parallel-cmds', 'max_parallel_cmds', type=int, default=None,
    help='Override the recipe\'s max_parallel_cmds setting.'
)
@click.option(
    '--ffmpeg-command', 'ffmpeg_command', default=None,
    help='Override the command used to run ffmpeg. A JSON list may be given for a multi-token command.'
)
@click.option(
    '--ffprobe-command', 'ffprobe_command', default=None,
    help='Override the command used to run ffprobe. A JSON list may be given for a multi-token command.'
)
@click.option(
    '--override-command', 'override_commands', nargs=2, multiple=True, metavar='NAME VALUE',
    help='Override the command NAME (argv[0]) with VALUE (a JSON list may be given). Repeatable.'
)
def main(recipe_path, var_args, records_csv_file, records_jsonl_file,
         max_parallel_cmds, ffmpeg_command, ffprobe_command, override_commands):
    data = vars_from_click_arg(var_args)

    if records_csv_file is not None:
        data['records'] = records_from_csv(records_csv_file)
    if records_jsonl_file is not None:
        data['records'] = records_from_jsonl(records_jsonl_file)

    recipe = load_recipe(recipe_path, data or None)

    if max_parallel_cmds is not None:
        recipe.settings.max_parallel_cmds = max_parallel_cmds

    if ffmpeg_command is not None:
        recipe.settings.command_override['ffmpeg'] = coerce(ffmpeg_command)
    if ffprobe_command is not None:
        recipe.settings.command_override['ffprobe'] = coerce(ffprobe_command)
    for name, value in override_commands:
        recipe.settings.command_override[name] = coerce(value)

    asyncio.run(exec_recipe(recipe))


if __name__ == "__main__":
    main()
