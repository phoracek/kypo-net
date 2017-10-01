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
    config = {
        'networks': {
            'networks': [
                {'name': 'lan2', 'ip': '10.0.2.0', 'prefix': 24},
                {'name': 'lan4', 'ip': '10.0.4.0', 'prefix': 24},
                {'name': 'lan1', 'ip': '10.0.1.0', 'prefix': 24},
                {'name': 'lan3', 'ip': '10.0.3.0', 'prefix': 24}
            ]
        },
        'routes': {
            'routes': [
                {'name': '', 'lan1': 'lan1', 'lan2': 'lan2'},
                {'name': '', 'lan1': 'lan3', 'lan2': 'lan2'},
                {'name': '', 'lan1': 'lan3', 'lan2': 'lan4'}
            ]
        }
    }
    expected_routes_by_nets = {
        'lan2': [
            {'to': '10.0.4.0/24', 'dev': 'eth2', 'metric': 200},
            {'to': '10.0.1.0/24', 'dev': 'eth1', 'metric': 100},
            {'to': '10.0.3.0/24', 'dev': 'eth2', 'metric': 100}
        ],
        'lan4': [
            {'to': '10.0.2.0/24', 'dev': 'eth2', 'metric': 200},
            {'to': '10.0.1.0/24', 'dev': 'eth2', 'metric': 300},
            {'to': '10.0.3.0/24', 'dev': 'eth2', 'metric': 100}
        ],
        'lan1': [
            {'to': '10.0.2.0/24', 'dev': 'eth1', 'metric': 100},
            {'to': '10.0.4.0/24', 'dev': 'eth1', 'metric': 300},
            {'to': '10.0.3.0/24', 'dev': 'eth1', 'metric': 200}
        ],
        'lan3': [
            {'to': '10.0.2.0/24', 'dev': 'eth1', 'metric': 100},
            {'to': '10.0.4.0/24', 'dev': 'eth3', 'metric': 100},
            {'to': '10.0.1.0/24', 'dev': 'eth1', 'metric': 200}
        ]
    }
    routes_by_nets = routing.get_routes_by_nets(config)
    assert routes_by_nets == expected_routes_by_nets
