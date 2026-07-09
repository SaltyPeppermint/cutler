import subprocess
import sys

def exec_cmd(name, args):
    sys.stderr.write(f'starting cmd {name}\n')
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True).stdout
        sys.stderr.write(f'finished cmd {name}\n')
        return result
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f'failed cmd {name}\ncmd: {shlex.join(args)}\nstderr:\n{e.stderr}\n')
        raise
