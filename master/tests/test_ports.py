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
        },
        'hosts': {
            'hosts': [
                {
                    'name': 'host4',
                    'lan': 'lan4',
                    'ip': '10.0.4.2',
                    'physRole': 'desktop'
                },
                {
                    'name': 'host1',
                    'lan': 'lan1',
                    'ip': '10.0.1.2',
                    'physRole': 'desktop',
                    'logicalRole': 'victim',
                    'ram': 1024
                },
                {
                    'name': 'host2',
                    'lan': 'lan2',
                    'ip': '10.0.2.2',
                    'physRole': 'desktop'
                },
                {
                    'name': 'host5',
                    'lan': 'lan4',
                    'ip': '10.0.4.3',
                    'physRole': 'desktop'
                }
            ]
        }
    }
    expected_ports_by_nets = {
        'lan2': ['eth3'],
        'lan4': ['eth2', 'eth3'],
        'lan1': ['eth2'],
        'lan3': []
    }
    ports_by_nets = ports.get_ports_by_nets(config)
    assert ports_by_nets == expected_ports_by_nets
