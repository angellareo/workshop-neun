import numpy as np
import matplotlib.pyplot as plt
import neun_py as neun

# Regular bursting HR parameters (typical bursting)
hr_regular = neun.models.HindmarshRose(
    a=1.0, b=3.0, c=1.0, d=5.0,
    r=0.005,  # faster slow current -> regular bursting
    s=4.0, x_rest=-1.6
)

# Chaotic HR parameters (deterministic chaos)
hr_chaotic = neun.models.HindmarshRose(
    a=1.0, b=3.0, c=1.0, d=5.0,
    r=0.001,  # slower slow current -> chaotic regime
    s=4.0, x_rest=-1.6
)

dt = 0.1
T = 1000
n_steps = int(T / dt)

I_reg = 3.0
I_chaos = 3.2

def simulate_hr(neuron, I_input, dt, T):
    n_steps = int(T / dt)
    V, y, z, t = [], [], [], []
    neuron.reset()
    for step in range(n_steps):
        t_curr = step * dt
        neuron.step(dt, I_input)
        V.append(neuron.V)
        y.append(neuron.y)
        z.append(neuron.z)
        t.append(t_curr)
    return np.array(t), np.array(V), np.array(y), np.array(z)

# Simulations
t_reg, V_reg, y_reg, z_reg = simulate_hr(hr_regular, I_reg, dt, T)
t_cha, V_cha, y_cha, z_cha = simulate_hr(hr_chaotic, I_chaos, dt, T)

# Plot time series comparison
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
axes[0].plot(t_reg, V_reg, linewidth=0.9, color='steelblue')
axes[0].set_title('Hindmarsh-Rose: Regular Bursting', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Membrane Potential (x)')
axes[0].grid(True, alpha=0.3)

axes[1].plot(t_cha, V_cha, linewidth=0.9, color='darkred')
axes[1].set_title('Hindmarsh-Rose: Chaotic Regime', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Time (ms)')
axes[1].set_ylabel('Membrane Potential (x)')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Phase space comparison (x-y)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(V_reg, y_reg, linewidth=0.6, color='steelblue')
ax1.set_title('Regular Bursting: Phase Space (x-y)')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.grid(True, alpha=0.3)

ax2.plot(V_cha, y_cha, linewidth=0.6, color='darkred')
ax2.set_title('Chaotic Regime: Phase Space (x-y)')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Optional 3D phase space for chaotic attractor
try:
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(121, projection='3d')
    ax.plot(V_reg, y_reg, z_reg, linewidth=0.4, alpha=0.8, color='steelblue')
    ax.set_title('Regular Bursting: 3D Phase Space')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot(V_cha, y_cha, z_cha, linewidth=0.4, alpha=0.8, color='darkred')
    ax2.set_title('Chaotic Regime: 3D Phase Space')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')

    plt.tight_layout()
    plt.show()
except Exception:
    # If 3D not available, skip
    pass