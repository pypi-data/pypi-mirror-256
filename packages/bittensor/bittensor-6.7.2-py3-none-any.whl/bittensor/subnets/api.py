# The MIT License (MIT)
# Copyright © 2021 Yuma Rao
# Copyright © 2023 Opentensor Foundation
# Copyright © 2023 Opentensor Technologies Inc

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import time
import redis
import random
import bittensor as bt

from abc import ABC, abstractmethod
from typing import Any, List, Union, Optional, Tuple, Dict
from .utils import serialize_metagraph, deserialize_metagraph
from .registry import APIRegistry, register_handler


class SubnetsAPI(ABC):
    def __init__(
        self, wallet: "bt.wallet", network: str, netuids: List[int] = None, interval=60
    ):
        self.wallet = wallet
        self.dendrite = bittensor.dendrite(wallet=wallet)
        self.subtensor = bittensor.subtensor(network)

        host = getenv("REDIS_HOST") or "localhost"
        port = getenv("REDIS_PORT") or 6379
        db = getenv("REDIS_DB") or 10
        self.database = redis.StrictRedis(host=host, port=port, db=db)

        stored_netuids = self.get_available_redis_metagraph_netuids()
        if netuids is not None:
            if not all([netuid in stored_netuids for netuid in netuids]):
                bt.logging.debug(
                    f"Not all passed netuids in stored metagraphs. Fetching: {netuids}"
                )
                self.init_redis_global_metagraph(netuids)
            else:
                bt.logging.debug(
                    f"All passed netuids in stored metagraphs... skipping fetch"
                )
        else:
            netuids = self.subtensor.get_all_subnet_netuids()
            bt.logging.info(f"Initializing global metagraph for all netuids...")
            self.init_global_redis_metagraph(netuids)

        self.sync_thread = None
        self.sync_running = False
        self.update_interval = interval
        self.run_sync_in_background_thread()

    @abstractmethod
    def prepare_synapse(self, *args, **kwargs) -> Any:
        """
        Prepare the synapse-specific payload.
        """
        ...

    @abstractmethod
    def process_responses(self, responses: List[Union["bt.Synapse", Any]]) -> Any:
        """
        Process the responses from the network.
        """
        ...

    def __call__(self, *args, **kwargs):
        return self.query_api(*args, **kwargs)

    def fetch_metagraphs(self, netuids=None):
        for netuid in netuids:
            bt.logging.debug(f"Fetching metagraph for netuid: {netuid}")
            yield netuid, self.subtensor.metagraph(netuid)

    def store_metagraph_in_redis(self, metagraph: "bt.metagraph"):
        serialized_data = serialize_metagraph(metagraph)

        for attr, value in serialized_data.items():
            self.database.hset(f"metagraph:{metagraph.netuid}", attr, json.dumps(value))

        self.database.set(f"metagraph:{metagraph.netuid}:updated", time.time())

    def retrieve_metagraph_from_redis(self, netuid: int):
        redis_key = f"metagraph:{netuid}"
        data = {
            attr.decode(): json.loads(self.database.hget(redis_key, attr))
            for attr in self.database.hkeys(redis_key)
        }
        return deserialize_metagraph(data)

    def get_available_redis_metagraph_netuids(self):
        keys = self.database.keys("metagraph:*")
        return [int(key.decode().split(":")[1]) for key in keys]

    def retrieve_all_metagraphs_from_redis(self, netuids: Optional[List[int]] = None):
        if netuids is None:
            netuids = self.get_available_redis_metagraph_netuids()
        return {
            netuid: self.retrieve_metagraph_from_redis(netuid) for netuid in netuids
        }

    def init_redis_global_metagraph(self, netuids=None):
        metagraphs = self.fetch_metagraphs(netuids)
        for _, metagraph in metagraphs:
            self.store_metagraph_in_redis(metagraph)

    def update_metagraphs(self):
        metagraphs = self.retrieve_all_metagraphs_from_redis()
        for netuid, metagraph in metagraphs.items():
            bt.logging.debug(
                f"syncing {metagraph.netuid} | {self.subtensor.network}..."
            )
            if self.database.get(f"metagraph:{metagraph.netuid}:updated") is not None:
                last_update = float(
                    self.database.get(f"metagraph:{metagraph.netuid}:updated")
                )
                if last_update + self.update_interval > time.time():
                    bt.logging.debug(f"Skipping sync for {metagraph.netuid}...")
                    continue
            if self.subtensor.network == metagraph.network:
                metagraph.sync(subtensor=self.subtensor, lite=True)
            else:
                metagraph = self.subtensor.metagraph(netuid)
            bt.logging.debug(f"storing {metagraph.netuid} in redis...")
            self.store_metagraph_in_redis(metagraph)

    def periodic_sync_metagraphs(self):
        while self.sync_thread is not None and self.sync_running:
            bt.logging.trace(f"Sleeping sync for {interval} seconds...")
            time.sleep(self.update_interval)
            self.update_metagraphs()

    def run_sync_in_background_thread(self):
        """
        Starts the API's operations in a separate background thread.
        This is useful for non-blocking operations.
        """
        bt.logging.debug("Starting API background service in separate thread.")
        self.sync_thread = threading.Thread(
            target=periodic_sync_metagraphs, daemon=True
        )
        self.sync_thread.start()
        bt.logging.debug("Started")

    def stop_sync_thread(self):
        """
        Stops the API's operations that are running in the background thread.
        """
        bt.logging.debug("Stopping API in background thread.")
        self.sync_thread.join(5)
        self.sync_running = False
        self.sync_thread = None
        bt.logging.debug("Stopped")

    async def ping_uids(self, uids, netuid, timeout=3):
        """
        Pings a list of UIDs to check their availability on the Bittensor network.

        Args:
            uids (list): A list of UIDs (unique identifiers) to ping.
            netuid (int): The unique identifier of the subnet to ping.
            timeout (int, optional): The timeout in seconds for each ping. Defaults to 3.

        Returns:
            tuple: A tuple containing two lists:
                - The first list contains UIDs that were successfully pinged.
                - The second list contains UIDs that failed to respond.
        """
        # Fetch from redis
        metagraph = retrieve_metagraph_from_redis(netuid)

        axons = [metagraph.axons[uid] for uid in uids]
        try:
            responses = await self.dendrite(
                axons,
                bt.Synapse(),
                deserialize=False,
                timeout=timeout,
            )
            successful_uids = [
                uid
                for uid, response in zip(uids, responses)
                if response.dendrite.status_code == 200
            ]
            failed_uids = [
                uid
                for uid, response in zip(uids, responses)
                if response.dendrite.status_code != 200
            ]
        except Exception as e:
            bt.logging.error(f"Dendrite ping failed: {e}")
            successful_uids = []
            failed_uids = uids
        bt.logging.debug("ping() successful uids:", successful_uids)
        bt.logging.debug("ping() failed uids    :", failed_uids)
        return successful_uids, failed_uids

    async def get_query_api_nodes(self, netuid, n=0.1, timeout=3):
        """
        Fetches the available API nodes to query for the particular subnet.

        Args:
            dendrite (bittensor.dendrite): The dendrite instance to use for querying.
            metagraph (bittensor.metagraph): The metagraph instance containing network information.
            n (float, optional): The fraction of top nodes to consider based on stake. Defaults to 0.1.
            timeout (int, optional): The timeout in seconds for pinging nodes. Defaults to 3.

        Returns:
            list: A list of UIDs representing the available API nodes.
        """
        metagraph = retrieve_metagraph_from_redis(netuid)

        bt.logging.debug(f"Fetching available API nodes for subnet {metagraph.netuid}")
        vtrust_uids = [
            uid.item() for uid in metagraph.uids if metagraph.validator_trust[uid] > 0
        ]
        top_uids = torch.where(metagraph.S > torch.quantile(metagraph.S, 1 - n))
        top_uids = top_uids[0].tolist()
        init_query_uids = set(top_uids).intersection(set(vtrust_uids))
        query_uids, _ = await self.ping_uids(init_query_uids, netuid, timeout=timeout)
        bt.logging.debug(
            f"Available API node UIDs for subnet {metagraph.netuid}: {query_uids}"
        )
        if len(query_uids) > 3:
            query_uids = random.sample(query_uids, 3)
        return query_uids

    async def get_query_api_axons(self, netuid, n=0.1, timeout=3, uid=None):
        """
        Retrieves the axons of query API nodes based on their availability and stake.

        Args:
            netuid (int): The unique identifier of the subnet to query.
            n (float, optional): The fraction of top nodes to consider based on stake. Defaults to 0.1.
            timeout (int, optional): The timeout in seconds for pinging nodes. Defaults to 3.
            uid (int, optional): The specific UID of the API node to query. Defaults to None.

        Returns:
            list: A list of axon objects for the available API nodes.
        """
        metagraph = retrieve_metagraph_from_redis(netuid)

        if uid is not None:
            query_uids = [uid]
        else:
            query_uids = await self.get_query_api_nodes(netuid, n=n, timeout=timeout)
        return [metagraph.axons[uid] for uid in query_uids]

    async def query_api(
        self,
        netuid: int,
        deserialize: bool = False,
        timeout: int = 12,
        n: float = 0.1,
        uid: int = None,
        **kwargs: Any,
    ) -> Any:
        """
        Queries the API nodes of a subnet using the given synapse and bespoke query function.

        Args:
            dendrite (bittensor.dendrite): The dendrite instance to use for querying.
            deserialize (bool, optional): Whether to deserialize the responses. Defaults to False.
            timeout (int, optional): The timeout in seconds for the query. Defaults to 12.
            n (float, optional): The fraction of top nodes to consider based on stake. Defaults to 0.1.
            uid (int, optional): The specific UID of the API node to query. Defaults to None.
            **kwargs: Keyword arguments for the prepare_synapse_fn.

        Returns:
            Any: The result of the process_responses_fn.
        """
        synapse = self.prepare_synapse(**kwargs)
        axons = await self.get_query_api_axons(
            netuid=netuid, n=n, timeout=timeout, uid=uid
        )
        bt.logging.debug(
            f"Quering valdidator axons with synapse {synapse.name} for subnet {netuid}..."
        )
        responses = await self.dendrite(
            axons=axons,
            synapse=synapse,
            deserialize=deserialize,
            timeout=timeout,
        )
        return self.process_responses(responses)
