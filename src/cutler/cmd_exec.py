import asyncio
import os
import shlex
import sys

async def exec_cmd(ctx, name, args):
    args = _override_cmd(ctx.settings.command_override, args)
    async with ctx.cmd_semaphore:
        sys.stderr.write(f'starting cmd {name}\n')
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        if proc.returncode != 0:
            sys.stderr.write(f'failed cmd {name}\ncmd: {shlex.join(args)}\nstderr:\n{stderr}\n')
            sys.stderr.flush()
            os._exit(1) # FIXME: wait for other tasks to complete

        sys.stderr.write(f'finished cmd {name}\n')
        return stdout

def _override_cmd(command_override, args):
    override = command_override.get(args[0])
    if override is None:
        return args
    prefix = [override] if isinstance(override, str) else list(override)
    return [*prefix, *args[1:]]
