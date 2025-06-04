#---------------question 1------------------#
import numpy as np, random, math
from utils import config

def sample_packet_attributes():
    """Return (pkt_type, size_MB, priority) matching the spec."""
    pkt_type = random.choices(config.PKT_TYPE_PMF,
                              weights=config.PKT_TYPE_PROB)[0]

    if pkt_type == 'text':
        size = random.uniform(0.05, 0.20)
    elif pkt_type == 'image':
        # log-normal with mean=1 MB, σ=0.5 MB (use μ, σ in *linear* scale)
        size = np.random.lognormal(mean=math.log(1),
                                   sigma=0.5)
    else:                           # video
        size = max(0.001,
                   random.normalvariate(6, 1))   # truncate at 0

    prio = config.PRIORITY_MAP[pkt_type]
    return pkt_type, size, prio