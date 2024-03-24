import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x_cycloid = []
y_cycloid = []
def animate_frame(i):
    x, slope, intercept = x_values[i], tangent[i], tangent_intercept[i]

    # Vector to the center
    vector_to_center_cycloid = np.array([slope, -1]) / np.sqrt(slope ** 2 + 1)
    vector_to_center_cycloid *= -radius * direction

    # Angle of rotation of the point relative to the center of the circle
    cycloid_alpha = ds[i] / radius * direction * -1
    rotation_matrix = np.array([[np.cos(cycloid_alpha), -np.sin(cycloid_alpha)],
                                [np.sin(cycloid_alpha), np.cos(cycloid_alpha)]])
    new_point_cycloid_vector = rotation_matrix @ start_vector

    start_vector[:] = new_point_cycloid_vector

    x_cycloid.append(x + vector_to_center_cycloid[0] + new_point_cycloid_vector[0])
    y_cycloid.append(slope * x + intercept + vector_to_center_cycloid[1] + new_point_cycloid_vector[1])

    # Update circle position
    t = np.arange(0, 2 * np.pi, 0.04)
    circle_offset = np.array([x + vector_to_center_cycloid[0], slope * x + intercept + vector_to_center_cycloid[1]])
    x_circle = radius * np.cos(t) + circle_offset[0]
    y_circle = radius * np.sin(t) + circle_offset[1]

    # Update tracing point on the edge of the circle
    point.set_data(circle_offset[0] + new_point_cycloid_vector[0], circle_offset[1] + new_point_cycloid_vector[1])

    # Update visualization
    line_circle.set_xdata(x_circle)
    line_circle.set_ydata(y_circle)
    line_epicycloid.set_data(x_cycloid, y_cycloid)
    circle_radius_line.set_data([circle_offset[0], circle_offset[0] + new_point_cycloid_vector[0]],
                                [circle_offset[1], circle_offset[1] + new_point_cycloid_vector[1]])

    return line, line_circle, line_epicycloid, point


# Constants: radius, accuracy
radius = 0.05
step_size = 0.001
direction = 1

# Declaration of the path
x_values = np.arange(0.00001, 10, step_size)
y_values = 2 * (np.sin(x_values) + np.sqrt(1 / x_values)) / (np.power(x_values, 2) + 53 + np.exp(x_values))

# Calculating derivatives
dx = np.roll(x_values, 1) - x_values
dy = np.roll(y_values, 1) - y_values
ds = np.sqrt(dx ** 2 + dy ** 2)

# Calculating tangents
tangent = dy / dx
tangent_intercept = y_values - np.multiply(tangent, x_values)


fig, ax = plt.subplots(figsize=(8, 6))  # Adjust the figure size
# Set axis limits
ax.set_xlim(min(x_values), max(x_values))
ax.set_ylim(-0.01, 5)

# Plot the original curve
line, = ax.plot(x_values, y_values, label='Curve', color='blue', linewidth=2)
# Initialize lines for the cycloid and circle
line_circle, = ax.plot([], [], label='Circle', color='green', linewidth=2)
line_epicycloid, = ax.plot([], [], label='Epicycloid', color='orange', linewidth=2)
circle_radius_line, = ax.plot([], [], label='Radius', color='purple', linewidth=2)
# Initialize point for the tracing point
point, = ax.plot([], [], 'ro', label='Tracing Point')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_title('Curve Animation')
ax.legend(loc='upper right')
plt.tight_layout()


# Start point declaration
x, slope = tangent[0], -1
start_vector = np.array([x, slope])
start_vector = start_vector / np.sqrt(np.sum(start_vector ** 2))
start_vector = np.multiply(start_vector, radius)

x, slope = tangent[0] + 2 * radius, -1
start_epicycloid_vector = np.array([x, slope])
start_epicycloid_vector = start_epicycloid_vector / np.sqrt(np.sum(start_epicycloid_vector ** 2))
start_epicycloid_vector = np.multiply(start_epicycloid_vector, -radius * direction)

animation = FuncAnimation(fig, animate_frame, frames=np.arange(len(tangent)), interval=1, repeat=False)

plt.show()