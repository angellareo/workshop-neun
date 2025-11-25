#!/usr/bin/env python3
"""
Network activity visualization with raster plot
Shows spike times for multiple neurons
"""
import neun_py
import matplotlib.pyplot as plt
import numpy as np

def create_hh_neuron(v_init=-65):
    """Create and initialize an HH neuron"""
    neuron_args = neun_py.HHDoubleConstructorArgs()
    neuron = neun_py.HHDoubleRK4(neuron_args)
    
    neuron.set_param(neun_py.HHDoubleParameter.cm, 1 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.vna, 50)
    neuron.set_param(neun_py.HHDoubleParameter.vk, -77)
    neuron.set_param(neun_py.HHDoubleParameter.vl, -54.387)
    neuron.set_param(neun_py.HHDoubleParameter.gna, 120 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.gk, 36 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.gl, 0.3 * 7.854e-3)
    
    neuron.set(neun_py.HHDoubleVariable.v, v_init)
    neuron.set(neun_py.HHDoubleVariable.m, 0.05)
    neuron.set(neun_py.HHDoubleVariable.h, 0.6)
    neuron.set(neun_py.HHDoubleVariable.n, 0.3)
    
    return neuron

# Create 5 neurons
n_neurons = 5
neurons = [create_hh_neuron(-65 + i*2) for i in range(n_neurons)]

# Connect in a simple network (each to next)
synapses = []
for i in range(n_neurons - 1):
    synapse = neun_py.ESynHHHHDoubleRK4(
        neurons[i], neun_py.HHDoubleVariable.v,
        neurons[i+1], neun_py.HHDoubleVariable.v,
        -0.001, -0.001
    )
    synapses.append(synapse)

# Simulation parameters
step = 0.001  # ms
duration = 200  # ms

# Storage for spike detection
spike_threshold = 0  # mV
spike_times = [[] for _ in range(n_neurons)]
was_below_threshold = [True] * n_neurons

times = []
voltages = [[] for _ in range(n_neurons)]

# Run simulation
time = 0.0
while time < duration:
    # Step synapses
    for synapse in synapses:
        synapse.step(step)
    
    # Add different inputs to create varied activity
    for i, neuron in enumerate(neurons):
        # First neuron gets constant input, others get less
        input_current = 0.12 if i == 0 else 0.08 if i == 1 else 0.0
        neuron.add_synaptic_input(input_current)
    
    # Step neurons
    for neuron in neurons:
        neuron.step(step)
    
    # Record and detect spikes
    times.append(time)
    for i, neuron in enumerate(neurons):
        v = neuron.get(neun_py.HHDoubleVariable.v)
        voltages[i].append(v)
        
        # Spike detection: crossing threshold from below
        if was_below_threshold[i] and v > spike_threshold:
            spike_times[i].append(time)
            was_below_threshold[i] = False
        elif v < spike_threshold:
            was_below_threshold[i] = True
    
    time += step

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Raster plot
for i, spikes in enumerate(spike_times):
    ax1.scatter(spikes, [i] * len(spikes), c='black', marker='|', s=100)

ax1.set_ylabel('Neuron ID')
ax1.set_xlabel('Time (ms)')
ax1.set_title('Network Activity: Raster Plot')
ax1.set_ylim(-0.5, n_neurons - 0.5)
ax1.set_yticks(range(n_neurons))
ax1.grid(True, alpha=0.3)

# Voltage traces (subset for clarity)
colors = plt.cm.viridis(np.linspace(0, 1, n_neurons))
for i in range(n_neurons):
    ax2.plot(times, voltages[i], color=colors[i], 
             label=f'Neuron {i}', linewidth=1.0, alpha=0.7)

ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('Membrane Potential (mV)')
ax2.set_title('Network Activity: Voltage Traces')
ax2.legend(loc='upper right', ncol=n_neurons)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('raster_plot.pdf')
plt.show()

# Print spike statistics
print("Spike Statistics:")
for i, spikes in enumerate(spike_times):
    print(f"  Neuron {i}: {len(spikes)} spikes")
    if len(spikes) > 1:
        isis = np.diff(spikes)
        print(f"    Mean ISI: {np.mean(isis):.2f} ms")
        print(f"    Firing rate: {len(spikes)/(duration/1000):.2f} Hz")
