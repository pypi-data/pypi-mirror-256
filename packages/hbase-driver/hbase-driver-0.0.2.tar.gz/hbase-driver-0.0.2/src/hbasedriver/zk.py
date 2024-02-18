import logging
from struct import unpack

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
from kazoo.handlers.threading import KazooTimeoutError

from protobuf_py import ZooKeeper_pb2

logger = logging.getLogger('pybase.' + __name__)
logger.setLevel(logging.DEBUG)

znode = "/hbase"


# LocateMeta takes a string representing the location of the ZooKeeper
# quorum. It then asks ZK for the location of the MetaRegionServer,
# returning a tuple containing (host_name, port).
# i.e. this gets the master server.
def locate_meta(zkquorum: list, establish_connection_timeout=5, missing_znode_retries=5, zk=None):
    if type(zkquorum) != list:
        raise ValueError("must provide a list for zookeeper quorum.")
    if zk is None:
        # Using Kazoo for interfacing with ZK
        # todo: try all contact points.
        for host in zkquorum:
            zk = KazooClient(hosts=host, timeout=3)
    try:
        zk.start(timeout=establish_connection_timeout)
    except KazooTimeoutError:
        raise Exception("Cannot connect to ZooKeeper at {}".format(zkquorum[0]))
    # MetaRegionServer information is located at /hbase/meta-region-server
    try:
        rsp, znodestat = zk.get(znode + "/meta-region-server")
    except NoNodeError:
        logger.error("cant locate meta-region-server, zk has no such node. ")
        raise Exception("zk locate meta failed")

    zk.stop()
    if len(rsp) == 0:
        # Empty response is bad.
        raise Exception("ZooKeeper returned an empty response")
    # The first byte must be \xff.
    # 4 byte: length of id
    first_byte, id_length = unpack(">cI", rsp[:5])
    if first_byte != b'\xff':
        # Malformed response
        raise Exception(
            "ZooKeeper returned an invalid response")
    # skip bytes already read , id and an 8-byte long type salt.
    rsp = rsp[5 + id_length:]
    # data is prepended with PBMagic
    assert rsp[:4] == b'PBUF'
    rsp = rsp[4:]

    meta = ZooKeeper_pb2.MetaRegionServer()
    meta.ParseFromString(rsp)
    # here we got the master host and port.
    hostname = meta.server.host_name
    port = meta.server.port

    logger.info('Discovered Master at %s:%s', hostname, port)
    return hostname, port
