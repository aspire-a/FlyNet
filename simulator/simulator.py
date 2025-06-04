import random
import numpy as np
from phy.channel import Channel
from entities.node import Node
from simulator.metrics import Metrics
from mobility import start_coords
from utils import config
from visualization.scatter import scatter_plot


class Simulator:
    """
    Description: simulation environment

    Attributes:
        env: simpy environment
        total_simulation_time: discrete time steps, in nanosecond
        n_drones: number of the drones
        channel_states: a dictionary, used to describe the channel usage
        channel: wireless channel
        metrics: Metrics class, used to record the network performance
        drones: a list, contains all drone instances

    """

    def __init__(self,
                 seed,
                 env,
                 channel_states,
                 n_nodes,
                 total_simulation_time=config.SIM_TIME):

        self.env = env
        self.seed = seed
        self.total_simulation_time = total_simulation_time  # total simulation time (ns)

        self.n_nodes = n_nodes  # total number of drones in the simulation
        self.channel_states = channel_states
        self.channel = Channel(self.env)

        self.metrics = Metrics(self)  # use to record the network performance

        start_position = start_coords.get_random_start_point_3d(seed)

        self.drones = [] # the name is drones but it contains drones and sensor nodes
        sensor_drone_flag=0  # 0 means sensor, 1 means drone
        for i in range(n_nodes):

            
            
            if config.HETEROGENEOUS:
                speed = random.randint(5, 60)
            else:
                speed = 20 # we will have a constant speed for all drones.

            # change this depending on how many drones you want, here I am creating five drones and the rest are sensors
            if n_nodes-i <= 5: 
                sensor_drone_flag=1
                print('Drone: ', i, ' initial location is at: ', start_position[i])

            else:
                print('Sensor Node: ', i, ' initial location is at: ', start_position[i])

            node = Node(env=env, node_id=i, coords=start_position[i], speed=speed,
                          inbox=self.channel.create_inbox_for_receiver(i), simulator=self,sensor_drone_flag=sensor_drone_flag)
            self.drones.append(node)

        scatter_plot(self)

        self.env.process(self.show_performance())
        self.env.process(self.show_time())

    def show_time(self):
        while True:
            print('At time: ', self.env.now / 1e6, ' s.')
            yield self.env.timeout(0.5*1e6)  # the simulation process is displayed every 0.5s

    def show_performance(self):

        yield self.env.timeout(self.total_simulation_time - 1)

        scatter_plot(self)

        self.metrics.print_metrics()

        # ─── TASK 1: generate & save all basic‐stats plots (if enabled) ───
        self.metrics.plot_basic_stats()

        """

        You can use these lines instead to print the network metrics every n seconds instead of the end only. 
        For example here, every 99.9 seconds or 100 seconds. Keep it at 99.9 to have the end metrics displayed
        before the simulation ends
        
        while True:
            yield self.env.timeout(99.9*1e6)
            self.metrics.print_metrics()
       """