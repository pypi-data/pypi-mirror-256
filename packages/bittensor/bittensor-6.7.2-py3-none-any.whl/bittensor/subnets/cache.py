import json
import torch
import time
import functools
import threading
from os import getenv
from redis import StrictRedis
from datetime import datetime

import bittensor as bt
from bittensor import __ss58_format__ as ss58_format, __type_registry__ as type_registry
from bittensor import (
    __finney_entrypoint__,
    __local_entrypoint__,
    __finney_test_entrypoint__,
)

from typing import List, Dict, Any, Optional, Union

bt.trace()

redis_db = None
subtensor = None
sync_thread = None

METAGRAPH_ATTRIBUTES = [
    "n",
    "block",
    "uids",
    "stake",
    "total_stake",
    "ranks",
    "trust",
    "consensus",
    "validator_trust",
    "incentive",
    "emission",
    "dividends",
    "active",
    "last_update",
    "validator_permit",
    "weights",
    "bonds",
]


def get_subtensor(network: str = "local"):
    return bt.subtensor(network)


def get_database() -> StrictRedis:
    host = getenv("REDIS_HOST") or "localhost"
    port = getenv("REDIS_PORT") or 6379
    db = getenv("REDIS_DB") or 10
    return StrictRedis(host=host, port=port, db=db) if redis_db == None else redis_db


def startup(network: str = "local"):
    global redis_db
    global subtensor

    if subtensor is not None:
        subtensor.close()

    redis_db = get_database()
    subtensor = get_subtensor(network)


def store_metagraph_in_redis(metagraph):
    db = get_database()
    serialized_data = serialize_metagraph(metagraph)

    for attr, value in serialized_data.items():
        db.hset(f"metagraph:{metagraph.netuid}", attr, json.dumps(value))

    db.set(f"metagraph:{metagraph.netuid}:updated", time.time())


def retrieve_metagraph_from_redis(netuid: int):
    db = get_database()
    redis_key = f"metagraph:{netuid}"
    data = {
        attr.decode(): json.loads(db.hget(redis_key, attr))
        for attr in db.hkeys(redis_key)
    }
    return deserialize_metagraph(data)


def get_metagraph(netuid: int) -> "bt.metagraph":
    key = f"metagraph:{netuid}"
    if redis_db.exists(key):
        return retrieve_metagraph_from_redis(netuid)
    return subtensor.metagraph(netuid)


def get_available_redis_metagraphs():
    keys = redis_db.keys("metagraph:*")
    return [int(key.decode().split(":")[1]) for key in keys]


def retrieve_all_metagraphs_from_redis(netuids=None):
    if netuids is None:
        netuids = get_available_redis_metagraphs()
    return {netuid: retrieve_metagraph_from_redis(netuid) for netuid in netuids}


def serialize_metagraph(metagraph_obj, dump=False):
    serialized_data = {}
    for attr in METAGRAPH_ATTRIBUTES:
        tensor = getattr(metagraph_obj, attr, None)
        if tensor is not None:
            serialized_data[attr] = tensor.cpu().numpy().tolist()

    serialized_data["netuid"] = metagraph_obj.netuid
    serialized_data["network"] = metagraph_obj.network
    serialized_data["version"] = metagraph_obj.version.item()
    serialized_data["axons"] = [axon.to_string() for axon in metagraph_obj.axons]
    serialized_data["netuid"] = metagraph_obj.netuid

    return json.dumps(serialized_data) if dump else serialized_data


def deserialize_metagraph(serialized_str):
    if isinstance(serialized_str, str):
        data = json.loads(serialized_str)
    else:
        data = serialized_str
    metagraph_obj = bt.metagraph(
        netuid=data["netuid"], network=data["network"], lite=False, sync=False
    )
    metagraph_obj.version = torch.nn.Parameter(
        torch.tensor([data["version"]], dtype=torch.int64), requires_grad=False
    )

    for attr in METAGRAPH_ATTRIBUTES:
        if attr in data:
            setattr(
                metagraph_obj,
                attr,
                torch.nn.Parameter(torch.tensor(data[attr]), requires_grad=False),
            )

    metagraph_obj.axons = [
        bt.chain_data.AxonInfo.from_string(axon_data) for axon_data in data["axons"]
    ]

    return metagraph_obj


def fetch_metagraphs(netuids=None):
    for netuid in netuids:
        bt.logging.debug(f"Fetching metagraph for netuid: {netuid}")
        yield netuid, subtensor.metagraph(netuid)


def init_redis_global_metagraph(netuids=None):
    metagraphs = fetch_metagraphs(netuids)
    for netuid, metagraph in metagraphs:
        store_metagraph_in_redis(metagraph)


def update_metagraphs():
    metagraphs = retrieve_all_metagraphs_from_redis()
    for netuid, metagraph in metagraphs.items():
        bt.logging.debug(f"syncing {metagraph.netuid} | {subtensor.network}...")
        if redis_db.get(f"metagraph:{metagraph.netuid}:updated") is not None:
            last_update = float(redis_db.get(f"metagraph:{metagraph.netuid}:updated"))
            if last_update + 60 * 60 * 24 > time.time():
                bt.logging.debug(f"Skipping sync for {metagraph.netuid}...")
                continue
        if subtensor.network == metagraph.network:
            metagraph.sync(subtensor=subtensor, lite=True)
        else:
            metagraph = subtensor.metagraph(netuid)
        bt.logging.debug(f"storing {metagraph.netuid} in redis...")
        store_metagraph_in_redis(metagraph)


def periodic_sync_metagraphs(interval: int = 30):
    global sync_thread
    while sync_thread is not None:
        bt.logging.trace(f"Sleeping sync for {interval} seconds...")
        time.sleep(interval)
        update_metagraphs()


def run_sync_in_background_thread(interval: int = 60 * 60 * 2):
    """
    Starts the API's operations in a separate background thread.
    This is useful for non-blocking operations.
    """
    global sync_thread
    bt.logging.debug("Starting API background service in separate thread.")
    wrapped_sync = functools.partial(periodic_sync_metagraphs, interval=interval)
    sync_thread = threading.Thread(target=wrapped_sync, daemon=True)
    sync_thread.start()
    bt.logging.debug("Started")


def stop_sync_thread():
    """
    Stops the API's operations that are running in the background thread.
    """
    global sync_thread
    bt.logging.debug("Stopping API in background thread.")
    sync_thread.join(5)
    sync_thread = None
    bt.logging.debug("Stopped")


def start(network: str = "local", netuids: List[int] = None, interval: int = 180):
    startup(network)

    stored_netuids = get_available_redis_metagraphs()
    if netuids is not None:
        if not all([netuid in stored_netuids for netuid in netuids]):
            bt.logging.debug(
                f"Not all passed netuids in stored metagraphs. Fetching: {netuids}"
            )
            init_redis_global_metagraph(netuids)
        else:
            bt.logging.debug(
                f"All passed netuids in stored metagraphs... skipping fetch"
            )
    else:
        netuids = subtensor.get_all_subnet_netuids()
        bt.logging.info(f"Initializing global metagraph for all netuids...")
        init_global_redis_metagraph(netuids)

    run_sync_in_background_thread(interval)
