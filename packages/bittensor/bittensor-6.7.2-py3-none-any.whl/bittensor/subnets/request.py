import torch
import bittensor as bt
from typing import List, Optional, Any, Union, Dict


async def ping_uids(dendrite, metagraph, uids, timeout=3):
    """
    Pings a list of UIDs to check their availability on the Bittensor network.

    Args:
        dendrite (bittensor.dendrite): The dendrite instance to use for pinging.
        metagraph (bittensor.metagraph): The metagraph instance containing network information.
        uids (list): A list of UIDs (unique identifiers) to ping.
        timeout (int, optional): The timeout in seconds for each ping. Defaults to 3.

    Returns:
        tuple: A tuple containing two lists:
            - The first list contains UIDs that were successfully pinged.
            - The second list contains UIDs that failed to respond.
    """
    axons = [metagraph.axons[uid] for uid in uids]
    try:
        responses = await dendrite(
            axons,
            bt.Synapse(),  # TODO: potentially get the synapses available back?
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


async def get_query_api_nodes(dendrite, metagraph, n=0.1, timeout=3):
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
    bt.logging.debug(f"Fetching available API nodes for subnet {metagraph.netuid}")
    vtrust_uids = [
        uid.item() for uid in metagraph.uids if metagraph.validator_trust[uid] > 0
    ]
    top_uids = torch.where(metagraph.S > torch.quantile(metagraph.S, 1 - n))
    top_uids = top_uids[0].tolist()
    init_query_uids = set(top_uids).intersection(set(vtrust_uids))
    query_uids, _ = await ping_uids(
        dendrite, metagraph, init_query_uids, timeout=timeout
    )
    bt.logging.debug(
        f"Available API node UIDs for subnet {metagraph.netuid}: {query_uids}"
    )
    if len(query_uids) > 3:
        query_uids = random.sample(query_uids, 3)
    return query_uids


async def get_query_api_axons(dendrite, metagraph, n=0.1, timeout=3, uid=None):
    """
    Retrieves the axons of query API nodes based on their availability and stake.

    Args:
        dendrite (bittensor.dendrite): The dendrite instance to use for querying.
        metagraph (bittensor.metagraph): The metagraph instance containing network information.
        n (float, optional): The fraction of top nodes to consider based on stake. Defaults to 0.1.
        timeout (int, optional): The timeout in seconds for pinging nodes. Defaults to 3.
        uid (int, optional): The specific UID of the API node to query. Defaults to None.

    Returns:
        list: A list of axon objects for the available API nodes.
    """
    if uid is not None:
        query_uids = [uid]
    else:
        query_uids = await get_query_api_nodes(
            dendrite, metagraph, n=n, timeout=timeout
        )
    return [metagraph.axons[uid] for uid in query_uids]


async def query_api(
    dendrite: bt.dendrite,
    metagraph: bt.metagraph,
    prepare_synapse_fn: callable,
    process_responses_fn: callable,
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
        metagraph (bittensor.metagraph): The metagraph instance containing network information.
        prepare_synapse_fn (callable): A function to prepare the synapse for the subnet.
        process_responses_fn (callable): A function to process the responses from the subnet.
        deserialize (bool, optional): Whether to deserialize the responses. Defaults to False.
        timeout (int, optional): The timeout in seconds for the query. Defaults to 12.
        n (float, optional): The fraction of top nodes to consider based on stake. Defaults to 0.1.
        uid (int, optional): The specific UID of the API node to query. Defaults to None.
        **kwargs: Keyword arguments for the prepare_synapse_fn.

    Returns:
        Any: The result of the process_responses_fn.
    """
    synapse = prepare_synapse_fn(**kwargs)
    axons = await get_query_api_axons(
        dendrite=dendrite, metagraph=metagraph, n=n, timeout=timeout, uid=uid
    )
    bt.logging.debug(
        f"Quering valdidator axons with synapse {synapse.name} for subnet {metagraph.netuid}..."
    )
    responses = await dendrite(
        axons=axons,
        synapse=synapse,
        deserialize=deserialize,
        timeout=timeout,
    )
    return process_responses_fn(responses)
