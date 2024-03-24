import cv2
import numpy as np

# Load the image in grayscale
input_image = cv2.imread('PG.jpg', cv2.IMREAD_GRAYSCALE)

input_image = cv2.medianBlur(input_image, 5)

# Define Kirsch kernels for all eight orientations
kirsch_kernels = [
    np.array([[5, 5, 5],
              [-3, 0, -3],
              [-3, -3, -3]]),

    np.array([[-3, -3, 5],
              [-3, 0, 5],
              [-3, -3, 5]]),

    np.array([[-3, 5, 5],
              [-3, 0, 5],
              [-3, -3, -3]]),

    np.array([[-3, 5, 5],
              [-3, 0, 5],
              [-3, -3, -3]]).T,

    np.array([[-3, -3, -3],
              [-3, 0, 5],
              [-3, 5, 5]]),

    np.array([[-3, -3, -3],
              [5, 0, -3],
              [5, 5, -3]]),

    np.array([[5, -3, -3],
              [5, 0, -3],
              [5, -3, -3]]),

    np.array([[5, 5, -3],
              [5, 0, -3],
              [-3, -3, -3]]),
]

# Function to perform convolution manually
def convolve2d(image, kernel):
    kernel = np.flipud(np.fliplr(kernel))
    output = np.zeros_like(image)

    for i in range(image.shape[0] - 2):
        for j in range(image.shape[1] - 2):
            output[i, j] = np.sum(image[i:i + 3, j:j + 3] * kernel)

    return output

# Compute gradients for all eight orientations
gradients = [convolve2d(input_image, kernel) for kernel in kirsch_kernels]

# Compute absolute values of the gradients
gradients = [np.abs(gradient) for gradient in gradients]

# Combine the gradients
edge_image = np.sum(gradients, axis=0)

# Normalize the resulting image to the range [0, 255]
edge_image = cv2.normalize(edge_image, None, 0, 255, cv2.NORM_MINMAX)

# Convert to uint8
edge_image = edge_image.astype(np.uint8)

# Save the result
cv2.imwrite('kirsch_edges.png', edge_image)