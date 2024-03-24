import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

def transform_coordinates(x, y, translation_x, translation_y, rotation_angle):
    transformed_x = x * np.cos(rotation_angle) - y * np.sin(rotation_angle) + translation_x
    transformed_y = x * np.sin(rotation_angle) + y * np.cos(rotation_angle) + translation_y
    return transformed_x, transformed_y

def initialize_plot():
    trace_dot.set_data([], [])
    trace_label.set_text('')
    trace_label.set_position((0.8, 0.9))
    trace_label.set_text('Tracing Point:')
    trace_label.set_text(f'({0:.2f}, {-P:.2f})')
    trace_label.set_text(f'({0:.2f}, {-P:.2f})')
    trace.set_data([], [])
    radius_line.set_data([0, 0], [0, -P])
    cycloid_line.set_data([], [])
    return cycloid_line, radius_line, trace, trace_dot, trace_label

def generate_positions(theta=0):
    while theta < 4 * np.pi:
        center_coordinates, radius_coordinates = np.array([0, 0]), np.array([0, -P])
        transformed_coordinates = transform_coordinates(center_coordinates, radius_coordinates, theta, 1, -theta)
        yield theta, transformed_coordinates

        theta += angle_increment

def animate_positions(pos):
    theta, transformed_coordinates = pos
    cycloid_line.set_data(cycloid_x + theta, cycloid_y + 1)
    radius_line.set_data(transformed_coordinates[0], transformed_coordinates[1])
    trace_dot.set_data(transformed_coordinates[0][1], transformed_coordinates[1][1])
    trace_label.set_text(f'Tracing Point:\n({transformed_coordinates[0][1]:.2f}, {transformed_coordinates[1][1]:.2f})')

    x_data_points.append(transformed_coordinates[0][1])
    y_data_points.append(transformed_coordinates[1][1])
    trace.set_data(x_data_points, y_data_points)

    return cycloid_line, radius_line, trace, trace_dot, trace_label

# Initialize parameters
theta_values = np.linspace(0, 2 * np.pi, 500)
radius_values, angle_increment, P = np.ones(500), np.pi / 25, 1
cycloid_x, cycloid_y = radius_values * np.cos(theta_values), radius_values * np.sin(theta_values)

# Create the plot
fig, ax = plt.subplots(figsize=(14, 7))
x_data_points, y_data_points = [], []

trace_dot = ax.plot([], [], 'ro', markersize=5)[0]
trace_label = ax.text(0.8, 0.9, 'Tracing Point:', ha='right', va='center', color='black', fontsize=10)

trace = Line2D([], [], color='blue', linewidth=3)
ax.add_line(trace)

radius_line = Line2D([0, 0], [0, -P], color='red', linewidth=3)
ax.add_line(radius_line)

cycloid_line = Line2D(cycloid_x, cycloid_y, color='green', linewidth=3)
ax.add_line(cycloid_line)

ax.axis('equal')
ax.set_aspect('equal', 'box')
ax.set(xlim=(-1.5, 14), ylim=(-1, 4))
ax.grid(color='blue', linewidth=0.5, linestyle='dotted')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
ax.set_title('Cycloid animation')

# Adjust x-axis ticks and labels
ax.set_xticks(np.arange(0, 15, 3))
ax.set_xticklabels(np.arange(0, 15, 3))
ax.set_xlabel('X')

# Create animation
my_animation = animation.FuncAnimation(fig, animate_positions, generate_positions,
                                       interval=20, blit=True, repeat=False, init_func=initialize_plot)

plt.show()