import logging
from queue import Queue
import re
from ezlab.infra.proxy import proxy_files
from ezlab.infra.remote import ssh_content_into_file, ssh_run_command
from ezlab.infra.repo import get_epel, get_insecure_registry, get_local_repo
from ezlab.parameters import GENERIC, KVM, PVE, SETUP_COMMANDS, TASK_FINISHED
from ezlab.utils import fire_and_forget
from ezlab.infra import hv_pve
from ezlab.infra import hv_kvm


logger = logging.getLogger()


@fire_and_forget
def prepare(
    hostname: str,
    hostip: str,
    config: dict,
    addhosts: list,
    prepare_for: str,
    queue: Queue,
    dryrun: bool,
):
    """
    Configure VMs for selected product, taking care of pre-requisites
    Params:
        <hostname>      : VM hostname
        <hostip>        : VM IP address (should be reachable)
        <config>        : Dictinary of configuration from app settings
        <addhosts>      : Other hosts to add to /etc/hosts file, dict{'ip', 'name'}
        <prepare_for>   : EZUA | EZDF | Generic (from parameters: UA|DF|GENERIC)
        <queue>         : Message queue
        <dryrun>        : Do not execute but report

    Returns <bool>     : True in succesful completion, False otherwise. If dryrun, returns dict of job run
    """

    response = {}

    if dryrun:
        response["task"] = (
            f"Prepare {hostname} ({hostip}) for {prepare_for} {'with hosts: ' + ','.join(addhosts) if len(addhosts) > 0 else 'as single node'}"
        )
        response["settings"] = config

    domain = config["domain"]
    cidr = config["cidr"]
    username = config["username"]
    # password = config["password"]
    keyfile = config["privatekeyfile"]
    # commands to execute, always prepend with generic/common commands, such as enable password auth, disable subscription mgr etc.
    commands = list(SETUP_COMMANDS[GENERIC]) + list(SETUP_COMMANDS[prepare_for])
    after_generic_commands = len(list(SETUP_COMMANDS[GENERIC]))

    # "/etc/cloud/templates/hosts.redhat.tmpl": f"127.0.0.1 localhost.localdomain localhost\n{hostip} {hostname}.{domain} {hostname}\n"
    hosts = [
        "127.0.0.1 localhost.localdomain localhost",
        f"{hostip} {hostname}.{domain} {hostname}",
    ] + [f"{h['ip']} {h['name']}.{domain} {h['name']}" for h in addhosts]

    files = {"/etc/hosts": "\n".join(hosts)}

    # update env files for proxy
    noproxy = (
        f"{hostip},{re.split(':|/', config.get('maprlocalrepo').split('://')[1])[0]}"
        if config.get("maprrepoislocal", False)
        else hostip
    )

    if config.get("proxy", "").strip() != "":
        for file in proxy_files(config["proxy"], domain, cidr, noproxy):
            files.update(file)

    # TODO: Not tested, enable insecure registry
    if (
        config.get("airgap_registry", "").strip() != ""
        and config["airgap_registry"].split("://")[0] == "http"
    ):
        files.update(
            {
                "/etc/docker/daemon.json": get_insecure_registry(
                    config["airgap_registry"]
                )
            }
        )

    repo_content = ""
    if config.get("yumrepo", "").strip() != "":
        for repo in ["BaseOS", "AppStream", "PowerTools", "extras"]:
            repo_content += get_local_repo(repo, config.get("yumrepo")) + "\n"

    else:
        print("Using system repositories")

    if config.get("epelrepo", "").strip() != "":
        repo_content += get_epel(config.get("epelrepo"))

    else:
        epel_default = "sudo subscription-manager repos --enable codeready-builder-for-rhel-8-x86_64-rpms; sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm"
        commands.insert(after_generic_commands, epel_default)

    if repo_content != "":  # yum or epel repo given
        files.update({"/etc/yum.repos.d/local.repo": repo_content})

    if dryrun:
        response["files"] = files
    else:
        try:
            for filepath, content in files.items():
                print(f"[{hostip}] Writing {filepath}")
                queue.put(f"[ {hostip} ] COPY {filepath}")
                for result in ssh_content_into_file(
                    host=hostip,
                    username=username,
                    keyfile=keyfile,
                    content=content,
                    filepath=filepath,
                ):
                    queue.put(f"[ {hostip} ] COPYOUT: {result}")

        except Exception as error:
            print(error)
            return False

    if (
        config.get("yumrepo", "").strip() != ""
        or config.get("epelrepo", "").strip() != ""
    ):
        commands.insert(
            after_generic_commands,
            "sudo dnf config-manager --set-disabled baseos appstream extras",
        )

    if config.get("proxy", "").strip() != "":
        commands.insert(
            after_generic_commands + 1,
            "sudo sed -i '/proxy=/d' /etc/dnf/dnf.conf > /dev/null; echo proxy={proxy_line} | sudo tee -a /etc/dnf/dnf.conf >/dev/null".format(
                proxy_line=(
                    config["proxy"]
                    if config["proxy"][-1] == "/"
                    else config["proxy"] + "/"
                )
            ),
        )

    # rename host
    commands.insert(
        after_generic_commands + 2, f"sudo hostnamectl set-hostname {hostname}.{domain}"
    )

    if dryrun:
        response["commands"] = commands

    else:
        try:
            for command in commands:
                print(f"[ {hostip} ] RUN: {command}")
                queue.put(f"[ {hostip} ] SSH: {command}")
                for output in ssh_run_command(
                    host=hostip, username=username, keyfile=keyfile, command=command
                ):
                    queue.put(f"[ {hostip} ] SSHOUT: {output}")
        except Exception as error:
            print(error)
            return False

    queue.put(TASK_FINISHED)

    return response if dryrun else True


@fire_and_forget
def clone(
    target: str,
    connection,
    resources: set,
    settings: dict,
    vm_number: int,
    queue: Queue,
    dryrun: bool,
):

    if target == PVE:
        return hv_pve.clone(
            proxmox=connection,
            resources=resources,
            settings=settings,
            vm_number=vm_number,
            queue=queue,
            dryrun=dryrun,
        )
    elif target == KVM:
        return hv_kvm.clone(
            conn=connection,
            resources=resources,
            settings=settings,
            vm_number=vm_number,
            queue=queue,
            dryrun=dryrun,
        )
    else:
        queue.put("Unknown target")
        return False

