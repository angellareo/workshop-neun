#!/usr/bin/env python3
"""
Chain of neurons connected via electrical synapses
Demonstrates signal propagation through a network
"""
import neun_py
import matplotlib.pyplot as plt
import numpy as np

def create_hh_neuron(v_init=-65):
    """Helper function to create and initialize an HH neuron"""
    neuron_args = neun_py.HHDoubleConstructorArgs()
    neuron = neun_py.HHDoubleRK4(neuron_args)
    
    # Set parameters
    neuron.set_param(neun_py.HHDoubleParameter.cm, 1 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.vna, 50)
    neuron.set_param(neun_py.HHDoubleParameter.vk, -77)
    neuron.set_param(neun_py.HHDoubleParameter.vl, -54.387)
    neuron.set_param(neun_py.HHDoubleParameter.gna, 120 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.gk, 36 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.gl, 0.3 * 7.854e-3)
    
    # Set initial voltage
    neuron.set(neun_py.HHDoubleVariable.v, v_init)
    neuron.set(neun_py.HHDoubleVariable.m, 0.05)
    neuron.set(neun_py.HHDoubleVariable.h, 0.6)
    neuron.set(neun_py.HHDoubleVariable.n, 0.3)
    
    return neuron

# Create a chain of 4 neurons with different initial conditions
neurons = [
    create_hh_neuron(-70),
    create_hh_neuron(-68),
    create_hh_neuron(-66),
    create_hh_neuron(-64)
]

# Connect them in a chain with electrical synapses
synapses = []
for i in range(len(neurons) - 1):
    synapse = neun_py.ESynHHHHDoubleRK4(
        neurons[i], neun_py.HHDoubleVariable.v,
        neurons[i+1], neun_py.HHDoubleVariable.v,
        0.002, 0.002  # Bidirectional coupling
    )
    synapses.append(synapse)

# Simulation parameters
step = 0.001  # ms
duration = 150  # ms

# Storage
times = []
voltages = [[] for _ in neurons]

# Run simulation
time = 0.0
while time < duration:
    # Step all synapses first
    for synapse in synapses:
        synapse.step(step)
    
    # Add input only to first neuron
    neurons[0].add_synaptic_input(0.15)
    
    # Step all neurons
    for neuron in neurons:
        neuron.step(step)
    
    # Record data
    times.append(time)
    for i, neuron in enumerate(neurons):
        voltages[i].append(neuron.get(neun_py.HHDoubleVariable.v))
    
    time += step

# Plot results
plt.figure(figsize=(12, 6))
colors = ['blue', 'red', 'green', 'purple']
for i, (v, color) in enumerate(zip(voltages, colors)):
    plt.plot(times, v, color=color, label=f'Neuron {i+1}', 
             linewidth=1.5, alpha=0.8)

plt.xlabel('Time (ms)')
plt.ylabel('Membrane Potential (mV)')
plt.title('Signal Propagation Through a Chain of Coupled Neurons')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('neuron_chain.pdf')
plt.show()
