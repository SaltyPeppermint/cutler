import asyncio
import os
import re
import shlex
import sys

__newline = re.compile(r'[\r\n]')

async def exec_cmd(ctx, name, args):
    args = _override_cmd(ctx.settings.command_override, args)
    async with ctx.cmd_semaphore:
        row = ctx.display.add(name)

        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout_chunks = []
        stderr_chunks = []
        on_line = lambda line: ctx.display.update(row, line)
        await asyncio.gather(
            _line_by_line(proc.stdout, stdout_chunks, on_line),
            _line_by_line(proc.stderr, stderr_chunks, on_line),
        )
        await proc.wait()

        stdout = b''.join(stdout_chunks).decode()
        stderr = b''.join(stderr_chunks).decode()

        if proc.returncode != 0:
            ctx.display.stop()  # tear down the live region so the terminal is usable
            sys.stderr.write(f'failed cmd {name}\ncmd: {shlex.join(args)}\nstderr:\n{stderr}\n')
            sys.stderr.flush()
            os._exit(1)  # FIXME: wait for other tasks to complete

        ctx.display.done(row)
        return stdout

def _override_cmd(command_override, args):
    override = command_override.get(args[0])
    if override is None:
        return args
    prefix = [override] if isinstance(override, str) else list(override)
    return [*prefix, *args[1:]]

async def _line_by_line(reader, chunks, on_line):
    # read
    buf = ''
    while True:
        data = await reader.read(4096)
        if not data:
            break
        chunks.append(data)

        buf += data.decode(errors='replace')
        segments = __newline.split(buf)
        buf = segments.pop()

        last = next((s for s in reversed(segments) if s.strip()), None)
        if buf.strip():
            last = buf
        if last is not None:
            on_line(last.strip())
