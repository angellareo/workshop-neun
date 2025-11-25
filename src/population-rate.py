#!/usr/bin/env python3
"""
Population firing rate analysis
Compute and visualize average network activity
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

# Create network of 10 neurons
n_neurons = 10
np.random.seed(42)
neurons = [create_hh_neuron(-65 + np.random.randn()*3) for _ in range(n_neurons)]

# Create all-to-all connectivity with weak coupling
synapses = []
coupling_strength = -0.0005  # Weak coupling
for i in range(n_neurons):
    for j in range(i+1, n_neurons):
        synapse = neun_py.ESynHHHHDoubleRK4(
            neurons[i], neun_py.HHDoubleVariable.v,
            neurons[j], neun_py.HHDoubleVariable.v,
            coupling_strength, coupling_strength
        )
        synapses.append(synapse)

# Simulation parameters
step = 0.001  # ms
duration = 200  # ms

# Storage
times = []
voltages = [[] for _ in range(n_neurons)]
population_voltage = []

# Run simulation
time = 0.0
while time < duration:
    # Step all synapses
    for synapse in synapses:
        synapse.step(step)
    
    # Add external input with some variability
    for i, neuron in enumerate(neurons):
        # Random input to create heterogeneous activity
        input_current = 0.10 + np.random.randn() * 0.01
        neuron.add_synaptic_input(input_current)
    
    # Step neurons
    for neuron in neurons:
        neuron.step(step)
    
    # Record data
    times.append(time)
    v_sum = 0
    for i, neuron in enumerate(neurons):
        v = neuron.get(neun_py.HHDoubleVariable.v)
        voltages[i].append(v)
        v_sum += v
    
    # Population mean voltage
    population_voltage.append(v_sum / n_neurons)
    
    time += step

# Compute population firing rate using sliding window
window_size = 5  # ms
window_samples = int(window_size / step)
firing_rate = []
rate_times = []

spike_threshold = 0  # mV
for i in range(0, len(times) - window_samples, window_samples//2):
    spike_count = 0
    window_time = times[i + window_samples//2]
    
    for j in range(n_neurons):
        # Count threshold crossings in window
        for k in range(i, min(i + window_samples, len(voltages[j]))):
            if k > 0 and voltages[j][k] > spike_threshold and voltages[j][k-1] <= spike_threshold:
                spike_count += 1
    
    # Convert to firing rate (Hz)
    rate = (spike_count / n_neurons) / (window_size / 1000)
    firing_rate.append(rate)
    rate_times.append(window_time)

# Plot results
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

# Individual neurons
colors = plt.cm.viridis(np.linspace(0, 1, min(5, n_neurons)))
for i in range(min(5, n_neurons)):  # Show first 5 neurons
    ax1.plot(times, voltages[i], color=colors[i], 
             label=f'Neuron {i}', linewidth=0.8, alpha=0.7)
ax1.set_ylabel('Membrane Potential (mV)')
ax1.set_title('Individual Neuron Activity (subset)')
ax1.legend(loc='upper right', ncol=5)
ax1.grid(True, alpha=0.3)

# Population average voltage
ax2.plot(times, population_voltage, 'b-', linewidth=1.5)
ax2.set_ylabel('Mean Voltage (mV)')
ax2.set_title('Population Average Membrane Potential')
ax2.grid(True, alpha=0.3)

# Population firing rate
ax3.plot(rate_times, firing_rate, 'r-', linewidth=2)
ax3.set_xlabel('Time (ms)')
ax3.set_ylabel('Firing Rate (Hz)')
ax3.set_title(f'Population Firing Rate (window: {window_size} ms)')
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('population_rate.pdf')
plt.show()

# Print statistics
print(f"Network Statistics:")
print(f"  Number of neurons: {n_neurons}")
print(f"  Number of synapses: {len(synapses)}")
print(f"  Mean firing rate: {np.mean(firing_rate):.2f} Hz")
print(f"  Peak firing rate: {np.max(firing_rate):.2f} Hz")
