#  Copyright 2017 kypo-net authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import collections


def get_ports_by_nets(config):
    ports_by_nets = {}

    config_nets = config['networks']['networks']
    config_routes = config['routes']['routes']
    config_hosts = config['hosts']['hosts']

    number_of_routes_per_net = _get_number_of_routes_per_net(config_routes)
    number_of_hosts_per_net = _get_number_of_hosts_per_net(config_hosts)
    for net in config_nets:
        net_name = net['name']
        ports_by_nets[net_name] = []
        start_index = number_of_routes_per_net[net_name] + 1
        end_index = start_index + number_of_hosts_per_net[net_name] - 1
        for i in range(start_index, end_index+1):
            ports_by_nets[net_name].append('eth{}'.format(i))

    return ports_by_nets


def _get_number_of_routes_per_net(config_routes):
    number_of_routes_per_net = collections.defaultdict(lambda: 0)
    for route in config_routes:
        number_of_routes_per_net[route['lan1']] += 1
        number_of_routes_per_net[route['lan2']] += 1
    return number_of_routes_per_net


def _get_number_of_hosts_per_net(config_hosts):
    number_of_hosts_per_net = collections.defaultdict(lambda: 0)
    for host in config_hosts:
        number_of_hosts_per_net[host['lan']] += 1
    return number_of_hosts_per_net
