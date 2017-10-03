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

from subprocess import check_call

# TODO: support editting
def setup_routes(routes):
    for route in routes:
        _add_route(route)


def _add_route(route):
    check_call([
        'ip', 'route', 'add',
        route['to'],
        'dev', route['dev'],
        'metric', route['metric']
    ])
