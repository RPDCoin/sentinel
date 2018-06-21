import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from rapidd import rapidDaemon
from rapid_config import rapidConfig


def test_rapidd():
    config_text = rapidConfig.slurp_config_file(config.rapid_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000003dc71373b2cb90c9bbd0e4bde5a6cc6013a4214eaea2cc8b71f9c68808d'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = rapidConfig.get_rpc_creds(config_text, network)
    rapidd = rapidDaemon(**creds)
    assert rapidd.rpc_command is not None

    assert hasattr(rapidd, 'rpc_connection')

    # rapid testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = rapidd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert rapidd.rpc_command('getblockhash', 0) == genesis_hash
