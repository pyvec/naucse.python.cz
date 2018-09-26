## Paramiko, Netmiko and Fabric

### Paramiko

Paramiko is a Python (2.7, 3.4+) implementation of the SSHv2 protocol, providing both client and server functionality. While it leverages a Python C extension for low level cryptography (Cryptography), Paramiko itself is a pure Python interface around SSH networking concepts.

#### Install Paramiko

```
pip install paramiko
```

#### Paramiko example

```
#!/usr/bin/env python

import sys, paramiko

if len(sys.argv) < 4:
    print "args missing"
    sys.exit(1)

hostname = sys.argv[1]
password = sys.argv[2]
command = sys.argv[3]

username = "admin"
port = 22

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.connect(hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(command)
    print stdout.read(),
finally:
    client.close()
```

You can specify SSH private key using option connect() method parameter **key_filename=**.

### Netmiko

Multi-vendor library to simplify Paramiko SSH connections to network devices.

Currently supported:

**Regularly tested**

```
Arista vEOS
Cisco ASA
Cisco IOS
Cisco IOS-XE
Cisco IOS-XR
Cisco NX-OS
Cisco SG300
HP Comware7
HP ProCurve
Juniper Junos
Linux
```

**Limited testing**

```
Alcatel AOS6/AOS8
Apresia Systems AEOS
Calix B6
Cisco WLC
Dell OS9 (Force10)
Dell OS10
Dell PowerConnect
Extreme ERS (Avaya)
Extreme VSP (Avaya)
Extreme VDX (Brocade)
Extreme MLX/NetIron (Brocade/Foundry)
Huawei
IP Infusion OcNOS
Mellanox
NetApp cDOT
Palo Alto PAN-OS
Pluribus
Ruckus ICX/FastIron
Ubiquiti EdgeSwitch
Vyatta VyOS
```

**Experimental**

```
A10
Accedian
Aruba
Ciena SAOS
Citrix Netscaler
Cisco Telepresence
Check Point GAiA
Coriant
Dell OS6
Dell EMC Isilon
Eltex
Enterasys
Extreme EXOS
Extreme Wing
Extreme SLX (Brocade)
F5 LTM
Fortinet
MRV Communications OptiSwitch
Nokia/Alcatel SR-OS
QuantaMesh
Rad ETX
```

#### Netmiko installation

```
pip install netmiko
```

#### Netmiko example

A simple SSH session to a Cisco router that executes the 'show ip int brief' command:

```
>>> from netmiko import ConnectHandler

>>> cisco_881 = {
...   'device_type': 'cisco_ios',
...   'ip': '10.10.10.227',
...   'username': 'pyclass',
...   'password': 'password',
... }

>>> net_connect = ConnectHandler(**cisco_881)
SSH connection established to 10.10.10.227:22
Interactive SSH session established 
```

Alternatively, I could just call the ConnectHandler function directly and not use a dictionary (as follows):

```
>>> net_connect = ConnectHandler(device_type='cisco_ios', ip='10.10.10.227', username='pyclass', password='password') 
```

Now at this point we have an SSH connection. I can verify this by executing the .find_prompt() method

```
>>> net_connect.find_prompt()
u'pynet-rtr1#' 
```

Use the .send_command() method to send the 'show ip int brief' command:

```
>>> output = net_connect.send_command("show ip int brief")
>>> print output
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0              unassigned      YES unset  down                  down    
FastEthernet1              unassigned      YES unset  down                  down    
FastEthernet2              unassigned      YES unset  down                  down    
FastEthernet3              unassigned      YES unset  down                  down    
FastEthernet4              10.220.88.20    YES NVRAM  up                    up      
Vlan1                      unassigned      YES unset  down                  down   
```

### Fabric

Fabric is a high level Python (2.7, 3.4+) library designed to execute shell commands remotely over SSH.

#### Fabric installation

```
pip install Fabric
```

#### Fabric example

```
from fabric.api import *
import fabric.contrib.project as project
import os
import shutil
import sys
import SocketServer

from pelican.server import ComplexHTTPRequestHandler

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'

# Github Pages configuration
env.github_pages_branch = "gh-pages"

# Port for `serve`
PORT = 8000

def clean():
    """Remove generated files"""
    if os.path.isdir(DEPLOY_PATH):
        shutil.rmtree(DEPLOY_PATH)
        os.makedirs(DEPLOY_PATH)

def build():
    """Build local version of site"""
    local('pelican -s pelicanconf.py')

def rebuild():
    """`build` with the delete switch"""
    local('pelican -d -s pelicanconf.py')

def regenerate():
    """Automatically regenerate site upon file modification"""
    local('pelican -r -s pelicanconf.py')

def serve():
    """Serve site at http://localhost:8000/"""
    os.chdir(env.deploy_path)

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()

def reserve():
    """`build`, then `serve`"""
    build()
    serve()

def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')

def cf_upload():
    """Publish to Rackspace Cloud Files"""
    rebuild()
    with lcd(DEPLOY_PATH):
        local('swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
              '-U {cloudfiles_username} '
              '-K {cloudfiles_api_key} '
              'upload -c {cloudfiles_container} .'.format(**env))

@hosts(production)
def publish():
    """Publish to production via rsync"""
    local('pelican -s publishconf.py')
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True,
        extra_opts='-c',
    )

def gh_pages():
    """Publish to GitHub Pages"""
    rebuild()
    local("ghp-import -b {github_pages_branch} {deploy_path} -p".format(**env))
```

