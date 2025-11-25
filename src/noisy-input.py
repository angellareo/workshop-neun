# Compare responses to clean vs noisy input
dt = 0.1
T = 500
n_steps = int(T / dt)

# Base current
I_base = 10.0
noise_std = 3.0

# Generate noisy current
np.random.seed(42)
I_clean = np.ones(n_steps) * I_base
I_noisy = I_base + np.random.randn(n_steps) * noise_std

# Simulate both conditions
lif_neuron = neun.models.LIF(tau_m=20.0, V_th=-50.0, V_reset=-70.0, V_rest=-65.0)

# Clean input
V_clean = []
t_trace = []
lif_neuron.reset()
for step in range(n_steps):
    t = step * dt
    lif_neuron.step(dt, I_clean[step])
    V_clean.append(lif_neuron.V)
    t_trace.append(t)

# Noisy input
V_noisy = []
lif_neuron.reset()
for step in range(n_steps):
    lif_neuron.step(dt, I_noisy[step])
    V_noisy.append(lif_neuron.V)

# Plot comparison
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

axes[0].plot(t_trace, V_clean, linewidth=1.5, label='Clean Input')
axes[0].set_ylabel('V (mV)')
axes[0].set_title('Response to Clean Input')
axes[0].grid(True, alpha=0.3)
axes[0].legend()

axes[1].plot(t_trace, V_noisy, linewidth=1.5, color='orange', label='Noisy Input')
axes[1].set_xlabel('Time (ms)')
axes[1].set_ylabel('V (mV)')
axes[1].set_title('Response to Noisy Input')
axes[1].grid(True, alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.show()