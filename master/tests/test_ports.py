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

from kyponet_master import ports


def test_get_ports():
    node_ifaces = [
        {'connectable_id': 'host4'},
        {'connectable_id': 'host1'},
        {'connectable_id': 'host2'},
        {'connectable_id': 'host5'}
    ]
    nets = [
        {'connectable_id': 'lan2', 'cidr4': '10.0.2.0/24'},
        {'connectable_id': 'lan4', 'cidr4': '10.0.4.0/24'},
        {'connectable_id': 'lan1', 'cidr4': '10.0.1.0/24'},
        {'connectable_id': 'lan3', 'cidr4': '10.0.3.0/24'},
    ]
    links = [
        {'src_connectable_id': 'lan1', 'dst_connectable_id': 'lan2'},
        {'src_connectable_id': 'lan2', 'dst_connectable_id': 'lan1'},
        {'src_connectable_id': 'lan3', 'dst_connectable_id': 'lan2'},
        {'src_connectable_id': 'lan2', 'dst_connectable_id': 'lan3'},
        {'src_connectable_id': 'lan3', 'dst_connectable_id': 'lan4'},
        {'src_connectable_id': 'lan4', 'dst_connectable_id': 'lan3'},
        {'src_connectable_id': 'lan4', 'dst_connectable_id': 'host4'},
        {'src_connectable_id': 'host4', 'dst_connectable_id': 'lan4'},
        {'src_connectable_id': 'lan1', 'dst_connectable_id': 'host1'},
        {'src_connectable_id': 'host1', 'dst_connectable_id': 'lan1'},
        {'src_connectable_id': 'lan2', 'dst_connectable_id': 'host2'},
        {'src_connectable_id': 'host2', 'dst_connectable_id': 'lan2'},
        {'src_connectable_id': 'lan4', 'dst_connectable_id': 'host5'},
        {'src_connectable_id': 'host5', 'dst_connectable_id': 'lan4'}
    ]
    expected_ports_by_nets = {
        'lan2': ['eth3'],
        'lan4': ['eth2', 'eth3'],
        'lan1': ['eth2'],
        'lan3': []
    }
    ports_by_nets = ports.get_ports_by_nets(node_ifaces, nets, links)
    assert ports_by_nets == expected_ports_by_nets
