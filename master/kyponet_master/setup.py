#  copyright 2017 kypo-net authors
#
#  licensed under the apache license, version 2.0 (the "license");
#  you may not use this file except in compliance with the license.
#  you may obtain a copy of the license at
#
#      http://www.apache.org/licenses/license-2.0
#
#  unless required by applicable law or agreed to in writing, software
#  distributed under the license is distributed on an "as is" basis,
#  without warranties or conditions of any kind, either express or implied.
#  see the license for the specific language governing permissions and
#  limitations under the license.

import collections
import contextlib
import json
import logging

import paramiko
import psycopg2

from . import ports
from . import routing


def setup(config):
    configs_by_nets = collections.defaultdict(dict)

    node_ifaces = config['node_interface']
    nets = config['network']
    links = config['link']

    for net_id, net_ports in ports.get_ports_by_nets(
            node_ifaces, nets, links).items():
        configs_by_nets[net_id]['ports'] = net_ports
    for net_id, net_routes in routing.get_routes_by_nets(nets, links).items():
        configs_by_nets[net_id]['routes'] = net_routes

    ips_by_nets_ids = {
        net['connectable_id']: '172.16.1.{}'.format(i + 2)
        for i, net in enumerate(nets)}

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for net_id, config in configs_by_nets.items():
        ssh.connect(ips_by_nets_ids[net_id])
        logging.info('Connected to %s via %s', net_id, ips_by_nets_ids[net_id])
        logging.info('Requesting config %s', config)
        try:
            stdin, stdout, stderr = ssh.exec_command('kyponet-client')
            json.dump(config, stdin)
            stdin.channel.shutdown_write()
            logging.info('Config setup finished with out: %s, err: %s',
                         stdout.read(), stderr.read())
        finally:
            ssh.close()


def get_config_from_db():
    config = {}
    with _connect_to_db() as conn:
        cursor = conn.cursor()
        config['node_interface'] = _get_node_interfaces_from_db(cursor)
        config['network'] = _get_nets_from_db(cursor)
        config['link'] = _get_links_from_db(cursor)
    return config


@contextlib.contextmanager
def _connect_to_db():
    conn = psycopg2.connect("dbname='kypodb' user='postgres' host='localhost'")
    try:
        yield conn
    finally:
        conn.close()


def _get_node_interfaces_from_db(cursor):
    cursor.execute("""
        SELECT connectable_id
        FROM node_interface
        ORDER BY connectable_id ASC
    """)
    net_rows = cursor.fetchall()
    return [{'connectable_id': row[0]} for row in net_rows]


def _get_nets_from_db(cursor):
    cursor.execute("""
        SELECT connectable_id, cidr4
        FROM network
        ORDER BY connectable_id ASC
    """)
    net_rows = cursor.fetchall()
    return [{'connectable_id': row[0], 'cidr4': row[1]} for row in net_rows]


def _get_links_from_db(cursor):
    cursor.execute("""
        SELECT src_connectable_id, dst_connectable_id
        FROM link
        ORDER BY measurable_id ASC
    """)
    net_rows = cursor.fetchall()
    return [
        {'src_connectable_id': row[0], 'dst_connectable_id': row[1]}
        for row in net_rows
    ]
