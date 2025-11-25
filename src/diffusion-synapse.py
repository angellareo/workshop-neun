#!/usr/bin/env python3
"""
Two neurons coupled via diffusion synapse
Demonstrates chemical-like coupling with dynamics
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
h1.set(neun_py.HHDoubleVariable.v, -70)
h2.set(neun_py.HHDoubleVariable.v, -65)

# Create diffusion synapse (chemical-like dynamics)
synapse = neun_py.DSynHHHHDoubleRK4(
    h1, neun_py.HHDoubleVariable.v,
    h2, neun_py.HHDoubleVariable.v
)

# Simulation parameters
step = 0.001  # ms
duration = 100  # ms

# Storage
times = []
v1_values = []
v2_values = []

# Run simulation
time = 0.0
while time < duration:
    # Step the synapse first
    synapse.step(step)
    
    # Add external input to first neuron
    h1.add_synaptic_input(0.12)
    
    # Step both neurons
    h1.step(step)
    h2.step(step)
    
    # Record data
    times.append(time)
    v1_values.append(h1.get(neun_py.HHDoubleVariable.v))
    v2_values.append(h2.get(neun_py.HHDoubleVariable.v))
    
    time += step

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(times, v1_values, 'b-', label='Neuron 1 (presynaptic)', linewidth=1.5)
plt.plot(times, v2_values, 'r-', label='Neuron 2 (postsynaptic)', linewidth=1.5)
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Potential (mV)')
plt.title('Diffusion Synapse: Chemical-like Coupling with Dynamics')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('diffusion_synapse.pdf')
plt.show()
