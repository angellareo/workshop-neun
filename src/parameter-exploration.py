import neun_py
import numpy as np
import matplotlib.pyplot as plt

# Explore effect of different sodium conductances
gna_values = np.linspace(80, 160, 10) * 7.854e-3
firing_frequencies = []

dt = 0.001
T = 500  # Longer simulation for frequency estimation
time = np.arange(0, T, dt)

for gna in gna_values:
    # Create neuron
    args = neun_py.HHDoubleConstructorArgs()
    neuron = neun_py.HHDoubleRK4(args)
    
    # Set parameters
    neuron.set_param(neun_py.HHDoubleParameter.cm, 1.0 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.vna, 50.0)
    neuron.set_param(neun_py.HHDoubleParameter.vk, -77.0)
    neuron.set_param(neun_py.HHDoubleParameter.vl, -54.387)
    neuron.set_param(neun_py.HHDoubleParameter.gna, gna)  # Vary this
    neuron.set_param(neun_py.HHDoubleParameter.gk, 36 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.gl, 0.3 * 7.854e-3)
    
    # Set initial conditions
    neuron.set(neun_py.HHDoubleVariable.v, -80.0)
    neuron.set(neun_py.HHDoubleVariable.m, 0.1)
    neuron.set(neun_py.HHDoubleVariable.n, 0.7)
    neuron.set(neun_py.HHDoubleVariable.h, 0.01)
    
    # Simulate and count spikes
    V = []
    spike_count = 0
    for t in time:
        neuron.add_synaptic_input(0.15)
        neuron.step(dt)
        V.append(neuron.get(neun_py.HHDoubleVariable.v))
    
    # Detect spikes (simple threshold crossing)
    V = np.array(V)
    spikes = np.where((V[:-1] < 0) & (V[1:] >= 0))[0]
    
    # Calculate frequency
    if len(spikes) > 1:
        # Use interval between first and last spike
        freq = (len(spikes) - 1) / ((spikes[-1] - spikes[0]) * dt / 1000)
    else:
        freq = 0
    
    firing_frequencies.append(freq)

# Plot parameter sweep
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(gna_values / 7.854e-3, firing_frequencies, 'o-', linewidth=2, markersize=6)
ax.set_xlabel('Na Conductance (mS/cm²)')
ax.set_ylabel('Firing Frequency (Hz)')
ax.set_title('Effect of Sodium Conductance on Firing Frequency')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()