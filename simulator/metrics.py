import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from datetime import datetime


class Metrics:
    """
    Tools for statistics of network performance

    1. Packet Delivery Ratio (PDR): is the ratio of number of packets received at the destinations to the number
       of packets sent from the sources
    2. Average end-to-end (E2E) delay: is the time a packet takes to route from a source to its destination through
       the network. It is the time the data packet reaches the destination minus the time the data packet was generated
       in the source node
    3. Routing Load: is calculated as the ratio between the numbers of control Packets transmitted
       to the number of packets actually received. NRL can reflect the average number of control packets required to
       successfully transmit a data packet and reflect the efficiency of the routing protocol
    4. Throughput: it can be defined as a measure of how fast the data is sent from its source to its intended
       destination without loss. In our simulation, each time the destination receives a data packet, the throughput is
       calculated and finally averaged
    5. Hop count: used to record the number of router output ports through which the packet should pass.

    References:
        [1] Rani. N, Sharma. P, Sharma. P., "Performance Comparison of Various Routing Protocols in Different Mobility
            Models," in arXiv preprint arXiv:1209.5507, 2012.
        [2] Gulati M K, Kumar K. "Performance Comparison of Mobile Ad Hoc Network Routing Protocols," International
            Journal of Computer Networks & Communications. vol. 6, no. 2, pp. 127, 2014.

    """

    def __init__(self, simulator):
        self.simulator = simulator

        self.control_packet_num = 0

        self.datapacket_generated = set()  # all data packets generated
        self.datapacket_arrived = set()  # all data packets that arrives the destination
        self.datapacket_generated_num = 0

        self.delivery_time = []
        self.deliver_time_dict = defaultdict()

        self.throughput = []
        self.throughput_dict = defaultdict()

        self.hop_cnt = []
        self.hop_cnt_dict = defaultdict()

        self.mac_delay = []

        self.collision_num = 0

        # --------added for priority queue--------
        self._dynamic = defaultdict(int)

        # --------added for task 2 metricss--------
        # Holds tuples of (node_id, timestamp, queue_length)
        self.queue_length_log = []

        # Maps priority → list of “delay”s (in simulation time units)
        self.delay_by_priority = defaultdict(list)
        # --------end of task 2 metricss--------


# --------same added for priority queue--------

def count(self, key: str, delta: int = 1) -> int:
    """
    Increase metric *key* by *delta* (default = 1) and return
    the updated value.

    * If *key* is an explicit attribute of Metrics
      (`collision_num`, `datapacket_generated_num`, …) we update
      that attribute so legacy code keeps working.
    * Otherwise we store the value in an internal dict that holds
      all ad-hoc counters created at run-time.
    """
    if hasattr(self, key):
        new_val = getattr(self, key) + delta
        setattr(self, key, new_val)
        return new_val

    self._dynamic[key] += delta
    return self._dynamic[key]


# Optional convenience getter (handy for tests / logging)
def value(self, key: str, default: int = 0) -> int:
    if hasattr(self, key):
        return getattr(self, key)
    return self._dynamic.get(key, default)


# ------------------end------------


# ——————————————————————————————————————————————————————————————————————
# TASK 2: METHODS TO RECORD QUEUE‐LENGTH & PER‐PRIORITY DELAYS
# ——————————————————————————————————————————————————————————————————————

def record_queue_length(self, node_id, timestamp, queue_length):
    """
    Log a snapshot of (which node’s TX‐queue, when in sim-time, and the queue size).
    Appends a tuple (node_id, timestamp, queue_length) to self.queue_length_log.
    """
    self.queue_length_log.append((node_id, timestamp, queue_length))


def record_delay(self, priority, delay):
    """
    Given an integer priority (0 = highest …), record the per-packet delay.
    Appends 'delay' to self.delay_by_priority[priority].
    """
    self.delay_by_priority[priority].append(delay)


# ——————————————————————————————————————————————————————————————————————
# TASK 2: end
# ——————————————————————————————————————————————————————————————————————


def print_metrics(self):
    # calculate the average end-to-end delay
    for key in self.deliver_time_dict.keys():
        self.delivery_time.append(self.deliver_time_dict[key])

    for key2 in self.throughput_dict.keys():
        self.throughput.append(self.throughput_dict[key2])

    for key3 in self.hop_cnt_dict.keys():
        self.hop_cnt.append(self.hop_cnt_dict[key3])

    e2e_delay = np.mean(self.delivery_time) / 1e3  # unit: ms

    pdr = len(self.datapacket_arrived) / self.datapacket_generated_num * 100  # in %

    rl = self.control_packet_num / len(self.datapacket_arrived)

    throughput = np.mean(self.throughput) / 1e3  # in Kbps

    hop_cnt = np.mean(self.hop_cnt)

    average_mac_delay = np.mean(self.mac_delay)

    # Timestamp for results
    now = datetime.now()
    timestamp = now.strftime("%H-%M-%S_%d-%m-%Y")

    # Log results to a file
    with open("simulator/network_results.txt", "a") as file:
        file.write(f"{timestamp}\n")
        file.write(f"Total Arrived is: {len(self.datapacket_arrived)}\n")
        file.write(f"Totally sent: {self.datapacket_generated_num} data packets\n")
        file.write(f"Packet delivery ratio is: {pdr}%\n")
        file.write(f"Average end-to-end delay is: {e2e_delay} ms\n")
        file.write(f"Routing load is: {rl}\n")
        file.write(f"Average throughput is: {throughput} Kbps\n")
        file.write(f"Average hop count is: {hop_cnt}\n")
        file.write(f"Collision num is: {self.collision_num}\n")
        file.write(f"Average MAC delay is: {average_mac_delay} ms\n")
        file.write(f"--------------------------------------------\n")

    print('Totally send: ', self.datapacket_generated_num, ' data packets')
    print('Packet delivery ratio is: ', pdr, '%')
    print('Average end-to-end delay is: ', e2e_delay, 'ms')
    print('Routing load is: ', rl)
    print('Average throughput is: ', throughput, 'Kbps')
    print('Average hop count is: ', hop_cnt)
    print('Collision num is: ', self.collision_num)
    print('Average mac delay is: ', average_mac_delay, 'ms')
