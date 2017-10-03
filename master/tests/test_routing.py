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

from kyponet_master import routing


def test_get_routes():
    nets = [
        {'connectable_id': 'lan2', 'cidr4': '10.0.2.0/24'},
        {'connectable_id': 'lan4', 'cidr4': '10.0.4.0/24'},
        {'connectable_id': 'lan1', 'cidr4': '10.0.1.0/24'},
        {'connectable_id': 'lan3', 'cidr4': '10.0.3.0/24'}
    ]
    links = [
        {'src_connectable_id': 'lan1', 'dst_connectable_id': 'lan2'},
        {'src_connectable_id': 'lan2', 'dst_connectable_id': 'lan1'},
        {'src_connectable_id': 'lan3', 'dst_connectable_id': 'lan2'},
        {'src_connectable_id': 'lan2', 'dst_connectable_id': 'lan3'},
        {'src_connectable_id': 'lan3', 'dst_connectable_id': 'lan4'},
        {'src_connectable_id': 'lan4', 'dst_connectable_id': 'lan3'}
    ]
    expected_routes_by_nets = {
        'lan2': [
            {
                'to': '10.0.1.1',
                'dev': 'eth1',
                'metric': 100
            },
            {
                'to': '10.0.3.1',
                'dev': 'eth2',
                'metric': 100
            },
            {
                'to': '10.0.4.0/24',
                'via': '10.0.3.1',
                'metric': 200
            },
            {
                'to': '10.0.1.0/24',
                'via': '10.0.1.1',
                'metric': 100
            },
            {
                'to': '10.0.3.0/24',
                'via': '10.0.3.1',
                'metric': 100
            }
        ],
        'lan4': [
            {
                'to': '10.0.3.1',
                'dev': 'eth1',
                'metric': 100
            },
            {
                'to': '10.0.2.0/24',
                'via': '10.0.3.1',
                'metric': 200
            },
            {
                'to': '10.0.1.0/24',
                'via': '10.0.3.1',
                'metric': 300
            },
            {
                'to': '10.0.3.0/24',
                'via': '10.0.3.1',
                'metric': 100
            }
        ],
        'lan1': [
            {
                'to': '10.0.2.1',
                'dev': 'eth1',
                'metric': 100
            },
            {
                'to': '10.0.2.0/24',
                'via': '10.0.2.1',
                'metric': 100
            },
            {
                'to': '10.0.4.0/24',
                'via': '10.0.2.1',
                'metric': 300
            },
            {
                'to': '10.0.3.0/24',
                'via': '10.0.2.1',
                'metric': 200
            }
        ],
        'lan3': [
            {
                'to': '10.0.2.1',
                'dev': 'eth1',
                'metric': 100
            },
            {
                'to': '10.0.4.1',
                'dev': 'eth2',
                'metric': 100
            },
            {
                'to': '10.0.2.0/24',
                'via': '10.0.2.1',
                'metric': 100
            },
            {
                'to': '10.0.4.0/24',
                'via': '10.0.4.1',
                'metric': 100
            },
            {
                'to': '10.0.1.0/24',
                'via': '10.0.2.1',
                'metric': 200
            }
        ]
    }
    routes_by_nets = routing.get_routes_by_nets(nets, links)
    assert routes_by_nets == expected_routes_by_nets
