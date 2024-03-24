import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def rotate_image(image, angle):
    # Rotate the image by the specified angle
    return np.rot90(image, k=int(angle / 90) % 4)
def graham_scan(points):
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def polar_angle(o, a):
        return np.arctan2(a[1] - o[1], a[0] - o[0])

    # Find the point with the lowest y-coordinate (and leftmost if ties)
    start_point = min(points, key=lambda p: (p[1], p[0]))

    # Sort the points based on polar angle from the start_point
    sorted_points = sorted(points, key=lambda p: (polar_angle(start_point, p), p))

    # Graham's scan algorithm
    hull = [start_point, sorted_points[0]]
    for p in sorted_points[1:]:
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return np.array(hull)

np.random.seed(42)

# Generate 20 random points
num_points = 20
points = np.column_stack((np.random.rand(num_points), np.random.rand(num_points)))

# Set the plot size
plt.figure(figsize=(10, 8))

# Load and rotate the image (replace 'your_image_path.png' with the actual path to your image file)
image_path = 'tiger.png'
image = plt.imread(image_path)
rotation_angles = np.random.uniform(0, 360, size=num_points)  # Generate random rotation angles for each tiger
rotated_images = [rotate_image(image, angle) for angle in rotation_angles]

# Plot the points with the rotated image
for point, rotated_image in zip(points, rotated_images):
    imagebox = OffsetImage(rotated_image, zoom=1)
    ab = AnnotationBbox(imagebox, point, frameon=False, pad=0)
    plt.gca().add_artist(ab)

# Compute and plot the convex hull
convex_hull = graham_scan(points)
convex_hull = np.concatenate((convex_hull, [convex_hull[0]]))  # Close the loop
plt.plot(convex_hull[:, 0], convex_hull[:, 1], 'k-', label='Convex Hull')

# Add labels and title
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Convex Hull around Randomly Generated Tigers')

# Display legend
plt.legend()

# Show the plot
plt.show()