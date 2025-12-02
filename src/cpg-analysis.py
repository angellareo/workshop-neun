#!/usr/bin/env python3
"""
Central Pattern Generator (CPG) Analysis
Demonstrates rhythmic activity and phase relationships
"""
import neun_py
import matplotlib.pyplot as plt
import numpy as np

def create_hr_neuron(I_ext=3.0, ini_x=0):
    """Create Hindmarsh-Rose neuron (good for rhythmic activity)"""
    neuron_args = neun_py.HRDoubleConstructorArgs()
    neuron = neun_py.HRDoubleRK4(neuron_args)
    
    # HR parameters for bursting
    neuron.set_param(neun_py.HRDoubleParameter.e, I_ext)
    neuron.set_param(neun_py.HRDoubleParameter.a, 1.0)
    neuron.set_param(neun_py.HRDoubleParameter.b, 3.0)
    neuron.set_param(neun_py.HRDoubleParameter.c, 1.0)
    neuron.set_param(neun_py.HRDoubleParameter.d, 5.0)
    neuron.set_param(neun_py.HRDoubleParameter.mu, 0.006)
    neuron.set_param(neun_py.HRDoubleParameter.S, 4.0)
    neuron.set_param(neun_py.HRDoubleParameter.xr, -1.6)
    neuron.set_param(neun_py.HRDoubleParameter.vh, 1)
    
    # Initial conditions
    neuron.set(neun_py.HRDoubleVariable.x, ini_x)
    neuron.set(neun_py.HRDoubleVariable.y, -10.0)
    neuron.set(neun_py.HRDoubleVariable.z, 0.0)
    
    return neuron

# Create two HR neurons with reciprocal inhibition (CPG configuration)
n1 = create_hr_neuron(3.0, -1.5)
n2 = create_hr_neuron(3.0, 0)


# Reciprocal coupling (simulating mutual inhibition)
s12 = neun_py.ESynHRHRDoubleRK4(
    n1, neun_py.HRDoubleVariable.x,
    n2, neun_py.HRDoubleVariable.x,
    -0.75, -0.75  # Inhibitory-like coupling
)

# Simulation parameters
step = 0.01  # ms
duration = 1000  # ms (longer to see rhythm)

# Storage
times = []
x1_values = []
x2_values = []

# Run simulation
time = 0.0
while time < duration:
    s12.step(step)
    n1.step(step)
    n2.step(step)
    
    times.append(time)
    x1_values.append(n1.get(neun_py.HRDoubleVariable.x))
    x2_values.append(n2.get(neun_py.HRDoubleVariable.x))
    
    time += step

# Convert to numpy arrays
times = np.array(times)
x1_values = np.array(x1_values)
x2_values = np.array(x2_values)

plt.plot(times, x1_values, 'b-', label='Neuron 1')
plt.plot(times, x2_values, 'r-', label='Neuron 2')
plt.legend()
plt.show()
# Detect burst peaks (local maxima above threshold)
def detect_bursts(signal, threshold=0):
    bursts = []
    for i in range(1, len(signal)-1):
        if signal[i] > threshold and signal[i] > signal[i-1] and signal[i] > signal[i+1]:
            bursts.append(i)
    return np.array(bursts)

bursts1 = detect_bursts(x1_values, threshold=1.0)
bursts2 = detect_bursts(x2_values, threshold=1.0)

# Compute inter-burst intervals (IBIs)
def compute_ibis(burst_indices, times):
    if len(burst_indices) < 2:
        return np.array([])
    burst_times = times[burst_indices]
    return np.diff(burst_times)

ibi1 = compute_ibis(bursts1, times)
ibi2 = compute_ibis(bursts2, times)

# Compute phase difference (time lag between bursts)
def compute_phase_lag(bursts1, bursts2, times):
    if len(bursts1) == 0 or len(bursts2) == 0:
        return []
    
    phase_lags = []
    for b1 in bursts1:
        # Find nearest burst in neuron 2
        if len(bursts2) > 0:
            nearest = bursts2[np.argmin(np.abs(bursts2 - b1))]
            lag = times[nearest] - times[b1]
            phase_lags.append(lag)
    
    return np.array(phase_lags)

phase_lags = compute_phase_lag(bursts1, bursts2, times)

# Visualization
fig = plt.figure(figsize=(14, 10))

# Activity traces
ax1 = plt.subplot(3, 2, (1, 2))
ax1.plot(times, x1_values, 'b-', linewidth=1.5, label='Neuron 1', alpha=0.8)
ax1.plot(times, x2_values, 'r-', linewidth=1.5, label='Neuron 2', alpha=0.8)
ax1.plot(times[bursts1], x1_values[bursts1], 'bo', markersize=4)
ax1.plot(times[bursts2], x2_values[bursts2], 'ro', markersize=4)
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Membrane Potential')
ax1.set_title('Central Pattern Generator: Rhythmic Activity')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Raster plot
ax2 = plt.subplot(3, 2, 3)
ax2.scatter(times[bursts1], np.ones_like(bursts1), c='blue', marker='|', s=100)
ax2.scatter(times[bursts2], np.zeros_like(bursts2), c='red', marker='|', s=100)
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['Neuron 2', 'Neuron 1'])
ax2.set_xlabel('Time (ms)')
ax2.set_title('Burst Timing (Raster)')
ax2.grid(True, alpha=0.3)

# Inter-burst intervals
ax3 = plt.subplot(3, 2, 4)
if len(ibi1) > 0:
    ax3.plot(ibi1, 'bo-', label='Neuron 1', markersize=4)
if len(ibi2) > 0:
    ax3.plot(ibi2, 'ro-', label='Neuron 2', markersize=4)
ax3.set_xlabel('Burst Number')
ax3.set_ylabel('Inter-Burst Interval (ms)')
ax3.set_title('Rhythm Regularity')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Phase relationship
ax4 = plt.subplot(3, 2, 5)
if len(phase_lags) > 0:
    ax4.hist(phase_lags, bins=20, color='purple', alpha=0.7, edgecolor='black')
    ax4.axvline(np.mean(phase_lags), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {np.mean(phase_lags):.1f} ms')
ax4.set_xlabel('Phase Lag (ms)')
ax4.set_ylabel('Count')
ax4.set_title('Phase Relationship Between Neurons')
ax4.legend()
ax4.grid(True, alpha=0.3)

# Zoomed view
ax5 = plt.subplot(3, 2, 6)
zoom_start = int(len(times) * 0.3)
zoom_end = int(len(times) * 0.5)
ax5.plot(times[zoom_start:zoom_end], x1_values[zoom_start:zoom_end], 
         'b-', linewidth=2, label='Neuron 1')
ax5.plot(times[zoom_start:zoom_end], x2_values[zoom_start:zoom_end], 
         'r-', linewidth=2, label='Neuron 2')
ax5.set_xlabel('Time (ms)')
ax5.set_ylabel('Membrane Potential')
ax5.set_title('Zoomed View: Alternating Bursts')
ax5.legend()
ax5.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('cpg_analysis.pdf')
plt.show()

# Print statistics
print("CPG Statistics:")
print(f"  Neuron 1: {len(bursts1)} bursts")
print(f"  Neuron 2: {len(bursts2)} bursts")
if len(ibi1) > 0:
    print(f"  Mean IBI Neuron 1: {np.mean(ibi1):.2f} ± {np.std(ibi1):.2f} ms")
if len(ibi2) > 0:
    print(f"  Mean IBI Neuron 2: {np.mean(ibi2):.2f} ± {np.std(ibi2):.2f} ms")
if len(phase_lags) > 0:
    print(f"  Mean phase lag: {np.mean(phase_lags):.2f} ± {np.std(phase_lags):.2f} ms")
