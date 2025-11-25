#!/usr/bin/env python3
"""
Two neurons coupled via electrical synapse (gap junction)
Demonstrates instantaneous bidirectional coupling
"""
import neun_py
import matplotlib.pyplot as plt
import numpy as np

# Create two Hodgkin-Huxley neurons
neuron_args = neun_py.HHDoubleConstructorArgs()
h1 = neun_py.HHDoubleRK4(neuron_args)
h2 = neun_py.HHDoubleRK4(neuron_args)

# Set parameters for both neurons
for neuron in [h1, h2]:
    neuron.set_param(neun_py.HHDoubleParameter.cm, 1 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.vna, 50)
    neuron.set_param(neun_py.HHDoubleParameter.vk, -77)
    neuron.set_param(neun_py.HHDoubleParameter.vl, -54.387)
    neuron.set_param(neun_py.HHDoubleParameter.gna, 120 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.gk, 36 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.gl, 0.3 * 7.854e-3)

# Set different initial voltages
h1.set(neun_py.HHDoubleVariable.v, -75)
h2.set(neun_py.HHDoubleVariable.v, -65)

# Create electrical synapse with conductance
# Negative conductance values create the proper coupling
synapse = neun_py.ESynHHHHDoubleRK4(
    h1, neun_py.HHDoubleVariable.v,
    h2, neun_py.HHDoubleVariable.v,
    -0.002,  # Conductance from h1 to h2
    -0.002   # Conductance from h2 to h1
)

# Simulation parameters
step = 0.001  # ms
duration = 100  # ms

# Storage
times = []
v1_values = []
v2_values = []
synaptic_currents = []

# Run simulation
time = 0.0
while time < duration:
    # Step the synapse first (updates coupling)
    synapse.step(step)
    
    # Add external input only to first neuron
    h1.add_synaptic_input(0.1)
    
    # Step both neurons
    h1.step(step)
    h2.step(step)
    
    # Record data
    times.append(time)
    v1_values.append(h1.get(neun_py.HHDoubleVariable.v))
    v2_values.append(h2.get(neun_py.HHDoubleVariable.v))
    
    # Get synaptic current
    i_syn = synapse.get(neun_py.ESynDoubleVariable.i1)
    synaptic_currents.append(i_syn)
    
    time += step

# Plot results
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Membrane potentials
ax1.plot(times, v1_values, 'b-', label='Neuron 1 (with input)', linewidth=1.5)
ax1.plot(times, v2_values, 'r-', label='Neuron 2 (coupled)', linewidth=1.5)
ax1.set_ylabel('Membrane Potential (mV)')
ax1.set_title('Electrical Synapse: Bidirectional Coupling via Gap Junction')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Synaptic current
ax2.plot(times, synaptic_currents, 'g-', linewidth=1.5)
ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('Synaptic Current')
ax2.set_title('Coupling Current Through Gap Junction')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('electrical_synapse.pdf')
plt.show()
