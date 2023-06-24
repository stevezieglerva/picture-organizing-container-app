import numpy as np
from PIL import Image

# Create a NumPy array of RGB colors
rgb_colors = np.array([
    [255, 0, 0],    # Red
    [0, 255, 0],    # Green
    [0, 0, 255],    # Blue
    [255, 255, 0],  # Yellow
    [255, 0, 255],  # Magenta
    [0, 255, 255]   # Cyan
], dtype=np.uint8)

# Specify the dimensions of the image
height, width = 2, 3

# Reshape the array to match the image dimensions
rgb_colors = rgb_colors.reshape((height, width, 3))

# Create a PIL image from the NumPy array
image = Image.fromarray(rgb_colors, 'RGB')

# Display the image
image.show()
