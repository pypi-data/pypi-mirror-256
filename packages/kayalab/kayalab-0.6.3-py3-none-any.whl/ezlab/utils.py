import asyncio
import base64
from ipaddress import IPv4Address, ip_address
import os
import shlex
import socket
import subprocess

from ezlab.parameters import *

# validation for non-zero entry
def nonzero(val):
    return len(val) != 0

# wrapper to make sync calls async-like
def fire_and_forget(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(
            None, f, *args, *[v for v in kwargs.values()]
        )

    return wrapped

# find app on system path
def find_app(name: str):
    """Return executable path for `name` on PATH or in CWD."""
    from shutil import which

    return which(cmd=name, path=f"{os.environ.get('PATH')}:{os.getcwd()}")

# execute app/script locally
def execute(cmd: str):
    proc = subprocess.Popen(
        args=shlex.split(cmd),
        stdout=subprocess.PIPE,
        universal_newlines=True,
        # env=sub_env,
    )

    while proc.stdout:
        output = proc.stdout.readline().strip()
        if output == "" and proc.poll() is not None:
            break
        if output:
            yield f">>> {output}"
    rc = proc.poll()

# Base64 conversion for secrets etc
def toB64(string: str):
    return base64.b64encode(string.encode("ascii")).decode("utf-8")

# IP address validation
def validate_ip(ip_string: str) -> bool:
    try:
        return isinstance(ip_address(ip_string), IPv4Address)
    except:
        return False

# reliably get FQDN for given IP
def get_fqdn(ip_string: str) -> str:
    fqdn, _, _ = socket.gethostbyaddr(ip_string)
    return fqdn


def is_file(file):
    return os.path.isfile(os.path.abspath(file))


def debug_queue_to_here(queue, message):
    print(message)
    queue.put(TASK_FINISHED)
    return True
