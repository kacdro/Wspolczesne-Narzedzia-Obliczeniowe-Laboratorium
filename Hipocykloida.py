import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def hypocycloid(a, b, t):
    x = (a - b) * np.cos(t) + b * np.cos((a/b - 1) * t)
    y = (a - b) * np.sin(t) - b * np.sin((a/b - 1) * t)
    return x, y

def draw_animation(a, b):
    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    # Draw the outer circle in the background
    outer_circle = plt.Circle((0, 0), 3, color='gray', linestyle='dashed', fill=False, label='Outer Circle (Radius=3)')
    ax.add_patch(outer_circle)

    # Draw the inner circle in the background with solid linestyle
    inner_circle = plt.Circle((0, 0), b, color='orange', linestyle='-', fill=False, label='Inner Circle (Radius=b)')
    ax.add_patch(inner_circle)

    line, = ax.plot([], [], label=f'Hypocycloid ({a},{b})')
    point, = ax.plot([], [], 'ro', label='Tracing Point')
    radius_ray, = ax.plot([], [], 'g-', label='Radius Ray')
    plt.title('Hypocycloid Animation with Circles, Tracing Point, and Radius Ray')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')

    def update(frame):
        t = np.linspace(0, frame / 10, 1000)
        x, y = hypocycloid(a, b, t)
        line.set_data(x, y)

        # Plot the tracing point at the current position
        tracing_x, tracing_y = hypocycloid(a, b, frame / 10)
        point.set_data(tracing_x, tracing_y)

        # Update the position of the inner circle along the edge of the outer circle
        inner_circle.set_center(((a - b) * np.cos(frame / 10), (a - b) * np.sin(frame / 10)))

        # Update the radius ray starting from the center of the inner circle to the tracing point
        radius_ray.set_data([inner_circle.center[0], tracing_x], [inner_circle.center[1], tracing_y])

        return line, point, inner_circle, radius_ray

    ani = FuncAnimation(fig, update, frames=100, interval=50, blit=True)
    plt.show()

# Example: a=3, b=1
draw_animation(3, 1)