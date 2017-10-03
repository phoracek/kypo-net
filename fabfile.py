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

import os

from fabric.api import task, hosts, execute, local, put, env, run, runs_once, lcd, cd


def _get_hosts(sandbox_name, ssh_config_path):
    master_host = None
    network_hosts = []

    with open(ssh_config_path) as ssh_config_file:
        ssh_config = ssh_config_file.readlines()

    for line in ssh_config:
        if not line.startswith('Host'):
            continue
        options = line.split()[1:]
        host_name = options[0]
        if host_name == sandbox_name:
            master_host = host_name
        elif host_name.startswith(sandbox_name):
            ip = options[1]
            if ip.startswith('172.16.1.'):
                network_hosts.append(host_name)

    return master_host, network_hosts


master_host, network_hosts = _get_hosts(
    os.environ['SANDBOX_NAME'],
    os.environ['SSH_CONFIG']
)

env.use_ssh_config = True


@task
def deploy():
    execute(deploy_master)
    execute(deploy_client)


@task
@hosts(master_host or [])
def deploy_master():
    with lcd('master'):
        tarball = execute(_package_master)['<local-only>']
        run('rm -rf /tmp/kyponet_master_dist')
        run('mkdir /tmp/kyponet_master_dist')
        with cd('/tmp/kyponet_master_dist'):
            put(tarball, 'kyponet-master.tar.gz')
            run('pip3 install --upgrade --force-reinstall '
                'kyponet-master.tar.gz')


@runs_once
def _package_master():
    local('rm -rf /tmp/kyponet_master_dist')
    local('python3 setup.py sdist --dist-dir /tmp/kyponet_master_dist')
    tarball = local(
        'find /tmp/kyponet_master_dist', capture=True).split('\n')[1]
    return tarball


@task
@hosts(network_hosts)
def deploy_client():
    with lcd('client'):
        tarball = execute(_package_client)['<local-only>']
        run('rm -rf /tmp/kyponet_client_dist')
        run('mkdir /tmp/kyponet_client_dist')
        with cd('/tmp/kyponet_client_dist'):
            put(tarball, 'kyponet-client.tar.gz')
            run("""
                tar -xvf kyponet-client.tar.gz;
                cd kyponet-client-*;
                python setup.py install
            """)


@runs_once
def _package_client():
    local('rm -rf /tmp/kyponet_client_dist')
    local('python3 setup.py sdist --dist-dir /tmp/kyponet_client_dist')
    tarball = local(
        'find /tmp/kyponet_client_dist', capture=True).split('\n')[1]
    return tarball
