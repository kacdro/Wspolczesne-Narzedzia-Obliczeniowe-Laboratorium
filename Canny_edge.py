import cv2
import numpy as np

def apply_gaussian_blur(image, kernel_size=5):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def manual_convolution(image, kernel):
    # Get the dimensions of the image and kernel
    img_height, img_width = image.shape
    kernel_height, kernel_width = kernel.shape

    # Initialize an empty output image
    output = np.zeros_like(image)

    # Perform manual convolution
    for i in range(1, img_height - 1):
        for j in range(1, img_width - 1):
            # Extract the region of interest from the image
            roi = image[i - 1:i + 2, j - 1:j + 2]

            # Perform element-wise multiplication and summation
            convolution_result = np.sum(roi * kernel)

            # Assign the result to the corresponding pixel in the output image
            output[i, j] = convolution_result

    return output

def compute_gradients(image):
    canny_kernel_x = np.array([[-1, 0, 1],
                               [-2, 0, 2],
                               [-1, 0, 1]])

    canny_kernel_y = np.array([[-1, -2, -1],
                               [0, 0, 0],
                               [1, 2, 1]])

    # Manual convolution for gradient_x and gradient_y
    gradient_x = manual_convolution(image, canny_kernel_x)
    gradient_y = manual_convolution(image, canny_kernel_y)

    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    gradient_direction = np.arctan2(gradient_y, gradient_x)

    gradient_direction = np.rad2deg(gradient_direction) % 180

    return gradient_magnitude, gradient_direction
def non_maximum_suppression(gradient_magnitude, gradient_direction):
    edge_image = np.zeros_like(gradient_magnitude, dtype=np.uint8)

    for i in range(1, gradient_magnitude.shape[0] - 1):
        for j in range(1, gradient_magnitude.shape[1] - 1):
            orientation = gradient_direction[i, j]

            if 0 <= orientation < 22.5 or 157.5 <= orientation < 180:
                neighbors = [gradient_magnitude[i, j - 1], gradient_magnitude[i, j + 1]]
            elif 22.5 <= orientation < 67.5:
                neighbors = [gradient_magnitude[i - 1, j - 1], gradient_magnitude[i + 1, j + 1]]
            elif 67.5 <= orientation < 112.5:
                neighbors = [gradient_magnitude[i - 1, j], gradient_magnitude[i + 1, j]]
            else:
                neighbors = [gradient_magnitude[i - 1, j + 1], gradient_magnitude[i + 1, j - 1]]

            if gradient_magnitude[i, j] >= max(neighbors):
                edge_image[i, j] = 255

    return edge_image

def edge_tracking_by_hysteresis(edge_image, low_threshold, high_threshold):
    strong_edges = (edge_image >= high_threshold)
    weak_edges = (edge_image >= low_threshold) & (edge_image < high_threshold)

    edge_image_final = np.zeros_like(edge_image, dtype=np.uint8)
    edge_image_final[strong_edges] = 255

    # Use edge tracking by hysteresis for weak edges
    strong_i, strong_j = np.nonzero(strong_edges)
    weak_i, weak_j = np.nonzero(weak_edges)

    for i, j in zip(weak_i, weak_j):
        neighbors = edge_image_final[i-1:i+2, j-1:j+2]
        if np.any(neighbors == 255):
            edge_image_final[i, j] = 255

    return edge_image_final

# Load the image in grayscale
input_image = cv2.imread('PG.jpg', cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur
blurred_image = apply_gaussian_blur(input_image)

# Compute gradients
gradient_magnitude, gradient_direction = compute_gradients(blurred_image)

# Non-maximum suppression
edge_image = non_maximum_suppression(gradient_magnitude, gradient_direction)

# Edge tracking by hysteresis
low_threshold = 50
high_threshold = 150
edge_image_final = edge_tracking_by_hysteresis(edge_image, low_threshold, high_threshold)

cv2.imwrite('custom_canny_edges.png', edge_image_final)
