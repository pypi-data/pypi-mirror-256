import io
import logging
import random
import socket
import string
from time import sleep
from paramiko import (
    AuthenticationException,
    AutoAddPolicy,
    BadHostKeyException,
    RSAKey,
    SSHClient,
    SSHException,
)

from ezlab.parameters import PVE

logging.getLogger("paramiko").setLevel(logging.WARNING)

def wait_for_ssh(host, username, privatekey):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy)
    sleep_time = 5
    try:
        while True:
            sleep(sleep_time)
            print(f"DEBUG: trying {username}@{host}")
            client.connect(
                host,
                username=username,
                # key_filename=privatekey,
                pkey=RSAKey.from_private_key(io.StringIO(privatekey)),
                timeout=sleep_time,
            )
            break
    except (
        BadHostKeyException,
        AuthenticationException,
        ConnectionResetError,
        SSHException,
        socket.error,
    ):
        print(f"{host} still waiting ssh...")
        sleep(sleep_time)
    except Exception as error:
        print(f"{host} failed ssh connection with {error}")
        return False
    finally:
        print(f"{host} ssh connection check done")
        client.close()

    return True


def ssh_run_command(
    host: str,
    username: str,
    keyfile: str,
    command: str,
):
    """
    Run commands over ssh using default credentials
    Params:
        <host>              : hostname/IP to SSH
        <username>          : username to authenticate
        <keyfile>           : private key for <username>
        <command>           : command to run
    Returns:
        Generator with stdout. Calling function should process output with a for loop.
        Prints out stderr directly into terminal.

    """
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy)
    command_output = None
    # print(f"Try connection to {host}")
    try:
        client.connect(
            host,
            username=username,
            # key_filename=keyfile,
            # pkey=RSAKey.from_private_key(io.StringIO(keyfile)),
            pkey=RSAKey.from_private_key_file(keyfile),
            timeout=60,
        )

        # if "hostname -f" not in command:
        #     yield f"CMD: {command}"

        _stdin, _stdout, _stderr = client.exec_command(command, get_pty=True)
        command_errors = _stderr.read().decode().strip()
        command_output = _stdout.read().decode().strip()

        if command_errors and command_errors != "":
            yield f"[CMDERR]: {command_errors}"
        if command_output and command_output != "":
            # should return only the command output
            yield command_output

    except Exception as error:
        print("SSHCMD exception: ", error)

    finally:
        client.close()


def ssh_content_into_file(
    host: str, username: str, keyfile: str, content: str, filepath: str
):
    random_eof = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    command = f"""cat << {random_eof} | sudo tee {filepath} > /dev/null
{content}
{random_eof}"""
    return ssh_run_command(
        host=host,
        username=username,
        keyfile=keyfile,
        command=command,
    )
