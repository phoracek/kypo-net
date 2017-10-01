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

from dijkstar import Graph
from dijkstar.algorithm import extract_shortest_path_from_predecessor_list
from dijkstar.algorithm import single_source_shortest_paths


def get_routes_by_nets(config):
    routes_by_nets = {}

    config_nets = config['networks']['networks']
    config_routes = config['routes']['routes']

    graph = _get_graph(config['routes']['routes'])
    nets_by_names = {
        net['name']: net for net in config_nets}

    for net_name in nets_by_names:
        predecessors_map = single_source_shortest_paths(graph, net_name)
        routes_by_nets[net_name] = []

        for dest_net_name in nets_by_names:
            if dest_net_name == net_name:
                continue
            try:
                shortest_path = extract_shortest_path_from_predecessor_list(
                    predecessors_map, dest_net_name)
            except KeyError:  # no route to destination
                continue
            next_hop_net = shortest_path[0][1]
            total_cost = shortest_path[3]
            routes_by_nets[net_name].append({
                'to': _get_route_to(nets_by_names[dest_net_name]),
                'dev': _get_route_dev(next_hop_net, config_routes),
                'metric': total_cost
            })

    return routes_by_nets


def _get_graph(config_routes):
    graph = Graph()
    for route in config_routes:
        graph.add_edge(route['lan1'], route['lan2'], route.get('metric', 100))
        graph.add_edge(route['lan2'], route['lan1'], route.get('metric', 100))
    return graph


def _get_route_to(net):
    return '{}/{}'.format(net['ip'], net['prefix'])


def _get_route_dev(next_hop_net_name, config_routes):
    for i, route in enumerate(config_routes):
        if next_hop_net_name in (route['lan1'], route['lan2']):
            return 'eth{}'.format(i + 1)
