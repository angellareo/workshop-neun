import neun_py
import numpy as np
import matplotlib.pyplot as plt

# Compare different external currents
currents = [0.05, 0.1, 0.15]
colors = ['blue', 'green', 'red']

# Create subplots for each current
fig, axes = plt.subplots(len(currents), 1, figsize=(10, 8), sharex=True)

dt = 0.001           # Time step (ms)
T = 100              # Simulation duration (ms)
time = np.arange(0, T, dt)

for idx, (I_ext, color) in enumerate(zip(currents, colors)):
    # Create neuron
    args = neun_py.HHDoubleConstructorArgs()
    neuron = neun_py.HHDoubleRK4(args)
    
    # Set parameters
    neuron.set_param(neun_py.HHDoubleParameter.cm, 1.0 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.vna, 50.0)
    neuron.set_param(neun_py.HHDoubleParameter.vk, -77.0)
    neuron.set_param(neun_py.HHDoubleParameter.vl, -54.387)
    neuron.set_param(neun_py.HHDoubleParameter.gna, 120 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.gk, 36 * 7.854e-3)
    neuron.set_param(neun_py.HHDoubleParameter.gl, 0.3 * 7.854e-3)
    
    # Set initial conditions
    neuron.set(neun_py.HHDoubleVariable.v, -80.0)
    neuron.set(neun_py.HHDoubleVariable.m, 0.1)
    neuron.set(neun_py.HHDoubleVariable.n, 0.7)
    neuron.set(neun_py.HHDoubleVariable.h, 0.01)

    # Simulate
    V = []
    for t in time:
        neuron.add_synaptic_input(I_ext)
        neuron.step(dt)
        V.append(neuron.get(neun_py.HHDoubleVariable.v))
    
    # Plot
    axes[idx].plot(time, V, color=color, linewidth=1.5)
    axes[idx].set_ylabel('V (mV)')
    axes[idx].set_title(f'External Current = {I_ext} nA')
    axes[idx].grid(True, alpha=0.3)

axes[-1].set_xlabel('Time (ms)')
plt.suptitle('Effect of Input Current on Hodgkin-Huxley Neuron', y=1.02)
plt.tight_layout()
plt.show()