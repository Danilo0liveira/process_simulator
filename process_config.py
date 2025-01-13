
# Model

from models.ph import pH_model

process_name = 'pH Neutralization'
process_model = pH_model

# Preocess Dimensions

num_in = 1
num_out = 1
num_dist = 1

# Steady State Data

wa1s = 3e-3
wa2s = -3e-2
wa3s = -3.05e-3
wa4s = -4.32e-4

wb1s = 0
wb2s = 3e-2
wb3s = 5e-5
wb4s = 5.28e-4

q1s = 16.6
q2s = 0.55
q3s = 15.6
pHins = 0

hs = 14

# Initial Conditions

state = [hs, wa4s, wb4s, pHins]
MV = [q3s]
PV = hs

