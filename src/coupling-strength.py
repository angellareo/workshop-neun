#!/usr/bin/env python3
"""
Explore effect of coupling strength on synchronization
Demonstrates how synaptic conductance affects network dynamics
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

def run_simulation(coupling_conductance):
    """Run simulation with given coupling strength"""
    # Create two neurons with different initial conditions
    h1 = create_hh_neuron(-75)
    h2 = create_hh_neuron(-65)
    
    # Create synapse with specified coupling
    synapse = neun_py.ESynHHHHDoubleRK4(
        h1, neun_py.HHDoubleVariable.v,
        h2, neun_py.HHDoubleVariable.v,
        -coupling_conductance, -coupling_conductance
    )
    
    # Simulation
    step = 0.001
    duration = 100
    
    v1_vals = []
    v2_vals = []
    
    time = 0.0
    while time < duration:
        synapse.step(step)
        h1.add_synaptic_input(0.1)
        h2.add_synaptic_input(0.08)
        h1.step(step)
        h2.step(step)
        
        v1_vals.append(h1.get(neun_py.HHDoubleVariable.v))
        v2_vals.append(h2.get(neun_py.HHDoubleVariable.v))
        
        time += step
    
    return np.array(v1_vals), np.array(v2_vals)

def compute_synchronization(v1, v2):
    """Compute correlation coefficient as measure of synchronization"""
    return np.corrcoef(v1, v2)[0, 1]

# Test different coupling strengths
conductances = np.linspace(0.0001, 0.01, 15)
sync_values = []

print("Computing synchronization for different coupling strengths...")
for g in conductances:
    v1, v2 = run_simulation(g)
    sync = compute_synchronization(v1, v2)
    sync_values.append(sync)
    print(f"  g = {g:.4f}: sync = {sync:.3f}")

# Create visualization
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

# Example traces for weak, medium, and strong coupling
example_conductances = [0.0001, 0.005, 0.01]
example_labels = ['Weak', 'Medium', 'Strong']
colors = ['red', 'orange', 'green']

for i, (g, label, color) in enumerate(zip(example_conductances, example_labels, colors)):
    v1, v2 = run_simulation(g)
    times = np.arange(len(v1)) * 0.001
    
    ax = ax1 if i == 0 else (ax2 if i == 1 else ax3)
    ax.plot(times, v1, 'b-', linewidth=1, alpha=0.8, label='Neuron 1')
    ax.plot(times, v2, 'r-', linewidth=1, alpha=0.8, label='Neuron 2')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Voltage (mV)')
    ax.set_title(f'{label} Coupling (g={g:.4f})')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('coupling_examples.pdf')

# Plot synchronization vs coupling strength
plt.figure(figsize=(10, 6))
plt.plot(conductances, sync_values, 'o-', linewidth=2, markersize=6)
plt.xlabel('Coupling Conductance')
plt.ylabel('Synchronization (Correlation)')
plt.title('Network Synchronization vs Coupling Strength')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('coupling_strength.pdf')
plt.show()

print("\nSynchronization increases with coupling strength!")
