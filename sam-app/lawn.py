import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def get_dominant_color(image):
    colors = image.getcolors(image.width * image.height)
    dominant_color = max(colors, key=lambda item: item[0])[1]
    return dominant_color


def normalize_color(color, num_bins):
    rgb = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
    normalized_color = tuple(int(c * num_bins / 256) for c in rgb)
    normalized_hex = "#{:02x}{:02x}{:02x}".format(*normalized_color)
    return normalized_hex


def generate_html_table(grid, image_path):
    html = f"<img width=300px; src='{image_path}'/><table>"
    for row in grid:
        html += "<tr>"
        for color in row:
            html += (
                f'<td height=10px; width=10px; style="background-color: {color};"></td>'
            )
        html += "</tr>"
    html += "</table>"
    return html


def rotate_grid(grid):
    transposed_grid = list(map(list, zip(*grid)))
    # Reverse each row to mirror the grid
    mirrored_grid = [row for row in transposed_grid]

    return mirrored_grid


def analyze_lawn(image_path, grid_size=(30, 25)):
    # Load the image
    image = Image.open(image_path)
    print(image.size)
    aspect_ratio = image.size[0] / image.size[1]
    print(aspect_ratio)
    width = 32
    height = int(width / aspect_ratio)
    grid_size = (width, height)

    # Resize the image
    image = image.resize(grid_size)

    # Convert the image to RGB
    image = image.convert("RGB")

    # Create the grid
    grid_width = image.width // grid_size[0]
    grid_height = image.height // grid_size[1]
    grid = [[None for _ in range(grid_size[1])] for _ in range(grid_size[0])]

    # Iterate through each grid cell
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            # Define the coordinates of the current grid cell
            left = x * grid_width
            upper = y * grid_height
            right = (x + 1) * grid_width
            lower = (y + 1) * grid_height

            # Crop the image to the current grid cell
            cell_image = image.crop((left, upper, right, lower))

            # Calculate the dominant color in the cell
            dominant_color = get_dominant_color(cell_image)

            # Convert RGB to HTML color code
            html_color_code = "#{:02x}{:02x}{:02x}".format(*dominant_color)

            # Store the HTML color code in the grid
            grid[x][y] = html_color_code

    # Generate HTML table with color-coded cells
    rotated_grid = rotate_grid(grid)
    html_table = generate_html_table(rotated_grid, image_path)

    # Print or save the HTML table
    with open("lawn.html", "w") as file:
        file.write(html_table)

    # Flatten the grid to create a list of HTML color codes
    flattened_grid = np.array(rotated_grid).flatten()

    # Calculate the histogram of HTML color codes
    histogram, bins = np.histogram(flattened_grid, bins=np.unique(flattened_grid))

    # Plot the histogram
    plt.bar(bins[:-1], histogram, color=bins[:-1])
    plt.xlabel("HTML Color Code")
    plt.ylabel("Count")
    plt.title("Histogram of Dominant Color Codes")
    plt.xticks(rotation=45)
    plt.show()


# Usage example
image_path = "lawn_2.jpg"  # Replace with the path to your image
analyze_lawn(image_path)
