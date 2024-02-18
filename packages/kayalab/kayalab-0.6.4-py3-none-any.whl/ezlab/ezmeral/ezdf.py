from queue import Queue
from paramiko import AutoAddPolicy, SSHClient
from ezlab.infra.remote import ssh_content_into_file, ssh_run_command
from ezlab.infra.repo import get_mapr_repo
from ezlab.utils import *
from ezlab.parameters import *
from paramiko_expect import SSHClientInteraction


@fire_and_forget
def cluster_install(
    hosts: list[str],
    settings: dict, # settings from "config" key
    config: dict, # settings from "EZDF" key
    queue: Queue,
    dryrun: bool = True,
):
    hostnames = []
    name=config.get("cluster_name", "ezlab")
    disks=config.get("maprdisks", "/dev/sdz")

    response = {}
    if dryrun:
        response["task"] = (
            f"Create Data Fabric cluster {name} on {','.join(hosts)} using disk(s) {disks}"
        )
        response["settings"] = settings

    # lazy way to catch exceptions
    try:
        username = settings.get("username")
        # used for connecting to nodes from this app
        keyfile = settings.get("privatekeyfile")
        # used for connection between cluster nodes
        password = settings.get("password")

        # get fqdn for each host
        if dryrun:

            def get_hostname_command(host):
                return f"ssh {settings.get('username')}@{host} 'hostname -f'"

            response["commands"] = [get_hostname_command(host) for host in hosts]

        else:
            for host in hosts:
                print(f"Getting fqdn for {host}")
                for result in ssh_run_command(
                    host=host.strip(),
                    username=username,
                    keyfile=keyfile,
                    command="hostname -f",
                ):
                    hostnames.append(result)

        commands: list[str] = INSTALL_COMMANDS[DF]

        if config.get("maprrepoislocal", False):
            # using local repository for mapr packages
            ezrepo: str = config.get("maprlocalrepo", "").rstrip("/")
            repouser = config["maprlocalrepousername"]
            repopass = config["maprlocalrepopassword"]

            wgetauthstring = (
                f"--user={repouser} --password={repopass}"
                if config.get("maprlocalrepoauth", False)
                else ""
            )

            proto, path, *_ = ezrepo.split("://")
            repourl = (
                f"{proto}://{repouser}:{repopass}@{path}"
                if config.get("maprlocalrepoauth", False)
                else ezrepo
            )

            commands.insert(
                0,
                f"[ -f /tmp/mapr-setup.sh ] || wget -q {wgetauthstring} {ezrepo}/installer/redhat/mapr-setup.sh -P /tmp; chmod +x /tmp/mapr-setup.sh",
            )

            commands.insert(
                1,
                f"curl -s -k https://127.0.0.1:9443/ > /dev/null || sudo /tmp/mapr-setup.sh -y -r {repourl}/",
            )

        else:
            # using HPE repository
            ezrepo = f"https://package.ezmeral.hpe.com/releases"
            repouser = config["maprrepouser"]
            repotoken = config["maprrepotoken"]

            commands.insert(
                0,
                f"[ -f /tmp/mapr-setup.sh ] || wget -q --user={repouser} --password= {repotoken} {ezrepo}/installer/redhat/mapr-setup.sh -P /tmp; chmod +x /tmp/mapr-setup.sh",
            )

            commands.insert(
                1,
                f"curl -s -k https://127.0.0.1:9443/ > /dev/null || sudo /tmp/mapr-setup.sh -y --repo-user {repouser} --repo-token {repotoken}",
            )

        first_host = hosts[0].strip()

        # Create and upload stanza file
        stanza = get_mapr_stanza(
            hosts=hostnames,
            username=username,
            password=password,
            disks=disks.split(","),
            cluster_name=name,
        )

        if dryrun:
            response["files"] = {"/tmp/mapr.stanza": stanza}

        else:
            print(f"{first_host} Writing /tmp/mapr.stanza")
            for result in ssh_content_into_file(
                host=first_host,
                username=username,
                keyfile=keyfile,
                content=stanza,
                filepath="/tmp/mapr.stanza",
            ):
                queue.put(f"{first_host}: {result}")

            queue.put(f"stanza copied to {first_host}")

            queue.put(f"starting installer on {first_host}")

        if dryrun:
            response["commands"].extend(commands)

        else:
            for command in commands:
                print(f"{first_host} Running: {command}")
                for result in ssh_run_command(
                    host=first_host,
                    username=username,
                    keyfile=keyfile,
                    command=command,
                ):
                    queue.put(f"{first_host} SSH {result}")

            queue.put(
                f"echo Check installation process and results. Installer is available at https://{first_host}:9443/"
            )

    except Exception as error:
        print("Cluster creation exception", error)
        queue.put(TASK_FINISHED)
        if dryrun:
            return response
        else:
            return False

    queue.put(TASK_FINISHED)
    if dryrun:
        return response
    else:
        return True


@fire_and_forget
def client_install(
    username: str,
    keyfile: str,
    config: dict, # settings from "EZDF" key
    queue: Queue,
):
    server = config.get("connect_to")
    client = config.get("maprclient")
    cluster_name = config.get("cluster_name")

    if config.get("maprrepoislocal", False):
        # using local repository for mapr packages
        ezrepo: str = config.get("maprlocalrepo", "").rstrip("/")
    else:
        # using HPE repository
        ezrepo = f"https://package.ezmeral.hpe.com/releases"

    repo_content = get_mapr_repo(ezrepo)
    repofilename = "/etc/yum.repos.d/mapr.repo"

    if client is not None:
        try:
            for out in ssh_content_into_file(
                host=client,
                username=username,
                keyfile=keyfile,
                content=repo_content,
                filepath=repofilename,
            ):
                queue.put(f"[ {client} ] COPY {repofilename}: {out}")

        except Exception as error:
            print("Client file copy exception", error)
            queue.put(TASK_FINISHED)
            return False

    else: # working on local machine
        with open(repofilename, 'w') as repofile:
            repofile.write(repo_content)

    commands = INSTALL_COMMANDS[DFCLIENT]

    for file in DF_SECURE_FILES:
        commands.append(
            f"sudo curl -s --insecure --user mapr:mapr sftp://{server}{file} --output {file}"
        )

    # Run these last
    commands.append(
        f"sudo /opt/mapr/server/configure.sh -c -C {server} -N {cluster_name} -secure"
    )
    commands.append("echo mapr | sudo -u mapr maprlogin password")

    for command in commands:
        print(f"Runnning {command}")
        try:
            if client is not None:
                for result in ssh_run_command(
                    host=client, username=username, keyfile=keyfile, command=command
                ):
                    queue.put(f"[ {client} ] SSH {result}")

            else: # running locally
                result = subprocess.run(command.split(" "), shell=True, capture_output=True, text=True, check=True, universal_newlines=True, timeout=300)
                queue.put(f" [LOCALHOST] RUNOUT {command}: {result}")

        except Exception as error:
            print("Client command exception", command, error)
            queue.put(f"[ {client} CMD {command} failed with: {error}")
            queue.put(TASK_FINISHED)
            return False

    queue.put(TASK_FINISHED)
    return True


@fire_and_forget
def crosscluster(
    config: dict,
    settings: dict,
    queue: Queue,
    dryrun: bool = True,
):
    local = settings["crosslocalcldb"]
    remote = settings["crossremotecldb"]
    adminuser = settings["crossadminuser"]
    adminpassword = settings["crossadminpassword"]
    username = config["username"]
    keyfile = config["privatekeyfile"]

    queue.put(f"Create cross cluster connectivity between {local} and {remote}")

    response = {}
    if dryrun:
        response["task"] = f"Cross-cluster setup between {local} and {remote}"
        response["settings"] = {**config, **settings}

    else:  # get truststore passwords
        try:
            local_truststore_password = ""
            remote_truststore_password = ""

            for out in ssh_run_command(
                host=local,
                command="sudo grep ssl.server.truststore /opt/mapr/conf/store-passwords.txt | cut -d'=' -f2",
                username=username,
                keyfile=keyfile,
            ):
                local_truststore_password = out

            for out in ssh_run_command(
                host=remote,
                command="sudo grep ssl.server.truststore /opt/mapr/conf/store-passwords.txt | cut -d'=' -f2",
                username=username,
                keyfile=keyfile,
            ):
                remote_truststore_password = out

            if local_truststore_password and remote_truststore_password:
                queue.put(
                    f"using local truststore password: {local_truststore_password}"
                )
                queue.put(
                    f"using remote truststore password: {remote_truststore_password}"
                )
            else:
                queue.put(
                    f"ERROR: failed to get truststore passwords, local: {local_truststore_password}, remote: {remote_truststore_password}"
                )
                return False
        except Exception as error:
            print("Cross cluster setup exception", error)
            queue.put(TASK_FINISHED)
            return False

    cross_cluster_setup = f"sudo rm -rf /tmp/mapr-xcs; sudo -i -u {adminuser} /opt/mapr/server/configure-crosscluster.sh create all \
    -localcrossclusteruser {adminuser} -remotecrossclusteruser {adminuser} \
    -localtruststorepassword {local_truststore_password if local_truststore_password else 'LOCAL_TRUSTSTORE_PASSWORD'} \
    -remotetruststorepassword {remote_truststore_password if remote_truststore_password else 'REMOTE_TRUSTSTORE_PASSWORD'} \
    -remoteip {remote} -localuser {adminuser} -remoteuser {adminuser}"

    if dryrun:
        response["commands"] = (
            f"ssh {local} sudo grep ssl.server.truststore /opt/mapr/conf/store-passwords.txt | cut -d'=' -f2"
        )
        response["commands"] = (
            f"ssh {remote} sudo grep ssl.server.truststore /opt/mapr/conf/store-passwords.txt | cut -d'=' -f2"
        )
        response["commands"] = cross_cluster_setup
        queue.put(TASK_FINISHED)
        return response

    else:
        try:
            queue.put(
                "If fails run the configure-crosscluster.sh command on one of the cluster nodes:"
            )
            queue.put(cross_cluster_setup)

            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy)

            client.connect(hostname=local, username=username, key_filename=keyfile)

            interact = SSHClientInteraction(client, timeout=300, display=True)
            prompt = f".*[{username}@{local} ~]$.*"
            interact.expect(prompt)
            # print(interact.current_output_clean)

            interact.send(cross_cluster_setup)

            interact.expect("Enter password for mapr user.*")
            interact.send(adminpassword)
            interact.expect("Enter password for mapr user.*")
            interact.send(adminpassword)

            interact.expect(prompt)
            interact.send("exit")
            interact.expect()
        except Exception as error:
            print("Cross cluster setup exception", error)
            queue.put(TASK_FINISHED)
            return False

        queue.put(TASK_FINISHED)
        return True


def get_mapr_stanza(
    hosts: list, username: str, password: str, disks: list, cluster_name: str
):
    """
    Return stanza for Data Fabric installation
    """
    hosts_yaml = ""
    for host in hosts:
        hosts_yaml += f"  -   {host}\n"

    disks_yaml = ""
    for disk in disks:
        disks_yaml += f"  -   {disk}\n"

    return f"""
environment:
  mapr_core_version: 7.6.0
config:
  hosts:
{hosts_yaml}
  ssh_id: {username}
  ssh_password: {password}
  enable_nfs: False
  db_admin_user: root
  db_admin_password: mapr123
  log_admin_password: mapr123
  metrics_ui_admin_password: mapr123
  enable_encryption_at_rest: True
  license_type: M7
  mep_version: 9.2.1
  disks:
{disks_yaml}
  disk_format: true
  disk_stripe: 1
  cluster_name: {cluster_name}
  services:
    # template-05-converged:
    template-20-drill:
    # template-30-maprdb:
    # template-60-maprxd:
    mapr-keycloak:
      enabled: True
    mapr-hivemetastore:
      database:
        name: hive
        user: hive
        password: mapr123
    # this conflicts with keycloak
    mapr-hbase-rest:
      enabled: False
    mapr-grafana:
      enabled: False
    mapr-opentsdb:
      enabled: True
    mapr-collectd:
      enabled: False
    mapr-fluentd:
      enabled: False
    mapr-kibana:
      enabled: False
    mapr-elasticsearch:
      enabled: False
    mapr-data-access-gateway:
    mapr-mastgateway:
"""
