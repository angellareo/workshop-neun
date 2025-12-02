import neun_py
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------
# Simulation parameters
# -------------------------------------
dt = 0.01
T = 5000
time = np.arange(0, T, dt)
n_steps = len(time)

# Regular HR mode base current
I_base = 2.5
noise_std = 0.5

# Generate noisy current
np.random.seed(42)
I_clean = np.ones(n_steps) * I_base
I_noisy = I_base + np.random.randn(n_steps) * noise_std

# -------------------------------------
# Helper function to configure HR neuron
# -------------------------------------
def configure_hr(neuron):
    params = neun_py.HRDoubleParameter
    neuron.set_param(params.e, 0)
    neuron.set_param(params.mu, 0.006)
    neuron.set_param(params.S, 4)
    neuron.set_param(params.a, 1)
    neuron.set_param(params.b, 3)
    neuron.set_param(params.c, 1)
    neuron.set_param(params.d, 5)
    neuron.set_param(params.xr, -1.6)
    neuron.set_param(params.vh, 1)

# -------------------------------------
# Helper function to set initial conditions
# -------------------------------------
def set_initial_conditions(neuron):
    neuron.set(neun_py.HRDoubleVariable.x, -0.712841)
    neuron.set(neun_py.HRDoubleVariable.y, -1.93688)
    neuron.set(neun_py.HRDoubleVariable.z, 3.16568)

# -------------------------------------
# Simulate HR neuron with arbitrary input
# -------------------------------------
def simulate_current(I_array):
    neuron = neun_py.HRDoubleRK4(neun_py.HRDoubleConstructorArgs())
    configure_hr(neuron)
    set_initial_conditions(neuron)

    V = []

    for k in range(n_steps):
        # Apply current (clean or noisy)
        neuron.add_synaptic_input(I_array[k])

        # Integrate one time step
        neuron.step(dt)

        # Record membrane potential (x variable)
        V.append(neuron.get(neun_py.HRDoubleVariable.x))

    return np.array(V)

# -------------------------------------
# Run both simulations
# -------------------------------------
V_clean = simulate_current(I_clean)
V_noisy = simulate_current(I_noisy)

# -------------------------------------
# Plotting
# -------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

axes[0].plot(time, V_clean, linewidth=1.2, label='Clean Input')
axes[0].set_ylabel('Membrane Potential (x)')
axes[0].set_title('HR Regular — Clean Input')
axes[0].grid(True, alpha=0.3)
axes[0].legend()

axes[1].plot(time, V_noisy, linewidth=1.2, color='orange', label='Noisy Input')
axes[1].set_xlabel('Time (ms)')
axes[1].set_ylabel('Membrane Potential (x)')
axes[1].set_title('HR Regular — Noisy Input')
axes[1].grid(True, alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.show()
