import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def draw_epicycloid_frame(frame, R, r, d, epicycloid_line, tracing_point, radius_vector, tangent_circle):
    # Update tracing point on the epicycloid
    theta_tracing_point = 2 * np.pi * frame / frames
    x_tracing_point = (R + r) * np.cos(theta_tracing_point) - d * np.cos((R + r) / r * theta_tracing_point)
    y_tracing_point = (R + r) * np.sin(theta_tracing_point) - d * np.sin((R + r) / r * theta_tracing_point)

    tracing_point.set_data(x_tracing_point, y_tracing_point)

    # Update radius vector starting point
    tangent_circle_center = np.array([4 * np.cos(2 * np.pi * frame / frames), 4 * np.sin(2 * np.pi * frame / frames)])
    radius_vector_start = tangent_circle_center  # Updated starting point to the current position of the tangent circle
    radius_vector.set_data([radius_vector_start[0], x_tracing_point], [radius_vector_start[1], y_tracing_point])

    # Update epicycloid
    theta_epicycloid = np.linspace(0, 2 * np.pi * frame / frames, 1000)
    x_epicycloid = (R + r) * np.cos(theta_epicycloid) - d * np.cos((R + r) / r * theta_epicycloid)
    y_epicycloid = (R + r) * np.sin(theta_epicycloid) - d * np.sin((R + r) / r * theta_epicycloid)

    epicycloid_line.set_data(x_epicycloid, y_epicycloid)

    # Update tangent circle with center at (0, 4) and radius 1
    tangent_circle_radius = 1
    theta_tangent_circle = np.linspace(0, 2 * np.pi, 1000)
    x_tangent_circle = tangent_circle_center[0] + tangent_circle_radius * np.cos(theta_tangent_circle)
    y_tangent_circle = tangent_circle_center[1] + tangent_circle_radius * np.sin(theta_tangent_circle)

    tangent_circle.set_data(x_tangent_circle, y_tangent_circle)

    return epicycloid_line, tracing_point, radius_vector, tangent_circle

# Set the parameters for the epicycloid
R = 3  # Radius of the larger circle
r = 1  # Radius of the smaller circle
d = 1  # Distance from the center of the smaller circle to the tracing point

# Set up the plot
fig, ax = plt.subplots()
epicycloid_line, = ax.plot([], [])
tracing_point, = ax.plot([], [], 'ro', label="Tracing Point")
radius_vector, = ax.plot([], [], 'g-', label="Radius Vector")
tangent_circle, = ax.plot([], [], 'purple', label="Tangent Circle")
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 7)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.legend()

# Set the number of frames for the animation
frames = 100

# Create the animation
ani = animation.FuncAnimation(
    fig, draw_epicycloid_frame, frames=frames, fargs=(R, r, d, epicycloid_line, tracing_point, radius_vector, tangent_circle),
    interval=50, blit=True
)

# Display the animation
plt.show()