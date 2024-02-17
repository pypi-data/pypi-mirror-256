def get_local_repo(repo: str, repo_url: str):
    return rf"""[local-{repo.lower()}]
name = Local {repo}
enabled = 1
gpgcheck = 0
baseurl = {repo_url.rstrip('/')}/\$releasever/{repo}/\$basearch/os
ui_repoid_vars = releasever basearch
priority=1
proxy=
"""


def get_insecure_registry(registry):
    return f"""
{
  "log-driver": "journald",
  "insecure-registries" : [ {registry} ]
}
"""

def get_epel(epelurl):
    return f"""
[local-epel]
name = Local EPEL
enabled = 1
gpgcheck = 0
baseurl = {epelurl}
priority=1
proxy="""