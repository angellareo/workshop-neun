import neun_py
import numpy as np

# Test multiple parameter combinations
param_grid = {
    'gna': [100, 120, 140],  # mS/cm² (before scaling)
    'gk': [30, 36, 42]       # mS/cm² (before scaling)
}

results = []

dt = 0.001
T = 100
time = np.arange(0, T, dt)

for gna in param_grid['gna']:
    for gk in param_grid['gk']:
        # Create neuron
        args = neun_py.HHDoubleConstructorArgs()
        neuron = neun_py.HHDoubleRK4(args)
        
        # Set parameters with varied conductances
        neuron.set_param(neun_py.HHDoubleParameter.cm, 1.0 * 7.854e-3)
        neuron.set_param(neun_py.HHDoubleParameter.vna, 50.0)
        neuron.set_param(neun_py.HHDoubleParameter.vk, -77.0)
        neuron.set_param(neun_py.HHDoubleParameter.vl, -54.387)
        neuron.set_param(neun_py.HHDoubleParameter.gna, gna * 7.854e-3)
        neuron.set_param(neun_py.HHDoubleParameter.gk, gk * 7.854e-3)
        neuron.set_param(neun_py.HHDoubleParameter.gl, 0.3 * 7.854e-3)
        
        # Set initial conditions
        neuron.set(neun_py.HHDoubleVariable.v, -80.0)
        neuron.set(neun_py.HHDoubleVariable.m, 0.1)
        neuron.set(neun_py.HHDoubleVariable.n, 0.7)
        neuron.set(neun_py.HHDoubleVariable.h, 0.01)
        
        # Simulate
        V = []
        for t in time:
            neuron.add_synaptic_input(0.1)
            neuron.step(dt)
            V.append(neuron.get(neun_py.HHDoubleVariable.v))
        
        # Detect spikes
        V_array = np.array(V)
        n_spikes = np.sum((V_array[:-1] < 0) & (V_array[1:] >= 0))
        
        results.append({
            'gna': gna,
            'gk': gk,
            'n_spikes': n_spikes,
            'mean_voltage': np.mean(V)
        })

# Analyze results
import pandas as pd
df = pd.DataFrame(results)
print(df)