# Dictionary of Izhikevich parameters for different cell types
neuron_types = {
    'Regular Spiking (RS)': {
        'a': 0.02, 'b': 0.2, 'c': -65, 'd': 8,
        'I_amp': 10, 'color': 'blue'
    },
    'Intrinsically Bursting (IB)': {
        'a': 0.02, 'b': 0.2, 'c': -55, 'd': 4,
        'I_amp': 10, 'color': 'green'
    },
    'Chattering (CH)': {
        'a': 0.02, 'b': 0.2, 'c': -50, 'd': 2,
        'I_amp': 10, 'color': 'red'
    },
    'Fast Spiking (FS)': {
        'a': 0.1, 'b': 0.2, 'c': -65, 'd': 2,
        'I_amp': 10, 'color': 'purple'
    },
    'Low-Threshold Spiking (LTS)': {
        'a': 0.02, 'b': 0.25, 'c': -65, 'd': 2,
        'I_amp': 10, 'color': 'orange'
    },
    'Resonator (RZ)': {
        'a': 0.1, 'b': 0.26, 'c': -65, 'd': 2,
        'I_amp': 3.5, 'color': 'brown'
    }
}

# Simulate and plot
dt = 0.1
T = 200
n_steps = int(T / dt)

fig, axes = plt.subplots(3, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, (name, params) in enumerate(neuron_types.items()):
    # Create Izhikevich neuron with specific parameters
    neuron = neun.models.Izhikevich(
        a=params['a'], 
        b=params['b'], 
        c=params['c'], 
        d=params['d']
    )
    
    V_trace = []
    t_trace = []
    
    for step in range(n_steps):
        t = step * dt
        neuron.step(dt, params['I_amp'])
        V_trace.append(neuron.V)
        t_trace.append(t)
    
    axes[idx].plot(t_trace, V_trace, color=params['color'], linewidth=1.5)
    axes[idx].set_title(name, fontsize=11, fontweight='bold')
    axes[idx].set_ylabel('V (mV)')
    axes[idx].grid(True, alpha=0.3)
    axes[idx].set_ylim([-80, 40])

axes[-2].set_xlabel('Time (ms)')
axes[-1].set_xlabel('Time (ms)')
plt.tight_layout()
plt.show()