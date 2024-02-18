# /usr/bin/python3

from ipaddress import ip_address
from queue import Queue
import string
import sys
import libvirt
from libvirt import *
from xml.etree import ElementTree as ET
from ezlab.infra.cloudinit import cloudinit_metadata, cloudinit_networkconfig, cloudinit_userdata
from ezlab.infra.authkey import get_privatekey_from_string, get_ssh_pubkey_from_privatekey
from ezlab.infra.remote import ssh_run_command, wait_for_ssh, ssh_content_into_file
from ezlab.parameters import SWAP_DISK_SIZE, TASK_FINISHED

def connect(host: str, username: str):
    try:
        conn = open(f"qemu+ssh://{username}@{host}/system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        return None

    return conn


def vms(conn: virConnect):
    domainIDs = conn.listDomainsID()
    if domainIDs == None or len(domainIDs) == 0:
        return list()
    else:
        for domainID in domainIDs:
            yield domainID


def bridges(conn: virConnect):
    return [
        n.bridgeName()
        for n in [conn.networkLookupByName(net) for net in conn.listNetworks()]
    ]


def pools(conn):
    pools = conn.listAllStoragePools()
    if not pools:
        return list()
        # raise SystemExit("Failed to locate any StoragePool objects.")

    # return pools
    return [pool for pool in pools if pool.isActive() == True]


def volumes(conn, pool):
    if pool is None:
        return list()
    sp = conn.storagePoolLookupByName(pool)
    if sp is None:
        return list()
    else:
        return sp.listVolumes()


def sp_basepath(sp):
    raw_xml = sp.XMLDesc(0)
    tree = ET.ElementTree(ET.fromstring(raw_xml))

    return tree.find("target").find("path").text


def get_storagepool(conn, poolname):
    return conn.storagePoolLookupByName(poolname)


def clone(
    conn: virConnect,
    resources: set,
    settings: dict,
    vm_number: int,
    queue=Queue,
    dryrun=True,
):
    """
    Clone VM
    """
    dom = None

    # Parse inputs
    (pool, baseimg, bridge, eznode, hostname, first_ip) = resources

    privatekey: str = settings["privatekey"]
    ssh_keyfile: str = settings["privatekeyfile"]

    multivm = vm_number > 0
    vm_name = hostname + str(vm_number if multivm else "")
    vm_domain = settings["domain"]
    vm_ip = str(
        ip_address(first_ip) + vm_number - 1 if multivm else ip_address(first_ip)
    )  # adjust for single VM
    vm_gateway = settings["gateway"]
    vm_network_bits = settings["cidr"].split("/")[1]

    pk = get_privatekey_from_string(privatekey)
    publickey = get_ssh_pubkey_from_privatekey(pk)
    kvm_host = conn.getHostname()
    _, host = conn.getURI().split('://')
    kvm_username = host.split('@')[0]
    sp = get_storagepool(conn, pool)
    # host path for storage pool
    sp_path = sp_basepath(sp)
    baseimgPath = sp.storageVolLookupByName(baseimg).path()

    queue.put(f"[ {vm_name} ] cloning...")

    # Cloud-init files
    cloudinit_files = {
        # meta-data           
        "/tmp/meta-data": cloudinit_metadata(hostname=vm_name),
        # user-data
        "/tmp/user-data": cloudinit_userdata(
            hostname=vm_name,
            fqdn=f"{vm_name}.{vm_domain}",
            ssh_username=settings["username"],
            ssh_password=settings["password"],
            ssh_pubkey=publickey,
            swap_disk="/dev/vdb",
        ),
        # network-config
        "/tmp/network-config": cloudinit_networkconfig(
            ip_address=vm_ip,
            network_bits=vm_network_bits,
            gateway=vm_gateway,
            nameserver=settings["nameserver"],
            searchdomain=vm_domain,
        ),
    }

    # copy cloudinit files
    if dryrun:
        queue.put(
            f"""Would configure disks:
                  OS Disk: {eznode['os_disk_size']}G
                  Swap Disk: {SWAP_DISK_SIZE}G
                  Data Disks (qty: {eznode["no_of_disks"]}): {eznode["data_disk_size"]}G
                  All disks will be stored in {kvm_host}:{sp_path}/{vm_name}/
                  """
        )
        queue.put("cloudinit files", cloudinit_files)

    else:
        queue.put(f"[ {vm_name} ] uploading cloud-init files...")
        try:
            for filepath, content in cloudinit_files.items():
                for out in ssh_content_into_file(
                    host=kvm_host,
                    username=kvm_username,
                    keyfile=ssh_keyfile,
                    content=content,
                    filepath=filepath,
                ):
                    queue.put(f"{kvm_host} COPY {filepath} {out}")

        except Exception as error:
            queue.put(f"KVM CLOUDINIT COPY ERROR for {vm_name}: {error}")
            queue.put(TASK_FINISHED)
            return False

        # package manager for kvm host
        PKGINSTALL = ""
        for out in ssh_run_command(kvm_host, kvm_username, ssh_keyfile, "command -v yum || command -v apt"):
            PKGINSTALL=out

        queue.put(f"[ {vm_name} ] creating disks...")
        # generate cloudinit iso file
        for out in ssh_run_command(
            kvm_host,
            kvm_username,
            ssh_keyfile,
            f"""
            # delete existing ci iso file
            [ -f {sp_path}/{vm_name}-ci.iso ] && sudo rm -f {sp_path}/{vm_name}-ci.iso
            cd /tmp && genisoimage -quiet -output {sp_path}/{vm_name}-ci.iso -V cidata -r -J user-data meta-data network-config
            """,
        ):
            print(out)

        # OS disk, backed by image
        create_osvol(
            sp=sp,
            volname=f"{vm_name}-os.qcow2",
            sizeGB=eznode["os_disk_size"],
            baseimg=baseimgPath,
        )

        # swap disk
        create_datavol(
            sp=sp,
            volname=f"{vm_name}-swap.qcow2",
            sizeGB=SWAP_DISK_SIZE,
        )

        # data disk(s)
        for i in range(eznode["no_of_disks"]):
            create_datavol(
                sp=sp,
                volname=f"{vm_name}-data{i}.qcow2",
                sizeGB=eznode["data_disk_size"],
            )

    queue.put(f"[ {vm_name} ] creating...")
    # Define VM
    vmXml = vm_xml(name=vm_name, memMB=int(eznode["memGB"] * 1024), cores=eznode["cores"], basepath=sp_path, baseimgPath=baseimgPath, bridge=bridge, no_of_datadisks=int(eznode["no_of_disks"]))

    if dryrun:
        queue.put(f"domain.xml to create VM: {vm_xml}")
    else:
        try:
            dom = conn.defineXMLFlags(vmXml,0)

        except Exception as error:
            queue.put(f"KVM VM DEFINITION ERROR for {vm_name}: {error}")
            queue.put(TASK_FINISHED)
            return False

    # Update dns entry in virtualnet
    if dryrun:
        queue.put(f"Add '{vm_ip}: {vm_name}.{vm_domain}' to your DNS")
    else:
        queue.put("")
        # ### THIS IS WRONG, NIC SHOULD BE DETACHED/ATTACHED TO ALL RUNNING INSTANCES
        try:
            queue.put(f"[ {vm_name} ] update libvirt dns")
            virnet = [
                conn.networkLookupByName(net)
                for net in conn.listNetworks()
                if conn.networkLookupByName(net).bridgeName() == bridge
            ].pop()
            if virnet:
                dnshostXml = f"<host ip='{vm_ip}'><hostname>{vm_name}</hostname></host>"
                if virnet.update(
                    command=libvirt.VIR_NETWORK_UPDATE_COMMAND_ADD_LAST,
                    section=libvirt.VIR_NETWORK_SECTION_DNS_HOST,
                    parentIndex=-1,
                    xml=dnshostXml,
                    flags=libvirt.VIR_DOMAIN_AFFECT_CONFIG | libvirt.VIR_DOMAIN_AFFECT_LIVE,
                ) == 0:
                    queue.put(f"[ {vm_name} ] dns entry added for {vm_ip}")
                else:
                    queue.put(f"[ {vm_name} ] dns update failed, ignoring")
            else:
                queue.put(f"[ {vm_name} ] dns update failed to match network, are you using a bridge?")

        except Exception as error:
            print("KVM VIRNET UPPDATE EXCEPTION", error)
            queue.put(
                f"Failed to update virtualNetwork, ignoring dns update for {vm_name}"
            )

    queue.put(f"[ {vm_name} ] start")
    # Create/Boot VM
    if not dryrun:
        try:
            if dom.create() < 0:
                queue.put(f"KVM VM CREATE ERROR for {vm_name}: {error}")
                queue.put(TASK_FINISHED)
                return False

            queue.put(f"[ {vm_name} ] booting")
            dom.setAutostart(1)  # turn on autostart
        except Exception as error:
            queue.put(f"KVM VM STARTUP ERROR for {vm_name}: {error}")
            queue.put(TASK_FINISHED)
            return False

    queue.put(f"[ {vm_name} ] waiting startup...")
    if not wait_for_ssh(f"{vm_name}.{vm_domain}", settings["username"], ssh_keyfile):
        queue.put(f"[ {dom.name()} ] SSH FAILED")
        queue.put(TASK_FINISHED)
        return False

    queue.put(f"[ {dom.name()} ] ready for {eznode['product']}")
    queue.put(TASK_FINISHED)
    return True


def vm_xml(name: str, memMB: int, cores: int, basepath: str, baseimgPath: str, bridge: str, no_of_datadisks: int):

    datadisks = ""
    letters = string.ascii_lowercase
    start_letter = letters.index('c') # starting from /dev/vdc

    for i in range(no_of_datadisks):
        diskname = f"vd{letters[start_letter + i]}"
        datadisks += f"""
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' discard='unmap'/>
      <source file='{basepath}/{name}-data{i}.qcow2'/>
      <backingStore/>
      <target dev='{diskname}' bus='virtio'/>
      <alias name='virtio-disk{i+2}'/>
    </disk>
"""

    return f"""
<domain type="kvm">
  <name>{name}</name>
  <metadata>
    <libosinfo:libosinfo xmlns:libosinfo="http://libosinfo.org/xmlns/libvirt/domain/1.0">
      <libosinfo:os id="http://rockylinux.org/rocky/8"/>
    </libosinfo:libosinfo>
  </metadata>
  <memory unit='MiB'>{memMB}</memory>
  <currentMemory unit='MiB'>{memMB}</currentMemory>
  <memoryBacking>
    <source type='memfd'/>
    <access mode='shared'/>
  </memoryBacking>
  <vcpu placement='static'>{cores}</vcpu>
  <features>
    <acpi/>
    <apic/>
    <vmport state='off'/>
  </features>
  <resource>
    <partition>/machine</partition>
  </resource>
  <sysinfo type='smbios'>
    <system>
      <entry name='serial'>ds=nocloud</entry>
    </system>
  </sysinfo>
  <os>
    <type arch='x86_64' machine='pc-q35-6.2'>hvm</type>
    <boot dev='hd'/>
    <smbios mode='sysinfo'/>
  </os>
  <devices>
    <clock offset="utc"/>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>destroy</on_crash>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' discard='unmap'/>
      <source file='{basepath}/{name}-os.qcow2'/>
      <backingStore type='file'>
        <format type='qcow2'/>
        <source file='{baseimgPath}'/>
        <backingStore/>
      </backingStore>
      <target dev='vda' bus='virtio'/>
      <alias name='virtio-disk0'/>
    </disk>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' discard='unmap'/>
      <source file='{basepath}/{name}-swap.qcow2'/>
      <backingStore/>
      <target dev='vdb' bus='virtio'/>
      <alias name='virtio-disk1'/>
    </disk>
    <disk type='file' device='cdrom'>
      <driver name='qemu' type='raw'/>
      <source file='{basepath}/{name}-ci.iso'/>
      <backingStore/>
      <target dev='sda' bus='sata'/>
      <readonly/>
      <alias name='sata0-0-0'/>
      <address type='drive' controller='0' bus='0' target='0' unit='0'/>
    </disk>
    {datadisks}
    <interface type="bridge">
      <source bridge="{bridge}"/>
    </interface>
    <input type="mouse" bus="ps2"/>
    <graphics type="vnc" autoport="yes" listen="127.0.0.1"/>
    <console type="pty">
      <source>
        <clipboard copypaste="yes"/>
      </source>
      <target type="virtio"/>
    </console>
    <memballoon model='virtio'/>
    <rng model='virtio'>
      <backend model='random'>/dev/urandom</backend>
      <alias name='rng0'/>
    </rng>
  </devices>
</domain>
"""


def create_datavol(sp: virStoragePool, volname:str, sizeGB: int):
    volXml = f"""
        <volume>
          <name>{volname}</name>
          <allocation>0</allocation>
          <capacity unit="GiB">{sizeGB}</capacity>
          <target>
            <format type='qcow2'/>
            <permissions>
              <mode>0644</mode>
              <label>virt_image_t</label>
            </permissions>
          </target>
        </volume>"""

    return sp.createXML(volXml, 0)   


def create_osvol(sp: virStoragePool, volname: str, sizeGB: int, baseimg: str):
    volXml = f"""
        <volume>
          <name>{volname}</name>
          <allocation>0</allocation>
          <capacity unit="GiB">{sizeGB}</capacity>
          <target>
            <format type='qcow2'/>
            <backingStore type='file'>
                <format type='qcow2'/>
                <source file='{baseimg}'/>
                <backingStore/>
            </backingStore>
            <permissions>
              <mode>0644</mode>
              <label>virt_image_t</label>
            </permissions>
          </target>
        </volume>"""

    return sp.createXML(volXml, 0)   


# def get_network_with_new_host(network: virNetwork, hostname: str, ip: str):

#     # <dns>
#     #   <host ip='192.168.122.2'>
#     #     <hostname>myhost</hostname>
#     #   </host>
#     # </dns>

#     raw_xml = network.XMLDesc(0)
#     tree = ET.ElementTree(ET.fromstring(raw_xml))
#     dnsDom = tree.find("dns")
#     if not dnsDom:
#         print("add dns entry")
#         dnsDom = ET.Element("dns")
#         tree.getroot().append(dnsDom)

#     else:
#         # check if ip exist (append host if so)
#         existing_ip = [h for h in dnsDom if h.get("ip") == ip]
#         if len(existing_ip) > 0:
#             hostElement = existing_ip[0]
#             if hostElement.find("hostname").text == hostname:
#                 # nothing to change
#                 return None
#             else:
#                 newhost = ET.Element("hostname")
#                 newhost.text = hostname
#                 hostElement.append(newhost)

#     # new host entry
#     newhost = ET.Element("hostname")
#     newhost.text = hostname
#     newip = ET.Element("host", ip=ip)
#     newip.append(newhost)
#     dnsDom.append(newip)

#     return ET.tostring(tree.getroot(), 'unicode')


# def get_nicXml(dom: virDomain, bridge: str):
#     tree = ET.ElementTree(
#         ET.fromstring(dom.XMLDesc(0))
#     )
#     root = tree.getroot()

#     interfaces = root.findall("./devices/interface")
#     nic = [nic for nic in interfaces if nic.find("source").attrib.get("bridge") == bridge].pop()

#     return ET.tostring(nic, 'unicode')


#         netXml = get_network_with_new_host(virnet, vm_name, vm_ip)
#         if netXml is not None:
#             virnet.destroy()
#             virnet.undefine()
#             network = conn.networkDefineXML(netXml)
#             if network == None:
#                 print("Failed to create network", netXml)
#             else:
#                 network.create()
#                 network.setAutostart(1)
#                 # remove/attach VM nic
#                 nicXml = get_nicXml(dom, bridge)
#                 dom.dev
#                 dom.attachDeviceFlags(nicXml, libvirt.VIR_DOMAIN_AFFECT_LIVE)


# if __name__ == "__main__":
#     conn = connect("10.1.1.5", "erdincka")
#     print(get_nicXml(conn.lookupByName("test"), "virbr0"))
