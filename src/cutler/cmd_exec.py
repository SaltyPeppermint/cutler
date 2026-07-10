import asyncio
import shlex
import sys

async def exec_cmd(ctx, name, args):
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
            sys.exit(1)

        sys.stderr.write(f'finished cmd {name}\n')
        return stdout
