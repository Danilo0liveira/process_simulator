import opcua
import opcua.client
import opcua.ua
import matplotlib.pyplot as plt
import numpy as np

from process_config import *

fig, ax = plt.subplots()
line, = ax.plot([], [])

ax.set_xlabel('Tempo [s]')
ax.set_ylabel('pH')

def update_plot():
    line.set_xdata(time[:k+1])
    line.set_ydata(pvt[0, :k+1])

    ax.relim()
    ax.autoscale_view(True, True, True)

    fig.canvas.draw()
    fig.canvas.flush_events()
    
# SIMULATION CODE

tmax = 20000 # simulation duration time
ts = 5 # sampling time
sim_speed = 0.1 # simulation speed

# OPC CONFIGURATION

server_host = 'localhost'
server_port = '48040'

ua_client = opcua.Client('opc.tcp://'+server_host+':'+server_port)
ua_client.connect()

namespace_index = ua_client.get_namespace_index('http://liec.ufcg.edu.br/Server200/')

MV_node = [ua_client.get_node(f"ns={namespace_index}; s=Processo10"+str(i+1)+".MVEscrita") for i in range(num_out)]
PV_node = [ua_client.get_node(f"ns={namespace_index}; s=Processo10"+str(i+1)+".PV") for i in range(num_in)]

# SIMULATION LOOP

time = np.arange(0, tmax, ts)
mvt = np.zeros(shape=(num_out, time.size))
pvt = np.zeros(shape=(num_in, time.size))

for k in range(time.size):

    MV = np.array([MV_node[i].get_value() for i in range(num_out)])
    [PV_node[i].set_value(opcua.ua.DataValue(opcua.ua.Variant(PV, opcua.ua.VariantType.Double))) for i in range(num_in)]

    mvt[:, k] = MV + np.array([q1s, q2s, q3s])
    pvt[:, k] = PV

    PV, state = process_model(mvt[:,k], state, time[k], ts)
    
    update_plot()
    plt.pause(ts*sim_speed)

ua_client.disconnect()
plt.ioff()
plt.show()