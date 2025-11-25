import neun_py
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create constructor arguments
args = neun_py.HHDoubleConstructorArgs()

# Step 2: Create a Hodgkin-Huxley neuron with Double precision and RK4 integrator
neuron = neun_py.HHDoubleRK4(args)

# Step 3: Set parameter values
neuron.set_param(neun_py.HHDoubleParameter.cm, 1.0 * 7.854e-3)    # Capacitance
neuron.set_param(neun_py.HHDoubleParameter.vna, 50.0)            # Na reversal
neuron.set_param(neun_py.HHDoubleParameter.vk, -77.0)            # K reversal  
neuron.set_param(neun_py.HHDoubleParameter.vl, -54.387)          # Leak reversal
neuron.set_param(neun_py.HHDoubleParameter.gna, 120 * 7.854e-3)  # Na conductance
neuron.set_param(neun_py.HHDoubleParameter.gk, 36 * 7.854e-3)    # K conductance
neuron.set_param(neun_py.HHDoubleParameter.gl, 0.3 * 7.854e-3)   # Leak conductance

# Step 4: Set initial conditions
neuron.set(neun_py.HHDoubleVariable.v, -80.0)  # Membrane potential
neuron.set(neun_py.HHDoubleVariable.m, 0.1)    # Na activation
neuron.set(neun_py.HHDoubleVariable.n, 0.7)    # K activation
neuron.set(neun_py.HHDoubleVariable.h, 0.01)   # Na inactivation

# Step 5: Run simulation
dt = 0.001            # Time step (ms)
T = 100               # Simulation duration (ms)
time = np.arange(0, T, dt)

V = []  # Membrane potential storage

for t in time:
    # Add external current input
    neuron.add_synaptic_input(0.1)  # Constant input current
    
    # Step neuron forward
    neuron.step(dt)
    
    # Record voltage
    V.append(neuron.get(neun_py.HHDoubleVariable.v))

# Step 6: Visualize
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(time, V, 'b-', linewidth=1.5)
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Membrane Potential (mV)')
ax.set_title('Hodgkin-Huxley Neuron - Basic Simulation')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Simulation completed: {len(time)} time steps")
print(f"Final voltage: {V[-1]:.2f} mV")