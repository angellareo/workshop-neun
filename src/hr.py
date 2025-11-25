import neun_py
import numpy as np
import matplotlib.pyplot as plt

# Different parameter sets for HR neuron
parameter_sets = [
    {'name': 'Regular Spiking', 'I': 3.0},
    {'name': 'Bursting', 'I': 3.5},
    {'name': 'Chaotic', 'I': 3.8},
]

fig, axes = plt.subplots(len(parameter_sets), 1, figsize=(12, 8))

dt = 0.01
T = 1000
time = np.arange(0, T, dt)

for idx, params in enumerate(parameter_sets):
    # Create Hindmarsh-Rose neuron
    args = neun_py.HRDoubleConstructorArgs()
    neuron = neun_py.HRDoubleRK4(args)
    
    # Set parameters
    neuron.set_param(neun_py.HRDoubleParameter.e, 3.281)
    neuron.set_param(neun_py.HRDoubleParameter.mu, 0.0029)
    neuron.set_param(neun_py.HRDoubleParameter.S, 4)
    # neuron.set_param(neun_py.HRDoubleParameter.a, 1)
    # neuron.set_param(neun_py.HRDoubleParameter.b, 3)
    # neuron.set_param(neun_py.HRDoubleParameter.c, 1)
    # neuron.set_param(neun_py.HRDoubleParameter.d, 5)
    # neuron.set_param(neun_py.HRDoubleParameter.xr, -1.6)
    # neuron.set_param(neun_py.HRDoubleParameter.vh, 1)

    # HR model uses default parameters, but we can modify them if needed
    # Set initial conditions
    neuron.set(neun_py.HRDoubleVariable.x, -0.712841)
    neuron.set(neun_py.HRDoubleVariable.y, -1.93688)
    neuron.set(neun_py.HRDoubleVariable.z, 3.16568)
    
    # Simulate with different input currents
    V = []
    for t in time:
        # neuron.add_synaptic_input(params['I'])
        neuron.step(dt)
        V.append(neuron.get(neun_py.HRDoubleVariable.x))  # x is membrane potential
    
    # Plot
    axes[idx].plot(time, V, 'b-', linewidth=1)
    axes[idx].set_title(f"{params['name']} (I = {params['I']})")
    axes[idx].set_ylabel('Membrane Potential')
    axes[idx].grid(True, alpha=0.3)
    if idx == len(parameter_sets) - 1:
        axes[idx].set_xlabel('Time (ms)')

plt.suptitle('Hindmarsh-Rose Neuron: Different Firing Patterns', fontsize=14)
plt.tight_layout()
plt.show()