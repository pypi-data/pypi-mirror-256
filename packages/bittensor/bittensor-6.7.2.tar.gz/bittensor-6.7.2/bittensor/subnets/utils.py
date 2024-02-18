import json
import torch

from bittensor import metagraph
from bittensor.chain_data import AxonInfo

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
    metagraph_obj = metagraph(
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
        AxonInfo.from_string(axon_data) for axon_data in data["axons"]
    ]

    return metagraph_obj
