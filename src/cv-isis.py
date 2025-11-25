# Analyze spike time variability
def compute_ISI_stats(neuron, I_input, dt, T):
    """Compute inter-spike interval statistics."""
    n_steps = int(T / dt)
    spike_times = []
    prev_V = neuron.V
    
    neuron.reset()
    for step in range(n_steps):
        t = step * dt
        if isinstance(I_input, np.ndarray):
            neuron.step(dt, I_input[step])
        else:
            neuron.step(dt, I_input)
        
        # Detect spike (works for both LIF and HR)
        if hasattr(neuron, 'V_th'):
            # LIF model
            if prev_V < neuron.V_th and neuron.V >= neuron.V_th:
                spike_times.append(t)
        else:
            # HR model - detect peaks above threshold
            if step > 0 and len(spike_times) == 0:
                prev_V = neuron.V
                continue
            if step > 1:
                V_prev2 = V_trace_local[step-2] if 'V_trace_local' in locals() else prev_V
                if prev_V > neuron.V and prev_V > 0:  # Peak detection
                    if len(spike_times) == 0 or t - spike_times[-1] > 5:  # Avoid double counting
                        spike_times.append(t)
        
        prev_V = neuron.V
    
    if len(spike_times) < 2:
        return None, None
    
    ISIs = np.diff(spike_times)
    mean_ISI = np.mean(ISIs)
    std_ISI = np.std(ISIs)
    CV = std_ISI / mean_ISI if mean_ISI > 0 else 0
    
    return ISIs, CV


def compute_ISI_stats_HR(neuron, I_input, dt, T, threshold=0):
    """Specialized ISI computation for HR model using peak detection."""
    n_steps = int(T / dt)
    spike_times = []
    V_prev = None
    V_curr = neuron.V
    
    neuron.reset()
    for step in range(n_steps):
        t = step * dt
        V_prev2 = V_prev
        V_prev = V_curr
        
        neuron.step(dt, I_input)
        V_curr = neuron.V
        
        # Detect peaks: V_prev is a local maximum above threshold
        if V_prev2 is not None and V_prev is not None:
            if V_prev > V_prev2 and V_prev > V_curr and V_prev > threshold:
                # Avoid double-counting nearby peaks
                if len(spike_times) == 0 or (t - dt) - spike_times[-1] > 5:
                    spike_times.append(t - dt)
    
    if len(spike_times) < 2:
        return None, None
    
    ISIs = np.diff(spike_times)
    mean_ISI = np.mean(ISIs)
    std_ISI = np.std(ISIs)
    CV = std_ISI / mean_ISI if mean_ISI > 0 else 0
    
    return ISIs, CV


# Compare CV for different noise levels (LIF) and chaotic HR
noise_levels = [0, 1, 2, 3, 4, 5]
CVs_LIF = []
T = 2000
dt = 0.1

# LIF with different noise levels
for noise_std in noise_levels:
    lif_neuron = neun.models.LIF(tau_m=20.0, V_th=-50.0, V_reset=-70.0, V_rest=-65.0)
    n_steps = int(T / dt)
    I_input = 10.0 + np.random.randn(n_steps) * noise_std
    
    ISIs, CV = compute_ISI_stats(lif_neuron, I_input, dt, T)
    CVs_LIF.append(CV if CV is not None else 0)

# Chaotic HR (no noise needed)
hr_neuron = neun.models.HindmarshRose(
    a=1.0, b=3.0, c=1.0, d=5.0, r=0.001, s=4.0, x_rest=-1.6
)
ISIs_HR, CV_HR = compute_ISI_stats_HR(hr_neuron, I_input=3.2, dt=dt, T=T)

# Plot comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# CV vs noise for LIF
ax1.plot(noise_levels, CVs_LIF, 'o-', linewidth=2, markersize=8, label='LIF + Noise')
ax1.axhline(y=CV_HR if CV_HR else 0, color='red', linestyle='--', linewidth=2, 
            label=f'Chaotic HR (CV={CV_HR:.3f})')
ax1.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5, label='Irregular firing')
ax1.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5, label='Highly variable')
ax1.set_xlabel('Noise Level (std)', fontsize=12)
ax1.set_ylabel('Coefficient of Variation (CV)', fontsize=12)
ax1.set_title('LIF: Effect of External Noise on Variability', fontsize=13)
ax1.legend()
ax1.grid(True, alpha=0.3)

# ISI distributions
if ISIs_HR is not None:
    # Get ISIs for LIF with moderate noise for comparison
    lif_neuron = neun.models.LIF(tau_m=20.0, V_th=-50.0, V_reset=-70.0, V_rest=-65.0)
    I_input_noisy = 10.0 + np.random.randn(int(T/dt)) * 3.0
    ISIs_LIF, _ = compute_ISI_stats(lif_neuron, I_input_noisy, dt, T)
    
    if ISIs_LIF is not None:
        ax2.hist(ISIs_LIF, bins=30, alpha=0.6, label='LIF + Noise (σ=3)', 
                 color='blue', density=True)
        ax2.hist(ISIs_HR, bins=30, alpha=0.6, label='Chaotic HR', 
                 color='red', density=True)
        ax2.set_xlabel('Inter-Spike Interval (ms)', fontsize=12)
        ax2.set_ylabel('Probability Density', fontsize=12)
        ax2.set_title('ISI Distributions: Noise vs Chaos', fontsize=13)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"\nVariability Comparison:")
print(f"LIF with noise (σ=3): CV = {CVs_LIF[3]:.3f}")
print(f"Chaotic HR (no noise): CV = {CV_HR:.3f}" if CV_HR else "Chaotic HR: No spikes detected")