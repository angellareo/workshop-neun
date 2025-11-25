import neun_py
import numpy as np
import matplotlib.pyplot as plt

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

# Simulate and record multiple variables
dt = 0.001
T = 100
time = np.arange(0, T, dt)

# Storage arrays
V = []      # Membrane potential
m_vals = [] # Na activation
h_vals = [] # Na inactivation  
n_vals = [] # K activation

for t in time:
    neuron.add_synaptic_input(0.1)
    neuron.step(dt)
    
    # Record all variables of interest
    V.append(neuron.get(neun_py.HHDoubleVariable.v))
    m_vals.append(neuron.get(neun_py.HHDoubleVariable.m))
    h_vals.append(neuron.get(neun_py.HHDoubleVariable.h))
    n_vals.append(neuron.get(neun_py.HHDoubleVariable.n))

# Plot multiple variables
fig, axes = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

axes[0].plot(time, V, 'b-', linewidth=1.5)
axes[0].set_ylabel('V (mV)')
axes[0].set_title('Membrane Potential')
axes[0].grid(True, alpha=0.3)

axes[1].plot(time, m_vals, 'r-', linewidth=1.5)
axes[1].set_ylabel('m')
axes[1].set_title('Na Activation')
axes[1].grid(True, alpha=0.3)

axes[2].plot(time, h_vals, 'g-', linewidth=1.5)
axes[2].set_ylabel('h')
axes[2].set_title('Na Inactivation')
axes[2].grid(True, alpha=0.3)

axes[3].plot(time, n_vals, 'orange', linewidth=1.5)
axes[3].set_ylabel('n')
axes[3].set_title('K Activation')
axes[3].set_xlabel('Time (ms)')
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()