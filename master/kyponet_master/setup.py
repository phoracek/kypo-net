#  copyright 2017 kypo-net authors
#
#  licensed under the apache license, version 2.0 (the "license");
#  you may not use this file except in compliance with the license.
#  you may obtain a copy of the license at
#
#      http://www.apache.org/licenses/license-2.0
#
#  unless required by applicable law or agreed to in writing, software
#  distributed under the license is distributed on an "as is" basis,
#  without warranties or conditions of any kind, either express or implied.
#  see the license for the specific language governing permissions and
#  limitations under the license.

import collections
import json

import paramiko

from . import ports
from . import routing


def setup(config):
    configs_by_nets = collections.defaultdict(dict)

    for net_name, net_ports in ports.get_ports_by_nets(config):
        configs_by_nets[net_name]['ports'] = net_ports
    for net_name, net_routes in routing.get_routes_by_nets(config):
        configs_by_nets[net_name]['routes'] = net_routes

    ips_by_nets = {
        net['name']: '172.16.1.{}'.format(i+2)
        for i, net in config['networks']['networks']}

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for net_name, config in configs_by_nets.items():
        ssh.connect(ips_by_nets[net_name])
        try:
            stdin, stdout, stderr = ssh.exec_command('cat')
            json.dump(config, stdin)
            stdin.close()
            print(stdout.read())
            print(stderr.read())
        finally:
            ssh.close()
