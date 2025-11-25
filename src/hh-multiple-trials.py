import neun_py
import numpy as np

# Diccionario de parámetros opcional, por si lo quieres usar
HH_PARAMS = {
    "cm": 1.0 * 7.854e-3,
    "vna": 50.0,
    "vk": -77.0,
    "vl": -54.387,
    "gna": 120 * 7.854e-3,
    "gk": 36 * 7.854e-3,
    "gl": 0.3 * 7.854e-3,
}


def set_hh_params(neuron, params):
    neuron.set_param(neun_py.HHDoubleParameter.cm, params["cm"])
    neuron.set_param(neun_py.HHDoubleParameter.vna, params["vna"])
    neuron.set_param(neun_py.HHDoubleParameter.vk, params["vk"])
    neuron.set_param(neun_py.HHDoubleParameter.vl, params["vl"])
    neuron.set_param(neun_py.HHDoubleParameter.gna, params["gna"])
    neuron.set_param(neun_py.HHDoubleParameter.gk, params["gk"])
    neuron.set_param(neun_py.HHDoubleParameter.gl, params["gl"])


n_trials = 10
all_voltages = []

dt = 0.001
T = 100
time = np.arange(0, T, dt)

for trial in range(n_trials):
    # Create fresh neuron for each trial
    args = neun_py.HHDoubleConstructorArgs()
    neuron = neun_py.HHDoubleRK4(args)
    
    # Set parameters (new helper function)
    set_hh_params(neuron, HH_PARAMS)
    
    # Set initial conditions
    neuron.set(neun_py.HHDoubleVariable.v, -80.0)
    neuron.set(neun_py.HHDoubleVariable.m, 0.1)
    neuron.set(neun_py.HHDoubleVariable.n, 0.7)
    neuron.set(neun_py.HHDoubleVariable.h, 0.01)
    
    V = []
    for t in time:
        # Add noisy input
        I_noisy = 0.1 + 0.05 * np.random.randn()
        neuron.add_synaptic_input(I_noisy)
        neuron.step(dt)
        V.append(neuron.get(neun_py.HHDoubleVariable.v))
    
    all_voltages.append(V)

# Analyze trial-to-trial variability
all_voltages = np.array(all_voltages)
mean_voltage = np.mean(all_voltages, axis=0)
std_voltage = np.std(all_voltages, axis=0)

print(f"Mean voltage at t=50ms: {mean_voltage[int(50/dt)]:.2f} ± {std_voltage[int(50/dt)]:.2f} mV")