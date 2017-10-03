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


def get_ports_by_nets(node_ifaces, nets, links):
    ports_by_nets = {}

    node_ifaces_ids = {
        node_iface['connectable_id'] for node_iface in node_ifaces}
    nets_ids = {net['connectable_id'] for net in nets}

    number_of_routes_per_net = _get_number_of_routes_per_net(nets_ids, links)
    number_of_hosts_per_net = _get_number_of_hosts_per_net(
        node_ifaces_ids, nets_ids, links)
    for net_id in nets_ids:
        ports_by_nets[net_id] = []
        start_index = number_of_routes_per_net[net_id] + 1
        end_index = start_index + number_of_hosts_per_net[net_id] - 1
        for i in range(start_index, end_index + 1):
            ports_by_nets[net_id].append('eth{}'.format(i))

    return ports_by_nets


def _get_number_of_routes_per_net(nets_ids, links):
    number_of_routes_per_net = collections.defaultdict(lambda: 0)
    for link in links:
        src_connectable_id = link['src_connectable_id']
        dst_connectable_id = link['dst_connectable_id']
        if src_connectable_id in nets_ids and dst_connectable_id in nets_ids:
            number_of_routes_per_net[src_connectable_id] += 1
    return number_of_routes_per_net


def _get_number_of_hosts_per_net(node_ifaces_ids, nets_ids, links):
    number_of_hosts_per_net = collections.defaultdict(lambda: 0)
    for link in links:
        src_connectable_id = link['src_connectable_id']
        dst_connectable_id = link['dst_connectable_id']
        if (src_connectable_id in nets_ids and
                dst_connectable_id in node_ifaces_ids):
            number_of_hosts_per_net[src_connectable_id] += 1
    return number_of_hosts_per_net
