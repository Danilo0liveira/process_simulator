import opcua
import numpy as np
import opcua.client

from time import sleep

from process_config import *

# SIMULATION CODE

tmax = 2000 # simulation duration time
ts = 5 # sampling time
sim_speed = 1 # simulation speed

# OPC CONFIGURATION

server_host = 'localhost'
server_port = '48040'

ua_client = opcua.Client('opc.tcp://'+server_host+':'+server_port)
ua_client.connect()

MV_node = ua_client.get_node(ua_client.get_namespace_index(), 'MV')
PV_node = ua_client.get_node(ua_client.get_namespace_index(), 'PV')

# SIMULATION LOOP

time = np.arange(0, tmax, ts)
mvt = np.zeros(num_in + num_out, time.size)
pvt = np.zeros(num_in + num_out, time.size)


for k in range(time.size):

    MV = MV_node.get_value()
    PV_node.set_value(PV)

    mvt[:, k] = MV + [q3s]
    pvt[:, k] = PV

    PV, state = process_model(mvt[:, k], state, time[k], ts)

    sleep(ts*sim_speed)

ua_client.disconnect()