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

import ipaddress

from dijkstar import Graph
from dijkstar.algorithm import extract_shortest_path_from_predecessor_list
from dijkstar.algorithm import single_source_shortest_paths


# set all possible routes, not the shortest one only
def get_routes_by_nets(nets, links):
    routes_by_nets = {}

    nets_by_ids = {net['connectable_id']: net for net in nets}

    graph = _get_graph(set(nets_by_ids), links)

    for net_id in nets_by_ids:
        neighs_routes = []
        nets_routes = []

        predecessors_map = single_source_shortest_paths(graph, net_id)

        for dest_net_id in nets_by_ids:
            if dest_net_id == net_id:
                continue
            try:
                shortest_path = extract_shortest_path_from_predecessor_list(
                    predecessors_map, dest_net_id)
            except KeyError:  # no route to destination
                continue
            next_hop_net_id = shortest_path[0][1]
            total_cost = shortest_path[3]
            if dest_net_id == next_hop_net_id:
                neighs_routes.append({
                    'to': _get_route_neigh_to(nets_by_ids[dest_net_id]),
                    'dev': _get_route_dev(next_hop_net_id, net_id, links),
                    'metric': total_cost
                })
            nets_routes.append({
                'to': _get_route_to(nets_by_ids[dest_net_id]),
                'via': _get_route_via(nets_by_ids[next_hop_net_id]),
                'metric': total_cost
            })

        routes_by_nets[net_id] = neighs_routes + nets_routes

    return routes_by_nets


def _get_graph(nets_ids, links):
    graph = Graph()
    for link in links:
        src_connectable_id = link['src_connectable_id']
        dst_connectable_id = link['dst_connectable_id']
        if src_connectable_id in nets_ids and dst_connectable_id in nets_ids:
            graph.add_edge(src_connectable_id, dst_connectable_id, 100)
    return graph


def _get_route_neigh_to(next_hop_net):
    return _get_first_host_addr(next_hop_net['cidr4'])


def _get_route_to(net):
    return net['cidr4']


def _get_route_dev(next_hop_net_id, net_id, links):
    i = 0
    for link in links:
        src_connectable_id = link['src_connectable_id']
        dst_connectable_id = link['dst_connectable_id']
        if src_connectable_id == net_id:
            i += 1
            if dst_connectable_id == next_hop_net_id:
                return 'eth{}'.format(i)


def _get_route_via(next_hop_net):
    return _get_first_host_addr(next_hop_net['cidr4'])


def _get_first_host_addr(subnet):
    net = ipaddress.ip_network(subnet)
    return str(next(net.hosts()))
