# Chaotic Hindmarsh-Rose model
# The HR model can exhibit chaotic dynamics without external noise
# Parameters for chaotic behavior: a=1.0, b=3.0, c=1.0, d=5.0, r=0.001, s=4.0, x_rest=-1.6

hr_neuron = neun.models.HindmarshRose(
    a=1.0, 
    b=3.0, 
    c=1.0, 
    d=5.0, 
    r=0.001,  # Slow recovery - key for chaos
    s=4.0, 
    x_rest=-1.6
)

dt = 0.1
T = 1000  # Longer time to see chaotic behavior
n_steps = int(T / dt)

# Constant input current (no external noise needed!)
I_input = 3.2

V_trace = []
y_trace = []  # Recovery variable
z_trace = []  # Slow adaptation variable
t_trace = []

hr_neuron.reset()
for step in range(n_steps):
    t = step * dt
    hr_neuron.step(dt, I_input)
    V_trace.append(hr_neuron.V)
    y_trace.append(hr_neuron.y)
    z_trace.append(hr_neuron.z)
    t_trace.append(t)

# Plot the chaotic dynamics
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

axes[0].plot(t_trace, V_trace, linewidth=0.8, color='darkblue')
axes[0].set_ylabel('Membrane Potential (x)', fontsize=12)
axes[0].set_title('Chaotic Hindmarsh-Rose Neuron (No External Noise!)', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)

axes[1].plot(t_trace, y_trace, linewidth=0.8, color='darkgreen')
axes[1].set_ylabel('Recovery (y)', fontsize=12)
axes[1].grid(True, alpha=0.3)

axes[2].plot(t_trace, z_trace, linewidth=0.8, color='darkred')
axes[2].set_xlabel('Time (ms)', fontsize=12)
axes[2].set_ylabel('Adaptation (z)', fontsize=12)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Phase space plot to visualize chaos
fig = plt.figure(figsize=(12, 5))

ax1 = fig.add_subplot(121, projection='3d')
ax1.plot(V_trace, y_trace, z_trace, linewidth=0.5, alpha=0.6)
ax1.set_xlabel('x (membrane potential)')
ax1.set_ylabel('y (recovery)')
ax1.set_zlabel('z (adaptation)')
ax1.set_title('3D Phase Space - Chaotic Attractor')

ax2 = fig.add_subplot(122)
ax2.plot(V_trace, y_trace, linewidth=0.5, alpha=0.6)
ax2.set_xlabel('x (membrane potential)')
ax2.set_ylabel('y (recovery)')
ax2.set_title('2D Projection (x-y plane)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()